#!/usr/bin/env python3
"""Rename and resize extracted images using a mapping file.

Usage: python3 optimize_images.py <workdir> <mapping.json> <images_outdir>
mapping.json: {"names": {"p01_x17": "randy-buckner", ...}, "photos": ["p01_x17", ...]}
Raw images not listed in "names" are skipped (use this to drop duplicates).
"""
import glob, json, os, sys
from PIL import Image

PHOTO_MAX, OTHER_MAX = 500, 1400


def main(workdir, mapping_path, outdir):
    with open(mapping_path) as fh:
        m = json.load(fh)
    names, photos = m["names"], set(m.get("photos", []))
    os.makedirs(outdir, exist_ok=True)
    done = set()
    for f in sorted(glob.glob(os.path.join(workdir, "raw", "*"))):
        stem = os.path.basename(f).rsplit(".", 1)[0]
        if stem not in names:
            print(f"skip  {stem}")
            continue
        im = Image.open(f)
        size = PHOTO_MAX if stem in photos else OTHER_MAX
        im.thumbnail((size, size))
        has_alpha = im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255
        if has_alpha:
            path = os.path.join(outdir, names[stem] + ".png")
            im.save(path, optimize=True)
        else:
            path = os.path.join(outdir, names[stem] + ".jpg")
            im.convert("RGB").save(path, quality=85, optimize=True)
        done.add(stem)
        print(f"wrote {os.path.basename(path)}")
    missing = set(names) - done
    if missing:
        print("WARNING: mapping entries with no raw image: " + ", ".join(sorted(missing)))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
