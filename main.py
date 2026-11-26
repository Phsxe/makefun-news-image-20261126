#!/usr/bin/env python3
"""news-image-20261126 entry: standard library only.

The newspaper image is pre-rendered and stored beside this file as
entry.png. The program just copies it to the grader's output directory.
No third-party packages are used, because the grader runs the entry in
a pinned Python image with nothing installed beyond the standard library.
"""

import os
import shutil

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        raise SystemExit(f"missing pre-rendered image: {source}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = os.path.join(here, "out")
    os.makedirs(out_dir, exist_ok=True)

    destination = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, destination)
    if os.path.getsize(destination) != os.path.getsize(source):
        raise SystemExit(f"copy incomplete: {destination}")
    print(f"wrote {destination}  1024x1024")


if __name__ == "__main__":
    main()
