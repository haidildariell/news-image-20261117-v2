#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered entry.png to the output directory.

Stdlib only, no network. The image itself is generated at build time by
build_image.py (see README.md); copying guarantees that repeated runs
write byte-identical output.
"""
import os
import shutil
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print(dst.stat().st_size)


if __name__ == "__main__":
    main()
