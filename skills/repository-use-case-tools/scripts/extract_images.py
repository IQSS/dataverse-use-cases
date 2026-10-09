#!/usr/bin/env python3
"""Extract distinct raster images from a PDF and build labeled contact sheets.

Usage: python3 extract_images.py <input.pdf> <workdir>
Writes <workdir>/raw/pNN_xREF.(png|jpg) and <workdir>/contact_sheet*.jpg
"""
import glob, os, subprocess, sys

try:
    import pymupdf as fitz
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "pymupdf",
                    "--break-system-packages", "-q"], check=True)
    import pymupdf as fitz
from PIL import Image, ImageDraw


def extract(pdf, workdir):
    raw = os.path.join(workdir, "raw")
    os.makedirs(raw, exist_ok=True)
    doc = fitz.open(pdf)
    seen = set()
    for pno, page in enumerate(doc, 1):
        for img in page.get_images(full=True):
            xref, smask = img[0], img[1]
            if xref in seen:
                continue  # same image object reused on another page
            seen.add(xref)
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha > 3:  # CMYK etc.
                pix = fitz.Pixmap(fitz.csRGB, pix)
            stem = os.path.join(raw, f"p{pno:02d}_x{xref}")
            if smask:  # merge transparency mask so logos keep alpha
                try:
                    pix = fitz.Pixmap(pix, fitz.Pixmap(doc, smask))
                    pix.save(stem + ".png")
                    continue
                except Exception:
                    pass
            if pix.n - pix.alpha == 1:  # grayscale
                pix = fitz.Pixmap(fitz.csRGB, pix)
            if pix.alpha:
                pix.save(stem + ".png")
            else:
                with open(stem + ".jpg", "wb") as f:
                    f.write(pix.tobytes("jpeg"))
    return sorted(glob.glob(os.path.join(raw, "*")))


def find_overlays(pdf):
    """Flag images that have text or other images drawn on top of them.

    Such images (header banners, title cards) look wrong when the raw image is
    used on its own, because the overlay text and icons are separate page objects.
    These regions must be rendered from the page instead (see render_region.py).
    """
    doc = fitz.open(pdf)
    found = []
    for pno, page in enumerate(doc, 1):
        prect = page.rect
        texts = [fitz.Rect(b[:4]) for b in page.get_text("blocks") if b[4].strip()]
        placements = []
        for img in page.get_images(full=True):
            for r in page.get_image_rects(img[0]):
                placements.append((img[0], r & prect))
        for xref, r in placements:
            if r.is_empty or r.get_area() < 0.02 * prect.get_area():
                continue
            hits_text = [t for t in texts if (t & r).get_area() > 0.8 * t.get_area()]
            hits_img = [x for x, o in placements
                        if x != xref and not o.is_empty and (o & r).get_area() > 0.8 * o.get_area()
                        and o.get_area() < 0.5 * r.get_area()]
            if hits_text or hits_img:
                found.append((pno, xref, r, len(hits_text), hits_img))
    return found


def list_links(pdf):
    """Return (page, link text, uri) for every external hyperlink in the PDF.

    Many use cases show display text ("data management page", "Link to article")
    whose real URL exists only in the link annotation, not in the visible text.
    """
    doc = fitz.open(pdf)
    out = []
    for pno, page in enumerate(doc, 1):
        for l in page.get_links():
            uri = l.get("uri")
            if not uri:
                continue
            r = l["from"]
            words = [w[4] for w in page.get_text("words")
                     if fitz.Rect(w[:4]).intersects(r)
                     and (fitz.Rect(w[:4]) & r).get_area() > 0.5 * fitz.Rect(w[:4]).get_area()]
            out.append((pno, " ".join(words), uri))
    return out


def contact_sheets(files, workdir, per_sheet=36, cols=6, cell=200):
    out = []
    for s in range(0, len(files), per_sheet):
        chunk = files[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cell * cols, (cell + 20) * rows), "white")
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            src = Image.open(f)
            w, h = src.size
            im = src.convert("RGBA")
            bg = Image.new("RGBA", im.size, (220, 220, 220, 255))
            bg.alpha_composite(im)
            im = bg.convert("RGB")
            im.thumbnail((cell - 4, cell - 4))
            x, y = (i % cols) * cell, (i // cols) * (cell + 20)
            sheet.paste(im, (x + 2, y + 2))
            d.text((x + 2, y + cell + 2), f"{os.path.basename(f)}  {w}x{h}", fill="black")
        n = s // per_sheet + 1
        name = os.path.join(workdir, "contact_sheet.jpg" if n == 1 else f"contact_sheet_{n}.jpg")
        sheet.save(name, quality=85)
        out.append(name)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    files = extract(sys.argv[1], sys.argv[2])
    print(f"Extracted {len(files)} distinct images:")
    for f in files:
        print("  " + os.path.basename(f))
    if files:
        for s in contact_sheets(files, sys.argv[2]):
            print("Contact sheet: " + s)
    else:
        print("No raster images found (figures may be vector; rasterize pages with pdftoppm).")
    links = list_links(sys.argv[1])
    if links:
        print("\nEMBEDDED HYPERLINKS (link text -> target):")
        for pno, text, uri in links:
            print(f"  page {pno}: \"{text}\" -> {uri}")
    overlays = find_overlays(sys.argv[1])
    if overlays:
        print("\nPOSSIBLE OVERLAYS (text or images drawn on top of an image):")
        for pno, xref, r, ntext, imgs in overlays:
            extra = f", images x{', x'.join(map(str, imgs))}" if imgs else ""
            print(f"  page {pno} image x{xref} at ({r.x0:.0f},{r.y0:.0f},{r.x1:.0f},{r.y1:.0f}) pt: "
                  f"{ntext} text block(s){extra} on top")
        print("  -> If the overlay is part of the design (banner, title card), render the region with "
              "render_region.py instead of using the raw image. See SKILL.md step 2b.")
