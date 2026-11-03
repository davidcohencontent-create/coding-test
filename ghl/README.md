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
The checkout is Whop's `EmbeddedCheckout` React component (`whop-checkout/EmbeddedCheckout.jsx`, plan `plan_IJNoDfl4ZUsMy`),
bundled with React into `funnel/whop-checkout.js`. The footer code loads that file from the GitHub Pages copy when the visitor
nears the prices and mounts it in the price section (`10-precios.html`). Nothing to paste for it.

- Card payments: once the payment stands, the buyer is sent to **`/gracias`**.
- Off-site methods (Klarna, bank transfer…): Whop returns to `/gracias?status=…`; a failed or cancelled payment shows
  "El pago no se ha completado" with a button back to the checkout (`/#checkout`; edit `SALES_URL` in `gracias/02-gracias.html`
  if the sales page has its own path).

Add the Gracias step (path `gracias`): same **Header Code** and **Custom CSS** as the sales page (no Footer Code), then
[`gracias/01-cabecera.html`](gracias/01-cabecera.html), [`gracias/02-gracias.html`](gracias/02-gracias.html), [`gracias/03-pie.html`](gracias/03-pie.html).

The 457 € "Con Judith" option is shown as fully booked ("Plazas completas", button disabled).

To change the checkout (plan, colours, language): edit `whop-checkout/EmbeddedCheckout.jsx` or `funnel/page.js`,
run `cd whop-checkout && npm install && npm run build`, then `python3 ghl/build.py`, and bump `?v=` in `WHOP_CHECKOUT_SCRIPT`.
