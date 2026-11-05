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

# ---------- Paste guide: every block in paste order with a Copy button, plus a live preview built from the same code ----------
import html as _html
steps = [
    ('Ajustes · Tracking Code · Header', 'Settings → Tracking Code → Header. Una vez, en cada paso del funnel.', (OUT / '1-head-code.html').read_text()),
    ('Ajustes · Custom CSS', 'Settings → Custom CSS. Una vez, en cada paso del funnel.', (OUT / '2-custom-css.css').read_text()),
    ('Ajustes · Tracking Code · Footer', 'Settings → Tracking Code → Footer. Solo en la página de ventas.', (OUT / '3-footer-code.html').read_text()),
]
LABELS = {'cabecera': 'Cabecera (activa “Sticky” en esta sección)', 'hero': 'Vídeo y titular', 'esto-es-para-ti': 'Esto es para ti si…',
          'yo-me-sentia-igual': 'Yo me sentía igual', 'programa-10-dias': 'Lo que trabajamos en 10 días',
          'herramientas': 'Herramientas', 'resenas-y-logos': 'Reseñas y logos', 'dos-caminos': 'Dos caminos',
          'mi-historia': 'Mi historia', 'precios': 'Precio / lista de espera', 'faq': 'Preguntas frecuentes', 'pie': 'Pie de página'}
for name in names:
    slug = name[3:-5]
    note = 'Sección a ancho completo, padding 0, sin fondo · fila de 1 columna, padding 0 · elemento Custom JS/HTML.'
    if slug == 'precios':
        note += ' Justo después, añade una sección con un Form (nombre + email) y pon su ID en “lista-espera”: ahí lleva el botón de la lista de espera.'
    steps.append((LABELS.get(slug, slug), note, (OUT / 'sections' / name).read_text()))

def block(i, title, note, code):
    return (f'<section class="step" id="s{i}"><header><span class="n">{i:02d}</span><div><h2>{_html.escape(title)}</h2>'
            f'<p>{_html.escape(note)}</p></div><button type="button" class="copy" data-for="c{i}">Copiar</button></header>'
            f'<textarea id="c{i}" spellcheck="false">{_html.escape(code)}</textarea></section>')
nav = ''.join(f'<a href="#s{i}"><span>{i:02d}</span>{_html.escape(t)}</a>' for i, (t, _, _) in enumerate(steps, 1))
body = ''.join(block(i, *s) for i, s in enumerate(steps, 1))
guide = '''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guía de pegado GHL</title>
<style>
:root{--bg:#f6f5f3;--card:#fff;--ink:#1d1b26;--muted:#6b6874;--line:#e6e3df;--accent:#5d0018;--code:#faf9f7}
@media (prefers-color-scheme:dark){:root{--bg:#141318;--card:#1d1c23;--ink:#eceaf0;--muted:#a19fa8;--line:#2d2b34;--accent:#e7a3b3;--code:#17161c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;background:var(--card);border-bottom:1px solid var(--line)}
.top h1{font-size:16px;margin:0}
.hint{color:var(--muted);font-size:13px;margin-right:auto}
.tabs button{font:inherit;padding:8px 14px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:999px;cursor:pointer}
.tabs button[aria-selected=true]{background:var(--accent);border-color:var(--accent);color:#fff}
.wrap{display:grid;grid-template-columns:260px minmax(0,1fr);gap:20px;max-width:1200px;margin:0 auto;padding:20px 16px}
nav{position:sticky;top:70px;align-self:start;display:grid;gap:2px;max-height:calc(100vh - 90px);overflow:auto}
nav a{display:flex;gap:10px;padding:7px 10px;border-radius:8px;color:var(--ink);text-decoration:none;font-size:14px}
nav a:hover{background:var(--card)}nav a span{color:var(--muted);font-variant-numeric:tabular-nums}
.step{background:var(--card);border:1px solid var(--line);border-radius:14px;margin-bottom:16px;overflow:hidden;scroll-margin-top:80px}
.step header{display:flex;gap:14px;align-items:flex-start;padding:14px 16px}
.step .n{flex:none;font-weight:600;color:var(--accent);font-variant-numeric:tabular-nums}
.step h2{font-size:16px;margin:0}.step p{margin:4px 0 0;color:var(--muted);font-size:14px}
.step header div{flex:1;min-width:0}
.copy{flex:none;font:inherit;font-weight:600;padding:8px 16px;border:0;border-radius:999px;background:var(--accent);color:#fff;cursor:pointer}
.copy.ok{background:#2f7d4f}
textarea{display:block;width:100%;height:180px;margin:0;padding:12px 16px;border:0;border-top:1px solid var(--line);background:var(--code);color:var(--ink);
  font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;resize:vertical;white-space:pre;overflow:auto}
#preview{display:none;padding:12px 16px}#preview .bar{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
#preview .bar button{font:inherit;padding:6px 12px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;cursor:pointer}
#preview .bar button[aria-pressed=true]{border-color:var(--accent);color:var(--accent);font-weight:600}
#frame{display:block;margin:0 auto;width:100%;height:calc(100vh - 140px);border:1px solid var(--line);border-radius:12px;background:#fff;transition:width .3s}
body.pv .wrap{display:none}body.pv #preview{display:block}
@media (max-width:760px){.wrap{grid-template-columns:1fr}nav{display:none}}
</style></head><body>
<div class="top"><h1>Guía de pegado · Curso de Confianza</h1>
<span class="hint">Puedes editar el código aquí; la vista previa usa lo que haya en cada caja.</span>
<div class="tabs" role="tablist"><button role="tab" aria-selected="true" data-tab="code">Código en orden</button> <button role="tab" aria-selected="false" data-tab="pv">Vista previa</button></div></div>
<div class="wrap"><nav>''' + nav + '''</nav><main>''' + body + '''</main></div>
<div id="preview"><div class="bar"><button aria-pressed="true" data-w="100%">Escritorio</button><button aria-pressed="false" data-w="390px">Móvil</button><button data-reload>Recargar</button></div>
<iframe id="frame" title="Vista previa de la página"></iframe></div>
<script>
(function () {
  function copy(btn) {
    var ta = document.getElementById(btn.dataset.for);
    var done = function () { btn.textContent = 'Copiado ✓'; btn.classList.add('ok'); setTimeout(function () { btn.textContent = 'Copiar'; btn.classList.remove('ok'); }, 1600); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(ta.value).then(done, fallback); else fallback();
    function fallback() { ta.focus(); ta.select(); try { document.execCommand('copy'); done(); } catch (e) { btn.textContent = 'Selecciona y Ctrl+C'; } }
  }
  document.querySelectorAll('.copy').forEach(function (b) { b.addEventListener('click', function () { copy(b); }); });
  var frame = document.getElementById('frame'), built = false;
  function build() {
    var v = function (i) { return document.getElementById('c' + i).value; };
    var n = document.querySelectorAll('.step').length, sections = '';
    for (var i = 4; i <= n; i++) sections += v(i) + '\\n';
    frame.srcdoc = '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
      v(1) + '<style>' + v(2) + '</style></head><body>' + sections + v(3) + '</body></html>';
    built = true;
  }
  document.querySelectorAll('[data-tab]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-tab]').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
      var pv = b.dataset.tab === 'pv'; document.body.classList.toggle('pv', pv);
      if (pv && !built) build();
    });
  });
  document.querySelectorAll('[data-w]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('[data-w]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      frame.style.width = b.dataset.w;
    });
  });
  document.querySelector('[data-reload]').addEventListener('click', build);
})();
</script></body></html>
'''
(OUT / 'guia-de-pegado.html').write_text(guide)
print('paste guide written: ghl/guia-de-pegado.html')
