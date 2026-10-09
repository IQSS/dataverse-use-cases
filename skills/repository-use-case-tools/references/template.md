# Output template

Adapt this to the PDF: drop sections that don't exist and keep sections in the PDF's order. Everything in `[brackets]` is a placeholder. `[Program]` is the initiative or program that published the use case, if the PDF names one; drop it if not.

````markdown
<p>
  <img src="images/[project]-logo.png" alt="[Project] logo" height="70">
  &nbsp;&nbsp;
  <img src="images/[program]-logo.png" alt="[Program] logo" height="70">
  &nbsp;&nbsp;
  <img src="images/harvard-dataverse-logo.png" alt="Harvard Dataverse logo" height="70">
</p>

# [Title exactly as on the PDF's first page]

*[Repository] · [Program] data sharing story — Published [YYYY-MM-DD]*

> "[Pull quote]"
>
> — [Speaker], [credential]

---

## Project Overview

**Principal Investigators / Researcher(s) or Team:** [...]

**Dataset(s) shared / Project Collection Page:** <[url]>

**Related publication(s):** [linked only if the URL is printed or visible]

**Funding:** [keep grant numbers in bold if bold in the PDF]

### [Interviewees / The Team]

| <img src="images/[first-last].jpg" alt="[Name]" width="150"> | <img src="images/[first-last].jpg" alt="[Name]" width="150"> | <img src="images/[first-last].jpg" alt="[Name]" width="150"> |
|:---:|:---:|:---:|
| **[Name] ([initials])**<br>[Title] | **[Name]**<br>[Title] | **[Name]**<br>[Title] |

---

## [Interview question, verbatim]

**([initials]):** [Answer paragraph, verbatim apart from obvious typo fixes]

[Further paragraphs]

![[Descriptive alt text]](images/[screenshot-name].jpg)
*[Caption from the PDF, with its URL if one was printed]*

---

[...repeat for every question...]

> "[Testimonial quote from a sidebar]"
>
> — [Name], [Title], [Organization]

### [Bulleted list from the PDF, e.g. "Curation and development tasks"]

- [item]

---

## Connect with [Program]

[Bulleted links, screenshots, QR codes]

<img src="images/qr-[target].jpg" alt="QR code for [target]" width="160">

### [Webinar series title]

![[Banner alt]](images/[program]-webinar-banner.jpg)

| Webinar | Topic | Date |
|---|---|---|
| 1 | [...] | [...] |

**Register here:** [link]

<img src="images/qr-[target].jpg" alt="QR code to register" width="160">

---

*[Funding or support statement, exactly as written in the PDF]*

<h2 align="center">Thank you!</h2>
````

## Notes

- **Speaker labels.** When answers come from a single unnamed speaker, as in a single-PI story, omit the labels and leave the answers as plain paragraphs.
- **Citations.** Dataset citations and publication lists get their own sub-heading. Use a numbered list for publications and a blockquote for a formal dataset citation.
- **Headshots shown more than once.** When the PDF repeats a headshot next to a quote, you may reuse the same image file there. Don't save a second copy.
