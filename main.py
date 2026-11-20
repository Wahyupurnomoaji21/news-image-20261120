#!/usr/bin/env python3
"""news-image-20261120 entrypoint: copy entry.png to the output dir.

The front page is rendered ahead of time by compose.py (Pillow, local
assets only) and stored in this repository as entry.png. This program
does no drawing, no resizing and no network access: it only copies the
stored bytes to $MAKEFUN_OUTPUT_DIR/entry.png (default /output), after
checking the file fits the competition's 1 MiB cap. Two runs therefore
always write identical bytes.

Local test:
    rm -rf out1 out2
    MAKEFUN_OUTPUT_DIR=out1 python3 main.py
    MAKEFUN_OUTPUT_DIR=out2 python3 main.py
    cmp out1/entry.png out2/entry.png
"""

import hashlib
import os
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
LIMIT = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    return 1


def main():
    if not os.path.isfile(SOURCE):
        return fail(f"entry.png missing: {SOURCE} (run: python3 compose.py)")
    with open(SOURCE, "rb") as fh:
        blob = fh.read()
    if len(blob) > LIMIT:
        return fail(f"entry.png is {len(blob)} bytes, over the {LIMIT} byte cap")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(blob)
    digest = hashlib.sha256(blob).hexdigest()
    with open(target, "rb") as fh:
        written = fh.read()
    if hashlib.sha256(written).hexdigest() != digest:
        return fail(f"verify failed: {target} differs from entry.png")
    print(f"wrote {len(blob)} bytes to {target}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
