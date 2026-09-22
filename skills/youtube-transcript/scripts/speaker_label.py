#!/usr/bin/env python3
"""Label 老高與小茉 Whisper transcripts from the original audio.

The existing Whisper segments have timestamps but no diarization.  This tool
uses a fast MFCC classifier to propose Xiaomo turns, then verifies each
candidate against reference speaker embeddings from a manually checked
two-host episode.  Original transcripts are never modified.

Outputs mirror the input tree under ``output/speaker-labeled`` and contain
JSON, TXT, and SRT derivatives.  Re-running is resume-safe unless
``--overwrite`` is supplied.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import math
import subprocess
import sys

import numpy as np
from scipy.fft import dct
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SAMPLE_RATE = 16_000
FRAME = 400
HOP = 160
NFFT = 512
NMEL = 40
MFCCS = 20

# Manually checked clean turns in QAGDGja7kbs.  Ranges are deliberately
# conservative: none crosses a speaker boundary.
REFERENCE_VIDEO = "QAGDGja7kbs"
XIAOMO_RANGES = [
    (457.74, 459.24),
    (482.10, 484.86),
    (488.84, 490.76),
    (493.56, 497.06),
    (506.58, 509.48),
    (908.12, 909.72),
    (912.00, 913.16),
    (1193.98, 1195.18),
    (1195.96, 1197.86),
    (1212.94, 1215.08),
    (1222.28, 1224.08),
    (1243.28, 1246.00),
    (1255.06, 1256.36),
]
LAOGAO_RANGES = [
    (1.0, 5.0),
    (20.46, 24.48),
    (100.00, 104.26),
    (299.34, 303.80),
    (439.54, 443.04),
    (445.04, 451.22),
    (459.24, 464.80),
    (497.06, 503.06),
    (513.14, 518.12),
    (900.96, 906.00),
    (914.88, 919.96),
    (1197.86, 1203.98),
    (1215.08, 1219.68),
    (1225.48, 1231.48),
    (1246.00, 1253.34),
]

# Text is only a weak tie-breaker after acoustic scoring.  It never creates a
# label by itself.
REACTION_TEXT = {
    "是吗", "真的吗", "真的假的", "为什么", "不会吧", "太可怕了", "好可怕",
    "什么意思", "怎么会", "然后呢", "对吗", "挺不容易的",
}


@dataclass
class Episode:
    transcript: Path
    audio: Path
    payload: dict
    features: np.ndarray
    waveform: np.ndarray


def _patch_old_torch_for_speechbrain() -> None:
    """SpeechBrain 1.1 supports newer torch.amp; this venv has torch 2.2."""
    import torch

    if hasattr(torch.amp, "custom_fwd"):
        return

    def custom_fwd(fwd=None, *, device_type=None, cast_inputs=None):
        del device_type
        return torch.cuda.amp.custom_fwd(fwd, cast_inputs=cast_inputs)

    def custom_bwd(bwd=None, *, device_type=None):
        del device_type
        return torch.cuda.amp.custom_bwd(bwd)

    torch.amp.custom_fwd = custom_fwd
    torch.amp.custom_bwd = custom_bwd


def video_id(path: Path) -> str:
    return path.parent.name.rsplit("__", 1)[-1]


def find_audio(audio_dir: Path, vid: str) -> Path:
    matches = sorted(audio_dir.glob(f"*__{vid}.*"))
    if not matches:
        raise FileNotFoundError(f"no audio for {vid}")
    return matches[0]


def decode_audio(path: Path) -> np.ndarray:
    proc = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar",
            str(SAMPLE_RATE), "-f", "s16le", "-",
        ],
        check=True,
        capture_output=True,
    )
    return np.frombuffer(proc.stdout, dtype="<i2").astype(np.float32) / 32768.0


def mel_filterbank() -> np.ndarray:
    def mel(hz):
        return 2595 * np.log10(1 + hz / 700)

    def hz(value):
        return 700 * (10 ** (value / 2595) - 1)

    points = hz(np.linspace(mel(60), mel(7600), NMEL + 2))
    bins = np.floor((NFFT + 1) * points / SAMPLE_RATE).astype(int)
    bank = np.zeros((NMEL, NFFT // 2 + 1), dtype=np.float32)
    for index in range(1, NMEL + 1):
        left, center, right = bins[index - 1:index + 2]
        bank[index - 1, left:center] = (
            np.arange(left, center) - left
        ) / max(1, center - left)
        bank[index - 1, center:right] = (
            right - np.arange(center, right)
        ) / max(1, right - center)
    return bank


MEL_BANK = mel_filterbank()
WINDOW = np.hanning(FRAME).astype(np.float32)


def segment_feature(waveform: np.ndarray, start: float, end: float) -> np.ndarray:
    left = max(0, round(start * SAMPLE_RATE))
    right = min(len(waveform), round(end * SAMPLE_RATE))
    audio = waveform[left:right]
    if len(audio) < FRAME:
        audio = np.pad(audio, (0, FRAME - len(audio)))
    starts = np.arange(1 + (len(audio) - FRAME) // HOP) * HOP
    frames = np.stack([audio[pos:pos + FRAME] for pos in starts])
    frames = (frames - frames.mean(axis=1, keepdims=True)) * WINDOW
    spectrum = np.abs(np.fft.rfft(frames, NFFT)) ** 2
    log_mel = np.log(np.maximum(spectrum @ MEL_BANK.T, 1e-10))
    mfcc = dct(log_mel, type=2, axis=1, norm="ortho")[:, :MFCCS]
    energy = np.log(np.maximum(np.mean(frames * frames, axis=1), 1e-10))
    keep = energy > np.percentile(energy, 20)
    if keep.sum() >= 2:
        mfcc = mfcc[keep]
    return np.concatenate(
        [mfcc.mean(0), mfcc.std(0), np.percentile(mfcc, [25, 75], axis=0).ravel()]
    )


def episode_features(payload: dict, waveform: np.ndarray) -> np.ndarray:
    return np.stack(
        [segment_feature(waveform, row["start"], row["end"])
         for row in payload["segments"]]
    )


def normalize_features(features: np.ndarray) -> np.ndarray:
    median = np.median(features, axis=0)
    iqr = np.percentile(features, 75, axis=0) - np.percentile(features, 25, axis=0)
    return (features - median) / np.maximum(iqr, 0.1)


def load_episode(transcript: Path, audio_dir: Path) -> Episode:
    payload = json.loads(transcript.read_text(encoding="utf-8"))
    audio = find_audio(audio_dir, video_id(transcript))
    waveform = decode_audio(audio)
    return Episode(
        transcript=transcript,
        audio=audio,
        payload=payload,
        features=episode_features(payload, waveform),
        waveform=waveform,
    )


def overlap_indices(segments: list[dict], ranges: list[tuple[float, float]]) -> list[int]:
    found = []
    for index, row in enumerate(segments):
        midpoint = (row["start"] + row["end"]) / 2
        if any(start <= midpoint <= end for start, end in ranges):
            found.append(index)
    return found


def train_fast_classifier(reference: Episode):
    features = normalize_features(reference.features)
    rows = reference.payload["segments"]
    female = overlap_indices(rows, XIAOMO_RANGES)
    male = overlap_indices(rows, LAOGAO_RANGES)
    indices = female + male
    labels = np.array([1] * len(female) + [0] * len(male))
    classifier = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=0.15, class_weight="balanced", max_iter=2000),
    )
    classifier.fit(features[indices], labels)
    return classifier


def likely_xiaomo_segments(classifier, episode: Episode) -> tuple[np.ndarray, np.ndarray]:
    rows = episode.payload["segments"]
    probabilities = classifier.predict_proba(normalize_features(episode.features))[:, 1]

    # Short direct reactions are common Xiaomo turns.  They receive only a
    # modest boost and must already have female-like acoustics.
    for index, row in enumerate(rows):
        text = row["text"].strip(" ，。！？!?…")
        duration = row["end"] - row["start"]
        if duration <= 4 and (
            text in REACTION_TEXT or text.endswith(("吗", "呢", "啊", "吧"))
        ) and probabilities[index] >= 0.45:
            probabilities[index] = max(probabilities[index], 0.82)

    # Keep the candidate net broad, but verify every segment separately.  A
    # previous run-level verifier swallowed Laogao's first reply when it sat
    # directly after a Xiaomo question.
    candidates = probabilities >= 0.72
    return probabilities, candidates


def candidate_runs(mask: np.ndarray, segments: list[dict]) -> list[tuple[int, int]]:
    del segments
    return [(index, index + 1) for index in np.flatnonzero(mask)]


def clip(waveform: np.ndarray, start: float, end: float, seconds: float = 1.5):
    left = max(0, round(start * SAMPLE_RATE))
    right = min(len(waveform), round(end * SAMPLE_RATE))
    audio = waveform[left:right]
    target = round(seconds * SAMPLE_RATE)
    if len(audio) > target:
        offset = (len(audio) - target) // 2
        audio = audio[offset:offset + target]
    actual = len(audio)
    if actual < target:
        audio = np.pad(audio, (0, target - actual))
    return audio.astype(np.float32), min(1.0, actual / target)


def load_voice_model(model_dir: Path):
    _patch_old_torch_for_speechbrain()
    from speechbrain.inference.speaker import EncoderClassifier
    from speechbrain.utils.fetching import LocalStrategy

    return EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=str(model_dir),
        local_strategy=LocalStrategy.COPY,
        run_opts={"device": "cpu"},
    )


def encode_clips(model, clips: list[np.ndarray], lengths: list[float], batch=32):
    import torch

    if not clips:
        return np.empty((0, 192), dtype=np.float32)
    result = []
    with torch.no_grad():
        for start in range(0, len(clips), batch):
            waves = torch.from_numpy(np.stack(clips[start:start + batch]))
            lens = torch.tensor(lengths[start:start + batch])
            encoded = model.encode_batch(waves, lens).squeeze(1).cpu().numpy()
            encoded /= np.maximum(np.linalg.norm(encoded, axis=1, keepdims=True), 1e-9)
            result.append(encoded)
    return np.concatenate(result)


def reference_embeddings(model, episode: Episode):
    clips = []
    lengths = []
    labels = []
    for label, ranges in (("XIAOMO", XIAOMO_RANGES), ("LAOGAO", LAOGAO_RANGES)):
        for start, end in ranges:
            audio, length = clip(episode.waveform, start, end)
            clips.append(audio)
            lengths.append(length)
            labels.append(label)
    embeddings = encode_clips(model, clips, lengths)
    references = {}
    for label in ("XIAOMO", "LAOGAO"):
        center = np.mean(embeddings[np.array(labels) == label], axis=0)
        references[label] = center / np.linalg.norm(center)
    return references


def verify_runs(model, references, episode: Episode, probabilities, runs):
    rows = episode.payload["segments"]
    clips = []
    lengths = []
    for start, end in runs:
        audio, length = clip(
            episode.waveform, rows[start]["start"], rows[end - 1]["end"]
        )
        clips.append(audio)
        lengths.append(length)
    embeddings = encode_clips(model, clips, lengths)
    accepted = []
    run_scores = []
    for (start, end), embedding, length in zip(runs, embeddings, lengths):
        sim_f = float(embedding @ references["XIAOMO"])
        sim_m = float(embedding @ references["LAOGAO"])
        acoustic = float(np.max(probabilities[start:end]))
        text = rows[start]["text"].strip(" ，。！？!?…")
        is_reaction = text in REACTION_TEXT or text.endswith(("吗", "呢", "啊", "吧"))
        # Very short reactions rely more on the fast acoustic model; identity
        # embeddings need roughly a second of voiced audio to be dependable.
        if length < 0.55 and is_reaction and len(text) <= 8 and acoustic >= 0.82:
            is_xiaomo = True
        else:
            is_xiaomo = sim_f - sim_m >= 0.005
        confidence = 1 / (1 + math.exp(-18 * (sim_f - sim_m)))
        accepted.append(is_xiaomo)
        run_scores.append((confidence, sim_f, sim_m, acoustic))
    return accepted, run_scores


def ts(seconds: float) -> str:
    total = int(seconds)
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def srt_ts(seconds: float) -> str:
    total = round(seconds * 1000)
    hours, rest = divmod(total, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    secs, millis = divmod(rest, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_outputs(episode: Episode, output_root: Path, probabilities, runs,
                  accepted, run_scores):
    payload = dict(episode.payload)
    rows = [dict(row) for row in payload["segments"]]
    for index, row in enumerate(rows):
        row["speaker"] = "LAOGAO"
        row["speaker_confidence"] = round(float(1 - probabilities[index]), 4)
        row["speaker_method"] = "voice_mfcc"
    for (start, end), keep, scores in zip(runs, accepted, run_scores):
        confidence, sim_f, sim_m, acoustic = scores
        for index in range(start, end):
            rows[index]["speaker"] = "XIAOMO" if keep else "LAOGAO"
            rows[index]["speaker_confidence"] = round(
                float(confidence if keep else 1 - confidence), 4
            )
            rows[index]["speaker_method"] = "voice_reference"
            rows[index]["speaker_similarity"] = {
                "xiaomo": round(sim_f, 4),
                "laogao": round(sim_m, 4),
                "mfcc": round(acoustic, 4),
            }
    payload["segments"] = rows
    payload["speaker_labeling"] = {
        "method": "MFCC candidate detection + ECAPA voice-reference verification",
        "reference_video": REFERENCE_VIDEO,
        "labels": ["LAOGAO", "XIAOMO"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_transcript": str(episode.transcript),
        "source_audio": str(episode.audio),
        "caveat": "Whisper boundaries can contain more than one voice; review low-confidence or unusually long segments.",
    }
    folder = output_root / episode.transcript.parent.name
    folder.mkdir(parents=True, exist_ok=True)
    stem = episode.transcript.stem
    json_path = folder / f"{stem}.speaker-labeled.json"
    txt_path = folder / f"{stem}.speaker-labeled.txt"
    srt_path = folder / f"{stem}.speaker-labeled.srt"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with txt_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(
                f"[{ts(row['start'])}] [{row['speaker']}] {row['text']}\n"
            )
    with srt_path.open("w", encoding="utf-8") as handle:
        for index, row in enumerate(rows, 1):
            handle.write(
                f"{index}\n{srt_ts(row['start'])} --> {srt_ts(row['end'])}\n"
                f"[{row['speaker']}] {row['text']}\n\n"
            )
    return json_path


def parse_args():
    skill = Path(__file__).resolve().parent.parent
    output = skill / "output"
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input-dir", type=Path, default=output / "whisper-large-v3")
    parser.add_argument("--audio-dir", type=Path, default=output / "audio")
    parser.add_argument("--output-dir", type=Path, default=output / "speaker-labeled")
    parser.add_argument("--model-dir", type=Path, default=skill.parent.parent / ".cache" / "speechbrain" / "spkrec-ecapa-voxceleb")
    parser.add_argument("--video-id", action="append", help="label only this video ID (repeatable)")
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    transcripts = sorted(args.input_dir.glob("*/*.json"))
    if args.video_id:
        wanted = set(args.video_id)
        transcripts = [path for path in transcripts if video_id(path) in wanted]
    if args.shard_count < 1 or not 0 <= args.shard_index < args.shard_count:
        raise SystemExit("shard index must be in [0, shard count)")
    transcripts = [
        path for index, path in enumerate(transcripts)
        if index % args.shard_count == args.shard_index
    ]
    reference_path = next(
        (path for path in args.input_dir.glob(f"*__{REFERENCE_VIDEO}/*.json")), None
    )
    if reference_path is None:
        raise SystemExit(f"reference transcript {REFERENCE_VIDEO} not found")

    print("Loading reference episode and voice model...", flush=True)
    reference = load_episode(reference_path, args.audio_dir)
    fast_classifier = train_fast_classifier(reference)
    voice_model = load_voice_model(args.model_dir)
    references = reference_embeddings(voice_model, reference)

    completed = skipped = failed = 0
    for number, transcript in enumerate(transcripts, 1):
        folder = args.output_dir / transcript.parent.name
        destination = folder / f"{transcript.stem}.speaker-labeled.json"
        if destination.exists() and not args.overwrite:
            skipped += 1
            print(f"[{number}/{len(transcripts)}] {video_id(transcript)} skip", flush=True)
            continue
        try:
            episode = reference if transcript == reference_path else load_episode(transcript, args.audio_dir)
            probabilities, candidates = likely_xiaomo_segments(fast_classifier, episode)
            runs = candidate_runs(candidates, episode.payload["segments"])
            accepted, scores = verify_runs(
                voice_model, references, episode, probabilities, runs
            )
            path = write_outputs(
                episode, args.output_dir, probabilities, runs, accepted, scores
            )
            xiaomo = sum(
                accepted[index] * (runs[index][1] - runs[index][0])
                for index in range(len(runs))
            )
            completed += 1
            print(
                f"[{number}/{len(transcripts)}] {video_id(transcript)} ok "
                f"({xiaomo}/{len(episode.payload['segments'])} Xiaomo segments) -> {path}",
                flush=True,
            )
        except Exception as exc:
            failed += 1
            print(f"[{number}/{len(transcripts)}] {video_id(transcript)} FAILED: {exc}", file=sys.stderr, flush=True)

    print(f"Done: {completed} completed, {skipped} skipped, {failed} failed", flush=True)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
