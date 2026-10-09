---
name: repository-use-case-to-markdown
description: Convert a PDF of a data repository use case, data sharing story, or researcher profile (for example Harvard Dataverse, Dryad, Figshare, Zenodo, OSF or Vivli use cases) into a clean Markdown file that keeps the photos, logos, screenshots and QR codes from the PDF, delivered as a zip with an images folder. Use this whenever the user uploads a use case, case study, data sharing story or interview-style PDF and asks to format, convert, reformat or turn it into Markdown or .md, or asks for "the same as before" on another use case PDF, even if they don't mention images.
---

# Repository Use Case PDF → Markdown with images

Turns an interview-style repository use case PDF (title page with a pull quote, project metadata block, team headshots, Q&A sections, screenshots of repository pages, and closing promotional pages) into a faithful Markdown document with every distinct image extracted, given a descriptive name, and placed where it appeared in the original.

The output is a zip containing `<Name>_Use_Case.md` plus an `images/` folder. The Markdown uses relative paths (`images/...`), so the two must travel together. That's why the zip is the primary deliverable.

## Requirements

The scripts need Python 3.9 or later with Pillow and PyMuPDF. They install PyMuPDF automatically if it's missing. All `scripts/` and `references/` paths below are relative to this skill's folder, the folder that contains this `SKILL.md`. Run the scripts from there or use their full paths.

## Workflow

### 1. Read the PDF text

If the PDF content is already in context, use it. Otherwise read it with `pdftotext -layout` (or the `pdf-reading` skill, if one is available). Note the order of sections, speaker initials, and every URL that is actually printed in the text.

### 2. Extract the images and look at them

```bash
python3 scripts/extract_images.py <input.pdf> <workdir>
```

The script installs PyMuPDF if it's missing. It writes each distinct image (deduplicated by PDF object, with transparency masks merged so logos keep their alpha) to `<workdir>/raw/pNN_xREF.(png|jpg)`. It also writes a labeled contact sheet to `<workdir>/contact_sheet.jpg`.

**View the contact sheet.** This is the only reliable way to tell which file is which person or screenshot. Match headshots to names using the caption order in the PDF, such as "(Clockwise, left to right)" or the name printed under each photo. Logos usually repeat on the first and last pages. The repeat is often a different object, so use one copy and skip the rest.

### 2b. Render designed regions that have text over an image

Header banners and title cards are often built from a background photo with text, an icon or a dark translucent box layered on top. In the PDF these are separate objects, so the raw extracted background shows none of that text. Placing it in the Markdown with the title as a separate heading looks nothing like the original. For example, a brain-cell photo appears on its own with the "As a researcher, I want to…" title stacked below it.

`extract_images.py` prints a **POSSIBLE OVERLAYS** list for images like this. For each flagged image that's part of the design (rather than, say, a screenshot with a callout over it), render the region from the page as it actually looks:

1. **Find the visible bounds.** The image's placement rectangle often runs past what's visible, because frames or white boxes cover the rest. Render a probe with a coordinate grid around the reported rectangle and view it:
   ```bash
   python3 scripts/render_region.py in.pdf 1 --probe 0 0 612 200 probe.png
   ```
2. **Render the exact region.** Use bounds just inside any decorative frame or border:
   ```bash
   python3 scripts/render_region.py in.pdf 1 20.5 23 592 161 <outdir>/images/header-banner.jpg
   ```
3. **View the result** and adjust the bounds until no frame edge or clipped text remains.

Then use the rendered image instead of the raw background and the separate icon. Leave those out of the mapping in step 3. When the overlaid text is the page title, put the banner inside the H1 with the full title as alt text:

```markdown
# ![As a researcher, I want to use the Harvard Dataverse Repository to share Big Data …](images/header-banner.jpg)
```

This keeps the original look, avoids printing the title twice, and keeps the title text in the document for accessibility and search. Keep any image credit for the background, such as an image gallery attribution line, in the footer.

### 3. Name and optimize the images

Write a small JSON mapping of raw stem to descriptive kebab-case name, and list which stems are headshots:

```json
{
  "names": {"p01_x17": "randy-buckner", "p02_x50": "gsp-dataset-page", "p01_x16": "harvard-dataverse-logo"},
  "photos": ["p01_x17"]
}
```

Then run:

```bash
python3 scripts/optimize_images.py <workdir> mapping.json <outdir>/images
```

Headshots are resized to 500px and screenshots to 1400px, as JPEG at quality 85. Images with transparency, typically logos, stay PNG. Any raw image left out of the mapping is skipped, which is how duplicates are dropped.

Naming conventions: people get `firstname-lastname`, logos get `<org>-logo`, screenshots get a short description of what's shown (`cafe-dataverse-collection`, `jnp-cerebellum-article`), and QR codes get `qr-<target>`.

### 4. Write the Markdown

Follow the structure in `references/template.md`. Key points:

- **Be faithful to the text.** Keep every Q&A answer in full, in the original order, with the original speaker labels such as **(DB):**. This is a reformat, not a summary.
- **Use headings for the questions.** Each interview question becomes an `##` heading, and a `---` rule separates sections.
- **Use blockquotes for quotes.** Pull quotes and testimonial quotes become blockquotes with an attribution line.
- **Put headshots in captioned grids.** Use a Markdown table whose first row holds `<img src="images/x.jpg" alt="Name" width="150">` cells and whose second row holds `**Name**<br>Title`. HTML `<img>` is used so the photos display at a consistent size. Use at most 3 per row and start a new table for more.
- **Place screenshots with Markdown image syntax.** Use `![descriptive alt](images/x.jpg)`, put an italic caption below when the PDF had one, and place each screenshot next to the text it illustrated in the PDF.
- **Size logos and QR codes with HTML.** Use `<img ... height="70">` for logos and `width="160"` for QR codes.
- **Turn schedules into tables.** Webinar schedules and similar lists become a Markdown table.
- **Keep the funding statement.** A funding or support footer that repeats on every page appears once, at the end.

### 5. Links: never invent URLs

Link only URLs that come from the PDF itself. There are three sources, in order of preference:

1. **Embedded hyperlinks.** `extract_images.py` prints an **EMBEDDED HYPERLINKS** list of every link in the file with its exact target. Display text like "repository's advanced search" or "Link to article" usually has its real URL here even when no address is visible on the page. Use these targets on the matching display text.
2. **URLs printed in the visible text.**
3. **URLs legibly visible in a screenshot,** such as a DOI on an article page.

When link text has no target from any of these, leave it as plain text and mention it in the final summary. A guessed URL that's wrong is worse than no link.

### 6. Light copy-editing, reported

Fix only obvious typos and transcription slips, such as "tdata" → "the data", "too deposit" → "to deposit", duplicated words, or a stray space inside a name. Also fix speaker-label mismatches, such as a label whose initials match no participant. Don't rephrase speech. When the PDF spells a name two different ways, choose the spelling from the title page and flag it. Keep a list of every change so you can report it in step 8.

### 7. Verify and package

```bash
python3 scripts/check_and_package.py <outdir>/<Name>_Use_Case.md <zip_path>
```

The script checks that every `images/...` reference in the Markdown exists, reports images that are never referenced, and zips the `.md` and `images/` together. Fix any missing references before delivering.

### 8. Deliver

Put the zip, and the `.md` file so it can be previewed, wherever this environment delivers files to the user, and share both, zip first:

- **Claude.ai:** copy them to `/mnt/user-data/outputs/` and present them with the file-presentation tool.
- **Claude Code and other environments:** write them to the user's working directory, or to the folder the user named, and give the paths.

Keep the reply short:

- one line on what's included, with image counts by type (headshots, logos, screenshots, QR codes)
- a note that the zip should be downloaded, because the `.md` needs its `images/` folder next to it
- the copy-edit changes and any unlinked or uncertain items from steps 5 and 6

## Edge cases

- **Vector-only figures.** `pdfimages` and PyMuPDF only see raster images. If a figure is visible on the page but missing from the contact sheet, rasterize the page with `pdftoppm -r 150 -f N -l N` and crop the region with PIL.
- **Grayscale or CMYK images.** The extraction script converts these to RGB automatically.
- **Very long PDFs with many screenshots.** Still view the contact sheet. The script paginates it into `contact_sheet_2.jpg` and later sheets when there are more than 36 images.
- **No images at all.** Produce a single `.md` file with no zip and say so.
