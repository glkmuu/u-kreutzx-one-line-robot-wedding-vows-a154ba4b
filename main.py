#!/usr/bin/env python3
"""One-Line Robot Wedding Vows — make.fun entrypoint.

Reads entry.txt (one line, 1-160 chars), validates the competition gate,
and writes it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.txt.
Python 3.13, standard library only.
"""

import os
import sys

MAX_CHARS = 160


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    with open(src, "rb") as f:
        raw = f.read()

    # Decode strictly: the gate requires UTF-8 text.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("error: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    if "\r" in text:
        print("error: entry must not contain carriage returns", file=sys.stderr)
        return 1

    # Gate: exactly one line, 1-160 characters, not only whitespace.
    # A single trailing newline in the source file is not part of the line.
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    if len(lines) != 1:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    line = lines[0]
    if not (1 <= len(line) <= MAX_CHARS):
        print(f"error: entry is {len(line)} chars, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not line.strip():
        print("error: entry must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Write bytes exactly: no trailing newline, no encoding surprises.
    with open(out_path, "wb") as f:
        f.write(line.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
