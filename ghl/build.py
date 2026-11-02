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
body = html[html.index('<header>'):html.index('<script')]
header = body[:body.index('</header>') + 9]
main = body[body.index('<main id="top">') + len('<main id="top">'):body.index('</main>')]
footer = body[body.index('<footer>'):body.index('</footer>') + 9]

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
