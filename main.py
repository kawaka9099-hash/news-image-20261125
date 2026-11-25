#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261125.

The front page itself is drawn by draw.py and stored in this repo as
entry.png. This program just places a copy of that image at the path
the grader expects. It uses only the Python standard library, so it
runs in a bare Python 3.13 sandbox with no network and no packages.

Output path, in order of preference:
  1. the first command-line argument, if one is given
  2. $MAKEFUN_OUTPUT_DIR/entry.png, if that variable is set
  3. /output/entry.png
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED_IMAGE = HERE / "entry.png"


def pick_destination():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return Path(out_dir) / "entry.png"
    return Path("/output/entry.png")


def main():
    dest = pick_destination()
    if dest.parent and str(dest.parent):
        dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BUNDLED_IMAGE, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
