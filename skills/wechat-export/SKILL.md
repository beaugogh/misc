---
name: wechat-export
description: Export, convert, inspect, validate, or selectively retain authorized WeChat chat history from unencrypted iPhone Finder/iTunes backups on macOS. Use for offline HTML, JSON, or CSV archives and for distinguishing parseable Finder backups from encrypted WeChat migration archives.
---

# WeChat Export

Preserve the source backup and write exports to a separate destination. Treat all outputs as sensitive personal data.

## Choose the input path

- For an iPhone Finder/iTunes backup containing `Manifest.db`, read [references/backup-formats.md](references/backup-formats.md), confirm `Manifest.plist` reports `IsEncrypted = 0`, then use the bundled exporter.
- For legacy `Backup.db` + `BAK_*_TEXT`/`BAK_*_MEDIA` or modern `backup.attr` + `ChatPackage`/`.tar.enc` archives, read the same reference. Do not claim these are directly parseable: they require WeChat restoration or format-specific decryption.
- Do not modify, prune, or delete a raw backup while exporting it.

## Export from an unencrypted Finder backup

Use the wrapper so the bundled runtime finds its templates and receives a UTF-8 locale:

```bash
python3 scripts/export_wechat.py \
  --backup "/path/to/MobileSync/Backup/<device-id>" \
  --output "/path/to/new-output" \
  --account "<account display name>"
```

Omit `--account` to export every discovered account. Add `--session "<visible chat name>"` repeatedly for a targeted export. Omit all sessions for a full export.

The bundled `WechatExporterCmd` is third-party version 1.9.5.13 for x64 macOS. Its licenses are preserved under `vendor/wechat-exporter-1.9.5.13/LICENSES`. On incompatible hardware or macOS versions, obtain a compatible build instead of altering the backup.

Exporter warnings about malformed unsupported payloads or unavailable remote avatars do not by themselves mean message extraction failed. Verify the finished archive before relying on it.

## Convert HTML to JSON and CSV

The HTML viewer stores up to roughly 1,000 messages inline and later messages in `<conversation>_files/Data/msg-*.js`. Never parse only the top-level HTML source.

```bash
python3 scripts/convert_wechat_export.py \
  "/path/to/html-output/<account>" \
  "/path/to/structured-output"
```

This writes `messages.json`, `messages.csv`, and `export_summary.json` while reading both inline and lazy-loaded messages.

## Validate

```bash
python3 scripts/audit_wechat_export.py \
  "/path/to/html-output/<account>" \
  --structured "/path/to/structured-output"
```

Require zero missing local HTML/media references and equal HTML, JSON, CSV, and summary message counts. Open the account `index.html` and spot-check long chats before deleting any redundant copy.

An exported folder can be self-contained while each individual `.html` file is not. Preserve the account directory, shared `Portrait`/`Emoji` folders, every `<conversation>_files` directory, and the indexes together.

## Inspect groups or retain selected conversations

To inspect a WCDB contact database for a group/contact name:

```bash
python3 scripts/inspect_wechat_group.py /path/to/contact.db "<name>"
```

To prune a working export to an exact allowlist after making and validating a full copy:

```bash
python3 scripts/keep_selected_wechat_conversations.py \
  "/path/to/html-output/<account>" \
  "/path/to/structured-output" \
  "Chat One" "Chat Two"
```

This is destructive within the supplied export directories. Resolve exact targets first, preserve the raw backup, and keep a verified full export until the reduced copy is checked.

## Completion criteria

Report the output paths, conversation/message counts, size, validation result, and any skipped empty/service sessions or unavailable content. Distinguish a readable archival export from a lossless raw backup: unsupported WeChat objects may remain placeholders even when all referenced local files are present.
