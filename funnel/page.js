// Sales page behaviour: method steps unlock as you scroll, and the Day 1 trailer's timed preview.

// Method: each step lights up when it reaches the middle of the screen and stays unlocked.
// Without JS, or with reduced motion, every step is simply shown.
(() => {
  const steps = [...document.querySelectorAll('.unlock li')];
  const count = document.querySelector('[data-step]');
  const bar = document.querySelector('.progress .bar i');
  if (!steps.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('js-unlock');
  const show = i => {
    steps.forEach((s, j) => { if (j <= i) s.classList.add('on'); });
    count.textContent = String(i + 1).padStart(2, '0');
    bar.style.setProperty('--p', (i + 1) / steps.length);
  };
  steps[0].classList.add('on');
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) show(steps.indexOf(e.target));
  }), { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach(s => io.observe(s));
})();

// Trailer: plays for data-preview seconds, then pauses and shows the paywall.
// With only the placeholder (no <video> yet), the play button runs the countdown so the flow can be previewed.
(() => {
  const box = document.querySelector('.trailer[data-preview]');
  if (!box) return;
  const limit = Number(box.dataset.preview) || 60;
  const video = box.querySelector('video');
  const play = box.querySelector('.play');
  const timer = box.querySelector('.timer');
  const paywall = box.querySelector('.paywall');
  const fmt = s => Math.floor(s / 60) + ':' + String(Math.ceil(s) % 60).padStart(2, '0');
  const render = left => { timer.textContent = 'Vista previa · ' + fmt(Math.max(0, left)); };
  const lock = () => { if (video) video.pause(); play.hidden = true; paywall.hidden = false; render(0); };
  let elapsed = 0, tick = null;

  if (video) {
    video.addEventListener('timeupdate', () => {
      render(limit - video.currentTime);
      if (video.currentTime >= limit) lock();
    });
    video.addEventListener('seeking', () => { if (video.currentTime > limit) video.currentTime = limit; });
    video.addEventListener('pause', () => { if (paywall.hidden) play.hidden = false; });
  }
  play.addEventListener('click', () => {
    play.hidden = true;
    if (video) { video.play(); return; }
    tick = setInterval(() => { elapsed++; render(limit - elapsed); if (elapsed >= limit) { clearInterval(tick); lock(); } }, 1000);
  });
  // Closing Day 1 pauses the preview
  box.closest('details')?.addEventListener('toggle', e => {
    if (e.target.open || !paywall.hidden) return;
    if (video) video.pause();
    if (tick) { clearInterval(tick); tick = null; play.hidden = false; }
  });
})();
