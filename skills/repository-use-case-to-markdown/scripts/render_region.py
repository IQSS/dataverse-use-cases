#!/usr/bin/env python3
"""Render a region of a PDF page exactly as it appears, overlays included.

Probe mode draws a coordinate grid so you can read off exact bounds:
  python3 render_region.py <input.pdf> <page> --probe <x0> <y0> <x1> <y1> <out.png>

Render mode writes the final cropped image (JPEG unless out ends in .png):
  python3 render_region.py <input.pdf> <page> <x0> <y0> <x1> <y1> <out.jpg> [dpi]

Coordinates are PDF points (page is usually 612 x 792); page numbers start at 1.
"""
import subprocess, sys

try:
    import pymupdf as fitz
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "pymupdf",
                    "--break-system-packages", "-q"], check=True)
    import pymupdf as fitz
from PIL import Image, ImageDraw


def render(pdf, page, rect, dpi):
    pix = fitz.open(pdf)[page - 1].get_pixmap(dpi=dpi, clip=fitz.Rect(*rect))
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def probe(pdf, page, rect, out, dpi=150, step=10):
    im = render(pdf, page, rect, dpi)
    d = ImageDraw.Draw(im)
    s = dpi / 72
    x0, y0, x1, y1 = rect
    v = (int(x0) // step + 1) * step
    while v < x1:
        px = (v - x0) * s
        d.line([(px, 0), (px, im.height)], fill=(0, 200, 255) if v % 50 else (255, 0, 255), width=1)
        if v % 50 == 0:
            d.text((px + 2, 2), str(v), fill=(255, 0, 255))
        v += step
    v = (int(y0) // step + 1) * step
    while v < y1:
        py = (v - y0) * s
        d.line([(0, py), (im.width, py)], fill=(0, 200, 255) if v % 50 else (255, 0, 255), width=1)
        if v % 50 == 0:
            d.text((2, py + 2), str(v), fill=(255, 0, 255))
        v += step
    im.save(out)
    print(f"Probe written to {out}: grid every {step} pt, labels every 50 pt")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 8 and a[2] == "--probe":
        probe(a[0], int(a[1]), tuple(map(float, a[3:7])), a[7])
    elif len(a) in (7, 8):
        dpi = int(a[7]) if len(a) == 8 else 200
        im = render(a[0], int(a[1]), tuple(map(float, a[2:6])), dpi)
        if a[6].lower().endswith(".png"):
            im.save(a[6], optimize=True)
        else:
            im.save(a[6], quality=88, optimize=True)
        print(f"Wrote {a[6]} ({im.width}x{im.height})")
    else:
        sys.exit(__doc__)
