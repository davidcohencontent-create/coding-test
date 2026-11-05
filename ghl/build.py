#!/usr/bin/env python3
"""Build GoHighLevel-ready pieces from funnel/: head code, scoped custom CSS, footer code and one HTML file per section.

Run from the repo root:  python3 ghl/build.py
Everything is scoped under the .jc wrapper class so the page styles and GHL's own styles cannot clash.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / 'funnel', ROOT / 'ghl'
IMG_BASE = 'https://davidcohencontent-create.github.io/coding-test/funnel/img/'  # swap for GHL media URLs later if wanted

# ---------- CSS: scope every selector under .jc ----------
def scope_selector(sel):
    sel = sel.strip()
    if sel in (':root', 'body'): return '.jc'
    if sel == 'html': return 'html'
    if sel == '*': return '.jc,.jc *,.jc *::before,.jc *::after'
    if sel.startswith('*'): return '.jc ' + sel
    return '.jc ' + sel

def split_top(s, ch=','):
    parts, depth, cur = [], 0, ''
    for c in s:
        depth += c == '('; depth -= c == ')'
        if c == ch and depth == 0: parts.append(cur); cur = ''
        else: cur += c
    return parts + [cur]

def scope_block(css):
    out, i = [], 0
    while i < len(css):
        if css.startswith('/*', i):
            j = css.index('*/', i) + 2; out.append(css[i:j]); i = j; continue
        if css[i].isspace(): out.append(css[i]); i += 1; continue
        j = css.index('{', i); head = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            depth += css[k] == '{'; depth -= css[k] == '}'; k += 1
        body = css[j + 1:k - 1]
        if head.startswith('@keyframes'): out.append(f'{head}{{{body}}}')
        elif head.startswith('@'): out.append(f'{head}{{{scope_block(body)}}}')
        else: out.append(','.join(scope_selector(s) for s in split_top(head)) + '{' + body + '}')
        i = k
    return ''.join(out)

css = (SRC / 'styles.css').read_text()
css = css[:css.index('/* Funnel steps: checkout, upsell, thank you */')]  # checkout pages are handled by Whop
css = css[css.index('*/') + 2:].lstrip()                                   # drop the file header comment
scoped = scope_block(css)
# GHL gives headings, paragraphs etc. their own colours and fonts; inside .jc they must inherit from the page.
# Inserted right after the base rules so the page's own, more specific rules still win.
reset = ('.jc h1,.jc h2,.jc h3,.jc h4,.jc p,.jc li,.jc ul,.jc ol,.jc blockquote,.jc figure,.jc figcaption,'
         '.jc summary,.jc span,.jc strong,.jc em{color:inherit;font-family:inherit}\n'
         '.jc h1,.jc h2,.jc h3{font-family:var(--serif)}\n')
anchor = '.jc a{color:inherit}'
assert anchor in scoped
scoped = scoped.replace(anchor, reset + anchor, 1)
scoped += '''
/* GHL: neutralise GHL's section/row/column/element boxes around our sections, so every section runs edge to edge
   with no white strips or gaps, whatever padding, width or background those boxes were given in the builder */
html:has(.jc),body:has(.jc){background:#f3f1ef!important}
body :has(> .jc),body :has(.jc){padding:0!important;margin:0!important;max-width:none!important;gap:0!important;border:0!important;box-shadow:none!important;background:transparent!important;min-height:0!important}
.jc{display:block;width:100%}
'''
scoped += '''
/* GHL: the header is not sticky inside a code element; make its GHL section sticky instead (section settings) */
.jc header{position:relative}
'''
(OUT / '2-custom-css.css').write_text('/* Curso de Confianza · Judith Calzada: paste into GHL page Settings → Custom CSS */\n' + scoped)

# ---------- Head code ----------
(OUT / '1-head-code.html').write_text('''<!-- Curso de Confianza: paste into GHL page Settings → Tracking Code → Header -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap">
''')

# ---------- Footer code: Vimeo API + all page behaviour, started once GHL has rendered the sections ----------
js = (SRC / 'motion.js').read_text() + '\n' + (SRC / 'page.js').read_text()
_ws = "const WHOP_CHECKOUT_SCRIPT = 'whop-checkout.js?v=2';"
assert _ws in js
js = js.replace(_ws, "const WHOP_CHECKOUT_SCRIPT = 'https://davidcohencontent-create.github.io/coding-test/funnel/whop-checkout.js?v=2';")
(OUT / '3-footer-code.html').write_text('''<!-- Curso de Confianza: paste into GHL page Settings → Tracking Code → Footer -->
<script src="https://player.vimeo.com/api/player.js"></script>
<script>
(function () {
  function start() {
    if (window.__jcStarted || !document.querySelector('.jc')) return false;
    window.__jcStarted = true;
''' + '\n'.join('    ' + l if l else '' for l in js.splitlines()) + '''
    return true;
  }
  // GHL renders the page in stages: try on load, then retry briefly until the sections exist.
  var tries = 0;
  function tick() { if (!start() && !window.__jcStarted && tries++ < 40) setTimeout(tick, 250); }
  if (document.readyState === 'complete') setTimeout(tick, 300);
  else window.addEventListener('load', function () { setTimeout(tick, 300); });
})();
</script>
''')

# ---------- Sections ----------
html = (SRC / 'index.html').read_text()
html = html.replace('src="img/', 'src="' + IMG_BASE)
body = html[html.index('<header>'):html.index('<script src=')]
header = body[:body.index('</header>') + 9]
main = body[body.index('<main id="top">') + len('<main id="top">'):body.index('</main>')]
footer = body[body.index('<footer'):]  # footer + its small links script
footer = footer[:footer.index('</script>') + 9]
# Legal pages are their own GHL steps: point links at the step paths instead of the preview's .html files
LEGAL = {'aviso-legal': 'Aviso legal y condiciones', 'privacidad': 'Política de privacidad', 'cookies': 'Política de cookies'}
def ghl_links(s):
    for slug in LEGAL: s = s.replace(f"'{slug}.html'", f"'/{slug}'").replace(f'"{slug}.html"', f'"/{slug}"')
    return s.replace('href="index.html"', 'href="/"')
footer = ghl_links(footer)
# The footer points at the legal pages as published in GHL. Once the domain is live these can go back to
# '/aviso-legal', '/privacidad' and '/cookies' (just delete this block).
GHL_LEGAL_URLS = {
    'aviso-legal': 'https://sites.leadconnectorhq.com/preview/6lP5PHsxGXzSwwL30aFo',
    'privacidad': 'https://sites.leadconnectorhq.com/preview/ZfjXAtHTgjp0tmcPc56W',
    'cookies': 'https://sites.leadconnectorhq.com/preview/tI6Yp7prPVe6shtS6gGP',
}
for slug, url in GHL_LEGAL_URLS.items():
    assert f"'/{slug}'" in footer; footer = footer.replace(f"'/{slug}'", f"'{url}'")

# Split main into its top-level <section>s; the comment lines right above a section belong to it
lines = main.split('\n'); starts = []
for i, l in enumerate(lines):
    if l.startswith('  <section'):
        j = i
        while j > 0 and lines[j - 1].startswith('  <!-- '): j -= 1
        starts.append(j)
blocks = ['\n'.join(lines[a:b]).strip('\n') for a, b in zip(starts, starts[1:] + [len(lines)])]
SLUGS = ['hero', 'esto-es-para-ti', 'yo-me-sentia-igual', 'programa-10-dias', 'herramientas',
         'resenas-y-logos', 'dos-caminos', 'mi-historia', 'precios', 'faq']
assert len(blocks) == len(SLUGS), (len(blocks), [b[:60] for b in blocks])
names = []
sec_dir = OUT / 'sections'; sec_dir.mkdir(exist_ok=True)
for f in sec_dir.glob('*.html'): f.unlink()
def write(n, slug, content):
    p = sec_dir / f'{n:02d}-{slug}.html'
    p.write_text(f'<div class="jc">\n{content.rstrip()}\n</div>\n'); names.append(p.name)
write(1, 'cabecera', header.replace('href="#top"', 'href="#"'))
for n, (slug, b) in enumerate(zip(SLUGS, blocks), start=2): write(n, slug, b)
n = len(SLUGS) + 2
write(n, 'pie', footer)
print('css', len(scoped), 'chars; sections:', *names, sep='\n  ')

# ---------- Extra funnel step: Gracias (Whop sends buyers here after paying) ----------
simple_header = '''<div class="jc">
<header>
  <div class="wrap">
    <span class="name">Judith Calzada</span>
  </div>
</header>
</div>
'''
gracias = '''<div class="jc">
<section class="thanks">
  <div class="wrap">
    <div class="intro">
      <h1>Ya estás <em>dentro.</em></h1>
      <p>Gracias por tu confianza. Tu acceso al Curso de Confianza está en camino.</p>
      <p class="cta" data-course hidden><a class="btn" href="#">Entrar al curso</a></p>
    </div>
    <ol class="thanks-list">
      <li><div><h3>Revisa tu email</h3><p>Whop te envía la confirmación del pago y el acceso al curso. Si no lo ves, mira en spam o promociones.</p></div></li>
      <li><div><h3>Empieza por el Día 1</h3><p>La confianza es un hábito y así se entrena.</p></div></li>
      <li><div><h3>Reserva un rato cada día</h3><p>Lección, ejercicio y meditación, a tu ritmo y sin caducidad.</p></div></li>
    </ol>
  </div>
</section>
</div>
<script>
(function () {
  // The course in Whop
  var COURSE_URL = 'https://whop.com/judithcalzadaduaigues-1bce/confianza-sin-permiso-66/';
  var go = document.querySelector('[data-course]');
  if (go && COURSE_URL) { go.querySelector('a').href = COURSE_URL; go.hidden = false; }
  // Whop returns here with ?status=failed|canceled when an off-site payment step did not go through
  var status = new URLSearchParams(location.search).get('status');
  if (status !== 'failed' && status !== 'canceled') return;
  var SALES_URL = '/#checkout'; // the sales page, at its checkout (change '/' if the sales page has its own path)
  var box = document.querySelector('.thanks');
  if (!box) return;
  box.querySelector('.intro').innerHTML = '<h1>El pago no se ha <em>completado.</em></h1>' +
    '<p>Puedes volver e intentarlo de nuevo con el mismo u otro método de pago.</p>' +
    '<p class="cta"><a class="btn" href="' + SALES_URL + '">Volver al pago</a></p>';
  var list = box.querySelector('.thanks-list');
  if (list) list.remove();
})();
</script>
'''
pie = (sec_dir / f'{len(SLUGS) + 2:02d}-pie.html').read_text()
import shutil
shutil.rmtree(OUT / 'pago', ignore_errors=True)  # the checkout now lives on the sales page
for step, middle in (('gracias', gracias),):
    d = OUT / step; d.mkdir(exist_ok=True)
    for f in d.glob('*.html'): f.unlink()
    (d / '01-cabecera.html').write_text(simple_header)
    (d / f'02-{step}.html').write_text(middle)
    (d / '03-pie.html').write_text(pie)
print('gracias step written')


# ---------- Legal steps: aviso-legal, privacidad, cookies ----------
legal_header = simple_header.replace('<span class="name">Judith Calzada</span>', '<a class="name" href="/">Judith Calzada</a>')
_tb = footer[footer.index('var TITULAR = {'):]; _tb = _tb[:_tb.index('};')]
TITULAR = dict(re.findall(r"(\w+): '([^']*)'", _tb))
for slug in LEGAL:
    page = (SRC / f'{slug}.html').read_text()
    sec = page[page.index('<section class="legal">'):page.index('</main>')].rstrip()
    d = OUT / 'legal' / slug; d.mkdir(parents=True, exist_ok=True)
    for f in d.glob('*.html'): f.unlink()
    (d / '01-cabecera.html').write_text(legal_header)
    # Write Judith's details (TITULAR in the footer script) straight into the page, so they show without the script
    for key, val in TITULAR.items():
        if not val: continue
        tag = f'<a data-t="{key}" href="#"></a>' if key == 'email' else None
        if tag and tag in sec: sec = sec.replace(tag, f'<a data-t="{key}" href="mailto:{val}">{val}</a>')
        sec = re.sub(rf'<dd data-t="{key}">[^<]*</dd>', f'<dd data-t="{key}">{val}</dd>', sec)
        sec = re.sub(rf'<div data-t-row hidden>(<dt>[^<]*</dt>(?:<dd>)?<(?:dd|a) data-t="{key}")', r'<div data-t-row>\1', sec)
    (d / f'02-{slug}.html').write_text(f'<div class="jc">\n{ghl_links(sec)}\n</div>\n')
    (d / '03-pie.html').write_text(pie)
print('legal steps written:', *LEGAL)
