#!/usr/bin/env python3
"""Inspect printable protobuf strings in an iOS WeChat chat-room contact record."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while offset < len(data) and shift < 70:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, offset
        shift += 7
    raise ValueError("invalid varint")


def printable(value: str) -> bool:
    value = value.strip("\x00\r\n\t ")
    return len(value) >= 2 and sum(ch.isprintable() for ch in value) / len(value) > 0.9


def protobuf_strings(data: bytes, depth: int = 0) -> list[str]:
    if depth > 5 or not data:
        return []
    strings: list[str] = []
    offset = 0
    try:
        while offset < len(data):
            key, offset = read_varint(data, offset)
            wire = key & 7
            if key == 0:
                break
            if wire == 0:
                _, offset = read_varint(data, offset)
            elif wire == 1:
                offset += 8
            elif wire == 2:
                length, offset = read_varint(data, offset)
                if length < 0 or offset + length > len(data):
                    break
                chunk = data[offset : offset + length]
                offset += length
                try:
                    decoded = chunk.decode("utf-8")
                    if printable(decoded):
                        strings.append(decoded.strip("\x00\r\n\t "))
                except UnicodeDecodeError:
                    pass
                strings.extend(protobuf_strings(chunk, depth + 1))
            elif wire == 5:
                offset += 4
            else:
                break
    except (ValueError, IndexError):
        pass
    return strings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("database", type=Path)
    parser.add_argument("group_name")
    args = parser.parse_args()

    connection = sqlite3.connect(f"{args.database.resolve().as_uri()}?immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    rows = connection.execute("SELECT * FROM Friend")
    matches = []
    for row in rows:
        fields: dict[str, list[str]] = {}
        all_strings: list[str] = []
        raw_match = False
        for key in row.keys():
            value = row[key]
            if isinstance(value, bytes):
                raw_match = raw_match or args.group_name.encode("utf-8") in value
                values = list(dict.fromkeys(protobuf_strings(value)))
                if values:
                    fields[key] = values
                    all_strings.extend(values)
        if args.group_name == row["userName"] or raw_match or any(args.group_name in value for value in all_strings):
            matches.append({"userName": row["userName"], "fields": fields})
    print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
