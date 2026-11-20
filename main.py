#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry (harness program/v1).

The approved front-page image lives in this repo as entry.png. This program
does one thing: copy that file byte-for-byte to the harness output
directory as entry.png, then verify the copy by size and SHA-256.

No rendering happens here, no network, no randomness: two runs always
write identical bytes.

Output directory comes from MAKEFUN_OUTPUT_DIR (default /output).
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
MAX_BYTES = 1024 * 1024  # harness limit: image must be <= 1 MiB


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def run() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        return fail(f"missing {source}")

    payload = source.read_bytes()
    if len(payload) > MAX_BYTES:
        return fail(
            f"{SOURCE_NAME} is {len(payload)} bytes, over the "
            f"{MAX_BYTES} byte limit"
        )
    source_hash = sha256_hex(payload)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return fail(f"cannot create output dir {out_dir}: {exc}")

    target = out_dir / SOURCE_NAME
    # Write via a temp file and rename, so an interrupted run never
    # leaves a half-written entry.png behind.
    tmp_target = out_dir / (SOURCE_NAME + ".tmp")
    try:
        tmp_target.write_bytes(payload)
        os.replace(tmp_target, target)
    except OSError as exc:
        return fail(f"cannot write {target}: {exc}")

    written = target.read_bytes()
    if written != payload:
        return fail(f"verify failed: {target} differs from {source}")
    written_hash = sha256_hex(written)
    if written_hash != source_hash:
        return fail("verify failed: sha256 mismatch after copy")

    print(f"wrote {target} ({len(written)} bytes)")
    print(f"sha256 {written_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
