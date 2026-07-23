#!/usr/bin/env python3
"""Extract title + abstract from all .md paper files in a directory.

Usage:
    python3 extract_abstracts.py <corpus_dir> <output_file>

Reads each .md file (first 8KB — abstract is always near top), extracts title from
frontmatter and abstract from the first ## Abstract / Abstract section, and writes
all to a single compact file for parallel screening.

Each paper gets ~500 chars of abstract — enough to judge relevance without reading
the full paper.
"""
import os
import re
import sys


def extract_abstracts(corpus_dir: str, output_file: str) -> int:
    papers = []
    for root, dirs, files in os.walk(corpus_dir):
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                    content = fh.read(8000)  # abstract is always near top
            except Exception:
                continue

            # Extract title from frontmatter
            title_match = re.search(r'^title:\s*"(.+?)"', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f.replace(".md", "")

            # Extract abstract — look for "## Abstract" or "Abstract" then text until next ##
            abs_match = re.search(
                r'(?:## Abstract|Abstract)[:\s]*(.+?)(?:\n## |\n# |\nKeywords|\n1\. Introduction|\Z)',
                content,
                re.DOTALL | re.IGNORECASE,
            )
            if abs_match:
                abstract = abs_match.group(1).strip()[:500]
            else:
                abstract = "(no abstract found) " + content[:300]

            papers.append(f"### {title}\n{abstract}\n")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"# All Paper Abstracts ({len(papers)} papers)\n\n")
        for p in papers:
            out.write(p + "\n")

    return len(papers)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_abstracts.py <corpus_dir> <output_file>")
        sys.exit(1)
    corpus_dir = sys.argv[1]
    output_file = sys.argv[2]
    count = extract_abstracts(corpus_dir, output_file)
    size = os.path.getsize(output_file)
    print(f"Extracted {count} abstracts to {output_file} ({size} bytes)")
