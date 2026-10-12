// Plan data shared by checkout, upsell and thank-you pages. The plan comes from ?plan=…
const PLANS = {
  'esencial':   { name: 'Esencial',   price: 50,  material: false, sesion: false },
  'completo':   { name: 'Completo',   price: 97,  material: true,  sesion: false },
  'con-judith': { name: 'Con Judith', price: 225, material: true,  sesion: true  },
};
const planId = PLANS[new URLSearchParams(location.search).get('plan')] ? new URLSearchParams(location.search).get('plan') : 'completo';
const plan = PLANS[planId];
const $$ = sel => document.querySelectorAll(sel);
$$('[data-plan-name]').forEach(el => el.textContent = plan.name);
$$('[data-plan-price]').forEach(el => el.textContent = plan.price + ' €');
$$('[data-plan-id]').forEach(el => el.href = el.href.replace('PLAN', planId));
// Elements only shown when the plan includes them
$$('[data-if-material]').forEach(el => el.hidden = !plan.material);
$$('[data-if-sesion]').forEach(el => el.hidden = !plan.sesion);
$$('[data-if-not-material]').forEach(el => el.hidden = plan.material);
