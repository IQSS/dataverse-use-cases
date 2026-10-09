#!/usr/bin/env python3
"""Verify image references in a Markdown file and zip it with its images folder.

Usage: python3 check_and_package.py <file.md> <output.zip>
Exits non-zero if any referenced image is missing.
"""
import os, re, sys, zipfile


def main(md_path, zip_path):
    base = os.path.dirname(os.path.abspath(md_path))
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    refs = set(re.findall(r'(images/[^\s")\'>]+)', text))
    missing = [r for r in sorted(refs) if not os.path.isfile(os.path.join(base, r))]
    img_dir = os.path.join(base, "images")
    present = set("images/" + f for f in os.listdir(img_dir)) if os.path.isdir(img_dir) else set()
    unused = sorted(present - refs)
    print(f"{len(refs)} image references, {len(present)} files in images/")
    if unused:
        print("Unreferenced images (place them or delete them): " + ", ".join(unused))
    if missing:
        print("MISSING images: " + ", ".join(missing))
        sys.exit(1)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(md_path, os.path.basename(md_path))
        for r in sorted(present):
            z.write(os.path.join(base, r), r)
    print(f"Wrote {zip_path} ({os.path.getsize(zip_path) / 1e6:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
