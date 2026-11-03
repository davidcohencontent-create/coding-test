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

## 3. Checkout (74 € via Whop) and the Gracias step
The Whop checkout for the 74 € plan (`plan_IJNoDfl4ZUsMy`) is embedded **in the price section of the sales page** (`10-precios.html`),
next to the offer card. Nothing to paste for it: the footer code sets the plan and loads Whop when the visitor nears the prices.
After paying, Whop sends the buyer to the funnel step with path **`/gracias`**.

Add that step: same **Header Code** and **Custom CSS** as the sales page (no Footer Code), then the sections in order:
[`gracias/01-cabecera.html`](gracias/01-cabecera.html), [`gracias/02-gracias.html`](gracias/02-gracias.html), [`gracias/03-pie.html`](gracias/03-pie.html).

The 457 € option is a slim line under the checkout; its "Elegir" stays on the prices until it is decided (`WHOP_CHECKOUT_URL_CON_JUDITH` in the footer code).
