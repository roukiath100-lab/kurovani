// Kurovani — défilé de looks (section lookbook)
(() => {
  const root = document.querySelector('[data-lookbook]'); if (!root) return;
  const $ = (s, r = root) => r.querySelector(s), $$ = (s, r = root) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const T = Object.assign({}, window.KV, window.KVLook);
  const lineup = $('[data-lb-lineup]'), ticks = $('[data-lb-ticks]'), figs = $$('.lb-fig'), items = $$('.lb-item');
  const N = figs.length; if (!N) return;
  const pad = i => String(i + 1).padStart(2, '0');
  const jitter = [0, .22, .08, .26, .12, .2, .1, .24];
  // Position des repères sur la silhouette : 1 = haut, 2 = bas, puis les suivants
  const DOTS = { front: [[50, 41], [38, 70], [62, 30], [50, 95]], back: [[26, 34], [40, 72], [62, 30], [50, 95]] };

  figs.forEach((f, i) => {
    items.forEach((it, k) => {
      const d = (DOTS[f.dataset.view] || DOTS.front)[k]; if (!d) return;
      const s = document.createElement('span');
      s.className = 'lb-dot'; s.dataset.piece = it.dataset.piece; s.textContent = k + 1;
      s.style.left = d[0] + '%'; s.style.top = d[1] + '%';
      f.appendChild(s);
    });
    const t = document.createElement('button');
    t.type = 'button'; t.className = 'lb-tick';
    t.innerHTML = `${pad(i)}<i></i><span></span>`; t.lastChild.textContent = f.dataset.name;
    t.setAttribute('aria-label', f.getAttribute('aria-label'));
    t.addEventListener('click', () => go(i, true));
    ticks.appendChild(t);
  });
  const tickEls = [...ticks.children];

  let cam = calm ? 0 : -1.6, target = 0, active = -1, focus = false, zoom = 1, zoomT = 1, auto = !calm, moved = 0;
  const half = Math.max(N / 2, 1);
  const wrap = v => N < 2 ? 0 : ((v + N / 2) % N + N) % N - N / 2;
  const idx = () => ((Math.round(target) % N) + N) % N;

  function layout() {
    const w = lineup.clientWidth, mobile = matchMedia('(max-width: 900px)').matches;
    const S = Math.max(130, Math.min(300, w * (mobile ? .46 : .235)));
    figs.forEach((f, i) => {
      const p = wrap(i - cam), a = Math.abs(p), on = i === active;
      const d = Math.min(1, a / 2.4 + (a > .35 ? jitter[i % jitter.length] : 0));
      const sc = (1 - .34 * d) * (on ? zoom : 1);
      const x = p * S * (1 - .1 * a);
      f.style.transform = `translate(calc(-50% + ${x.toFixed(1)}px), ${(-d * 5).toFixed(2)}%) scale(${sc.toFixed(4)})`;
      f.style.filter = d > .04 ? `blur(${(d * d * 6).toFixed(2)}px)` : 'none';
      f.style.opacity = N > 2 && a > half - .6 ? Math.max(0, (half - a) / .6).toFixed(2) : (1 - .45 * d).toFixed(2);
      f.style.zIndex = 100 - Math.round(d * 40);
    });
  }
  function frame() {
    cam += (target - cam) * (lineup.classList.contains('lb-drag') ? .35 : .09);
    zoom += (zoomT - zoom) * .1;
    layout();
    requestAnimationFrame(frame);
  }
  function setActive() {
    const i = idx(); if (i === active) return; active = i;
    figs.forEach((f, k) => f.classList.toggle('lb-on', k === i));
    tickEls.forEach((t, k) => t.setAttribute('aria-current', k === i));
    $('[data-lb-n]').textContent = 'Look ' + pad(i); $('[data-lb-name]').textContent = figs[i].dataset.name;
    const v = figs[i].dataset.view === 'back' ? 'back' : 'front';
    $$('.lb-th img').forEach(img => { const src = img.dataset[v]; if (src && img.getAttribute('src') !== src) img.src = src; });
  }
  function go(i, user) { if (user) auto = false; target = Math.round(target) + wrap(i - idx()); setActive(); }
  function step(d) { auto = false; target = Math.round(target) + d; setActive(); }
  const clearHot = () => $$('.lb-hot').forEach(e => e.classList.remove('lb-hot'));
  const hot = id => { clearHot(); $$(`[data-piece="${id}"]`).forEach(e => e.classList.add('lb-hot')); };
  function setFocus(v) { focus = v; root.classList.toggle('lb-focus', v); zoomT = v ? 1.1 : 1; if (v) auto = false; else clearHot(); }

  let sx = 0, st = 0, down = false;
  lineup.addEventListener('pointerdown', e => { if (e.target.closest('.lb-close, .lb-dot') || focus) return; down = true; moved = 0; sx = e.clientX; st = target; });
  addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); if (moved > 6) { lineup.classList.add('lb-drag'); auto = false; target = st - dx / (lineup.clientWidth * .235); } });
  addEventListener('pointerup', () => { if (!down) return; down = false; lineup.classList.remove('lb-drag'); target = Math.round(target); setActive(); });
  figs.forEach((f, i) => f.addEventListener('click', e => {
    if (moved > 6) return;
    const dot = e.target.closest('.lb-dot'); if (dot) { hot(dot.dataset.piece); return; }
    if (focus) return;
    go(i, true); setFocus(true);
  }));
  $('[data-lb-close]').addEventListener('click', () => setFocus(false));
  $('[data-lb-prev]').addEventListener('click', () => step(-1)); $('[data-lb-next]').addEventListener('click', () => step(1));
  let wheelLock = 0;
  lineup.addEventListener('wheel', e => { if (Math.abs(e.deltaX) > Math.abs(e.deltaY) && Math.abs(e.deltaX) > 12 && !focus) { e.preventDefault(); if (!wheelLock) { step(e.deltaX > 0 ? 1 : -1); wheelLock = setTimeout(() => wheelLock = 0, 380); } } }, { passive: false });
  document.addEventListener('keydown', e => {
    if (e.target.closest('input, textarea, select') || document.querySelector('.lbx.on')) return;
    if (e.key === 'Escape') setFocus(false);
    if (e.key === 'ArrowLeft') step(-1); if (e.key === 'ArrowRight') step(1);
  });
  if (N > 1) setInterval(() => { if (auto && !focus && !down && document.visibilityState === 'visible') { target = Math.round(target) + 1; setActive(); } }, 3600);

  // ---- Pièces : taille, ajout au panier Shopify
  const toast = document.getElementById('toast'); let tt;
  const say = m => { if (!toast) return; toast.textContent = m; toast.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('on'), 2600); };
  const variantOf = it => { const h = $('[data-lb-variant]', it); if (h) return h.hasAttribute('data-soldout') ? null : h.value; const b = $('.lb-szs [aria-pressed="true"]:not([disabled])', it); return b ? b.dataset.variant : null; };
  async function add(list, msg) {
    const ids = list.map(variantOf).filter(Boolean);
    if (!ids.length) { say(T.pick || 'Choisis une taille disponible'); return; }
    try {
      const base = T.root || '/';
      const res = await fetch(base + 'cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ items: ids.map(id => ({ id: +id, quantity: 1 })) }) });
      const data = await res.json(); if (!res.ok) throw new Error(data.description || data.message);
      const cart = await (await fetch(base + 'cart.js')).json();
      document.querySelectorAll('[data-cart-count]').forEach(n => n.textContent = cart.item_count);
      const bag = document.querySelector('.bag'); if (bag) { bag.classList.remove('bump'); void bag.offsetWidth; bag.classList.add('bump'); }
      say(msg || T.added || 'Ajouté au panier');
    } catch (err) { say(err.message || T.error || 'Ajout impossible, réessaie'); }
  }
  items.forEach(it => {
    it.addEventListener('click', e => {
      const s = e.target.closest('[data-variant]');
      if (s) $$('[data-variant]', it).forEach(b => b.setAttribute('aria-pressed', b === s));
      if (e.target.closest('[data-lb-add]')) add([it], $('h3', it).textContent.trim() + ' : ' + (T.added || 'ajouté au panier'));
    });
    it.addEventListener('pointerenter', () => { if (focus) hot(it.dataset.piece); });
  });
  const full = $('[data-lb-addfull]'); if (full) full.addEventListener('click', () => add(items, T.addedFull));

  setActive(); frame();
})();
