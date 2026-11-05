# Tarea: lista de espera del «Intensivo de la Confianza» en GoHighLevel (GHL)

Trabaja en mi cuenta de GoHighLevel, en el funnel **«Test Marta»** (página de ventas de Judith Calzada). Usa el navegador (Chrome) de mi ordenador. Haz los pasos en orden, comprueba cada uno con una captura y al final dame un resumen de lo que has hecho y de lo que no hayas podido hacer.

**Reglas:**
- No cambies ninguna otra sección de la página, ni dominios, ni ajustes de la cuenta.
- No borres nada que no se mencione aquí.
- Si un menú no se llama exactamente como digo, busca el equivalente y dímelo.
- Antes de **publicar el workflow**, enséñame cómo ha quedado y espera mi OK.

## Paso 1 · Crear el formulario
Sites → Forms → Builder → **+ Add Form** → nombre: `Lista de espera · Intensivo de la Confianza`.

Campos, en este orden. **Borra todos los demás**, incluidas las dos casillas por defecto de SMS en inglés («[BUSINESS NAME]… Text HELP… reply STOP»):

| Campo | Etiqueta | Placeholder | Obligatorio |
|---|---|---|---|
| Full Name | `Nombre completo` | `Tu nombre y apellidos` | Sí |
| Phone | `Teléfono móvil` | `600 000 000` | Sí, país por defecto **España (+34)** |
| Email | `Email` | `tu@email.com` | Sí |
| Checkbox / Terms & Conditions | (sin etiqueta) | `Acepto la política de privacidad y que Judith Calzada me escriba por email sobre el Intensivo de la Confianza.` | **Sí** |
| Checkbox | (sin etiqueta) | `Quiero recibir también avisos por SMS o WhatsApp sobre el Intensivo. Puedo darme de baja cuando quiera.` | No |

Ajustes del formulario:
- **Botón:** texto `Unirme a la lista de espera`, color `#5d0018`.
- **Al enviar:** mostrar el mensaje `¡Ya estás en la lista! Te escribiré en cuanto abran las plazas.`
- **Estilo:** fondo transparente, sin borde ni sombra, ancho completo.
- **Enlaces «Privacy Policy | Terms of Service»** del pie del formulario: si se pueden editar, apúntalos a https://sites.leadconnectorhq.com/preview/ZfjXAtHTgjp0tmcPc56W (privacidad) y https://sites.leadconnectorhq.com/preview/6lP5PHsxGXzSwwL30aFo (aviso legal). Si no, desactívalos.

Styles → **Custom CSS**, pega esto tal cual:

```css
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,500;1,400&display=swap');
html, body, form, #_builder-form, [class*="form-builder"], .ghl-form-wrap { background: transparent !important; box-shadow: none !important; border: 0 !important; font-family: 'PP Neue Montreal', 'Helvetica Neue', Helvetica, Arial, sans-serif !important; color: #1d1b26 !important; }
form, #_builder-form { padding: 0 8px !important; max-width: none !important; }
label, .label-alignment, .form-field-label { font-size: 13px !important; font-weight: 500 !important; letter-spacing: .08em !important; text-transform: uppercase !important; color: #4f4c58 !important; margin-bottom: 6px !important; }
input[type="text"], input[type="email"], input[type="tel"], input[type="number"], textarea, select, .form-control { font: 16px/1.4 'Helvetica Neue', Helvetica, Arial, sans-serif !important; color: #1d1b26 !important; background: #fff !important; border: 1px solid rgba(29,27,38,.14) !important; border-radius: 2px !important; padding: 14px 16px !important; height: auto !important; box-shadow: none !important; transition: border-color .2s, box-shadow .2s !important; }
input::placeholder, textarea::placeholder { color: #9a96a0 !important; }
input:focus, textarea:focus, select:focus, .form-control:focus { outline: 0 !important; border-color: #5d0018 !important; box-shadow: 0 0 0 3px rgba(93,0,24,.12) !important; }
.iti__selected-flag, .vti__dropdown, .phone-input .country-code { background: #fff !important; border-radius: 2px 0 0 2px !important; }
input[type="checkbox"] { accent-color: #5d0018 !important; width: 16px !important; height: 16px !important; margin-top: 3px !important; }
.checkbox-container label, .option label, label[for*="checkbox"], .terms-and-conditions, .tnc-text { font-size: 14px !important; line-height: 1.5 !important; letter-spacing: 0 !important; text-transform: none !important; font-weight: 400 !important; color: #4f4c58 !important; }
a { color: #5d0018 !important; }
a:hover { color: #430011 !important; }
button[type="submit"], .btn, .button-element, .ghl-btn { width: 100% !important; background: #5d0018 !important; border: 1px solid #5d0018 !important; border-radius: 2px !important; color: #fff !important; font: 500 13px/1 'Helvetica Neue', Helvetica, Arial, sans-serif !important; letter-spacing: .16em !important; text-transform: uppercase !important; padding: 18px 24px !important; box-shadow: none !important; cursor: pointer !important; transition: background .25s, transform .25s !important; }
button[type="submit"]:hover, .btn:hover, .button-element:hover { background: #430011 !important; transform: translateY(-1px) !important; }
button[type="submit"]::after { content: "  →"; }
.thank-you-message, .form-success, [class*="thank"] { font-family: 'EB Garamond', Garamond, serif !important; font-style: italic !important; font-size: 22px !important; color: #1d1b26 !important; text-align: center !important; }
.form-builder--item, .form-field-wrapper { margin-bottom: 14px !important; }
```

Guarda y haz una captura de la vista previa del formulario.

## Paso 2 · Copiar el código de inserción
Integrate → **Embed**: copia el código completo (iframe + script).

## Paso 3 · Pegar el formulario en la página
Funnel **Test Marta** → página de ventas → **Edit page**. Busca la sección del precio (la granate con «¿Vas a seguir esperando a sentirte preparada?» y la tarjeta «Intensivo de la Confianza»). Abre su elemento **Custom JS/HTML**, borra todo y pega el bloque de abajo. Después **sustituye la línea que empieza por `<!-- PEGA AQUÍ` por el código de inserción del Paso 2**. Guarda la página.

```html
<div class="jc">
  <section class="final" id="precios">
    <style>
      .final .offer .price.soon{font-style:italic;font-size:52px;margin:14px 0 10px}
      .cd{display:flex;justify-content:center;gap:10px;margin:6px 0 18px}
      .cd div{min-width:64px;padding:10px 6px 8px;border:1px solid var(--line);background:#fff;text-align:center}
      .cd b{display:block;font-family:var(--serif);font-weight:500;font-size:34px;line-height:1;color:var(--ink);font-variant-numeric:tabular-nums}
      .cd span{display:block;margin-top:6px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
      .final .wrap .offer p.cd-label{margin:0 0 4px;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:600}
      .waitlist{text-align:left}
      .waitlist .btn{width:100%}
      .wl-embed{margin:6px -8px 0}
      .wl-embed iframe{display:block;width:100%;min-height:420px;border:0}
      .final .wrap .waitlist p.wl-msg{margin:10px 0 0;font-size:14px;color:#b3261e;text-align:center}
      @media (max-width:760px){.cd{gap:6px}.cd div{min-width:0;flex:1}.cd b{font-size:28px}.final .offer .price.soon{font-size:44px}}
    </style>
    <div class="wrap">
      <h2>¿Vas a seguir esperando a <em>sentirte preparada?</em></h2>
      <div class="buy solo">
        <div class="offer">
          <img class="offer-img" src="https://davidcohencontent-create.github.io/coding-test/funnel/img/dia-bloqueado.jpg" alt="" loading="lazy">
          <h3>Intensivo de la Confianza</h3>
          <p class="price soon">Próximamente</p>
          <div class="countdown" data-open="2026-11-26T00:00:00+01:00">
            <p class="cd-label">Las plazas se abren en</p>
            <div class="cd" aria-live="off">
              <div><b data-u="d">21</b><span>días</span></div>
              <div><b data-u="h">00</b><span>horas</span></div>
              <div><b data-u="m">00</b><span>min</span></div>
              <div><b data-u="s">00</b><span>seg</span></div>
            </div>
          </div>
          <p class="offer-line">Únete a la lista de espera y serás la primera en saber cuándo abren las plazas.</p>
          <ul class="offer-list">
            <li>10 días de vídeos · 11 lecciones grabadas</li>
            <li>Meditaciones guiadas</li>
            <li>Llamadas grupales con Judith</li>
            <li>A tu ritmo y sin caducidad</li>
          </ul>
          <div class="waitlist">
            <button class="btn" type="button" data-wl-open>Unirme a la lista de espera</button>
            <div class="wl-embed" id="lista-espera" hidden>
              <!-- PEGA AQUÍ el código de inserción del formulario de GHL (sustituye esta línea entera) -->
            </div>
            <p class="wl-msg" hidden>Falta pegar aquí el código del formulario de GHL.</p>
          </div>
        </div>
      </div>
      <div class="also full">
        <p><strong>Con Judith</strong> Todo el curso, más acceso directo a Judith y llamadas semanales. <span class="badge-full">Plazas completas</span></p>
        <span class="btn sm is-disabled" aria-disabled="true">Completo</span>
      </div>
    </div>
    <script>
    (function () {
      // Countdown to the opening date; when it is reached it says the places are open
      var box = document.querySelector('.countdown');
      if (box && !box.dataset.run) {
        box.dataset.run = '1';
        var end = new Date(box.dataset.open).getTime(), pad = function (n) { return (n < 10 ? '0' : '') + n; };
        var tick = function () {
          var t = Math.max(0, end - Date.now()), s = Math.floor(t / 1000);
          box.querySelector('[data-u=d]').textContent = Math.floor(s / 86400);
          box.querySelector('[data-u=h]').textContent = pad(Math.floor(s % 86400 / 3600));
          box.querySelector('[data-u=m]').textContent = pad(Math.floor(s % 3600 / 60));
          box.querySelector('[data-u=s]').textContent = pad(s % 60);
          if (t <= 0) { box.querySelector('.cd-label').textContent = '¡Las plazas ya están abiertas!'; box.querySelector('.cd').hidden = true; return; }
          setTimeout(tick, 1000 - Date.now() % 1000);
        };
        tick();
      }
      // Waiting list: the button opens the GHL form embedded below it (GHL saves the contact; a workflow adds the opportunity)
      var open = document.querySelector('[data-wl-open]');
      if (!open || open.dataset.ready) return;
      open.dataset.ready = '1';
      open.addEventListener('click', function () {
        var box = document.getElementById('lista-espera');
        if (!box.querySelector('iframe, form')) { box.parentNode.querySelector('.wl-msg').hidden = false; return; }
        box.hidden = false; open.hidden = true;
        box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    })();
    </script>
  </section>
</div>

```

## Paso 4 · Pipeline
Opportunities → Pipelines → **+ Create**:
- Nombre: `Intensivo de la Confianza`
- Etapas: `Lista de espera`, `Contactada`, `Inscrita`, `No interesada`.

## Paso 5 · Workflow (gratuito, sin webhook)
Automation → Workflows → **+ Create Workflow → Start from scratch** → nombre `Lista de espera · Intensivo`.
- **Trigger:** Form Submitted, filtrado por el formulario «Lista de espera · Intensivo de la Confianza».
- **Acción 1:** Add Contact Tag → `lista-espera-intensivo`
- **Acción 2:** Create/Update Opportunity:
  - Pipeline `Intensivo de la Confianza`, etapa `Lista de espera`
  - Nombre `{{contact.first_name}} · Intensivo`, estado Open
  - Sin oportunidades duplicadas.

Guarda. **Enséñame el workflow y espera mi OK antes de publicarlo.**

## Paso 6 · Prueba
1. Abre la vista previa de la página en una ventana de incógnito y baja hasta el precio. Pulsa «Unirme a la lista de espera»: el formulario debe aparecer dentro de la tarjeta, con el estilo de la página (campos cuadrados, botón granate).
2. Rellénalo con: nombre `Prueba Lista Espera`, móvil `600000000`, email `prueba+listaespera@example.com`, primera casilla marcada. Envía.
3. Comprueba en Contacts el contacto con la etiqueta `lista-espera-intensivo`, y en Opportunities → Intensivo de la Confianza → Lista de espera su tarjeta.
4. Haz capturas de la página con el formulario, del contacto y de la oportunidad.
5. Borra después el contacto de prueba.

Si algo del formulario no coge el estilo (por ejemplo el botón sigue azul), haz una captura y dime qué parte es, para ajustar el CSS.
