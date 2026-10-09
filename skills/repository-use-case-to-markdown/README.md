# repository-use-case-to-markdown

A Claude skill that converts a PDF of a data repository use case into a Markdown file. The Markdown keeps the photos, logos, screenshots, QR codes, header banners and hyperlinks from the PDF.

## Install

**Claude.ai:** Download this folder `repository-use-case-to-markdown` from this repository's [Releases](../../releases) page, then upload it under **Settings → Capabilities → Skills**.

**Claude Code:** Clone or copy this folder into `~/.claude/skills/` for personal use, or into `.claude/skills/` inside a project:

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/repository-use-case-to-markdown ~/.claude/skills/repository-use-case-to-markdown
```

The scripts need Python 3.9 or later with Pillow and PyMuPDF (`pip install pillow pymupdf`). They install PyMuPDF automatically if it's missing.

## Use

Give Claude a use case PDF and ask, for example:

> Format this use case as a Markdown file and include images from the file

You get a zip containing the `.md` file and an `images/` folder. Keep them together, because the Markdown uses relative image paths.

## Contents

- **`SKILL.md`:** the instructions Claude follows
- **`references/template.md`:** the Markdown output template
- **`scripts/`:** helper scripts for extracting images and links, rendering header banners, resizing images, and packaging the result. These also run on their own; see each script's header for usage.

## License

[MIT](LICENSE)
