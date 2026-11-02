# Curso de Confianza: GHL version

Generated from `funnel/` by `python3 ghl/build.py`. Rebuild after any change to the page, then re-paste what changed.

## 1. Page-wide code (once)
In the funnel step: **Edit page → Settings**.

| File | Where it goes in GHL |
|---|---|
| `1-head-code.html` | Settings → Tracking Code → **Header** |
| `2-custom-css.css` | Settings → **Custom CSS** |
| `3-footer-code.html` | Settings → Tracking Code → **Footer** |

## 2. Sections (in this order)
For each file in `sections/`:
1. Add a **Section**: full width, padding top/bottom 0, no background.
2. Add a **Row** with 1 column: full width, row and column padding 0.
3. Add a **Custom JS/HTML** (code) element and paste the whole file.

`01-cabecera`: also turn on **Sticky** in that section's settings (the header can't stick by itself inside a code element).

## Notes
- Everything is wrapped in `<div class="jc">` and every style is prefixed with `.jc`, so GHL's styles and the page's styles don't clash.
- Images load from the GitHub Pages copy (`.../funnel/img/`). To host them in GHL instead, upload them to the GHL media library and replace those URLs.
- The scripts start once GHL has finished rendering; animations and the Day 1 trailer timer may not run inside the editor, only in Preview / the live page.
- Whop checkout links are still `TODO client` at the top of the footer code.
