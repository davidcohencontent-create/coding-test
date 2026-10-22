// Fade-up entrance as blocks scroll into view, staggered within each group.
// Skipped entirely for reduced motion or old browsers, so content is always visible without it.
(() => {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const groups = ['.intro > *', '.video', '.cta', 'section > .wrap > .label', 'section > .wrap > h2',
    '.method-head > *', '.about > *', '.row4 > *', '.days > *', '.cols > *', '.plans > *',
    '.faq > *', '.final .wrap > *', '.checkout > *', '.offer .wrap > *', '.next > *'];
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll(groups.join(',')).forEach(el => {
    const i = [...el.parentElement.children].indexOf(el);
    el.style.setProperty('--d', Math.min(i, 6) * 70 + 'ms');
    el.classList.add('reveal');
    io.observe(el);
  });
})();
