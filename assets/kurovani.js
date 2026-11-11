// Kurovani — interactions du thème
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hover = matchMedia('(hover: hover)').matches;
  const T = window.KV || {};

  // Message court en bas d'écran
  const toast = $('#toast'); let tt;
  const say = m => { if (!toast) return; toast.textContent = m; toast.classList.add('on'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('on'), 2600); };

  // Pièce maîtresse : rotation au glisser, puis calage sur la face la plus proche
  $$('.stage').forEach(stage => {
    const spin = $('.spinner', stage), bF = $('[data-turn="front"]', stage), bB = $('[data-turn="back"]', stage);
    if (!spin) return;
    let ry = -22, startX = 0, startRy = 0, dragging = false;
    const apply = () => spin.style.setProperty('--ry', ry + 'deg');
    const sideOf = a => { const n = ((a % 360) + 360) % 360; return n > 90 && n < 270 ? 'back' : 'front'; };
    const mark = () => { const s = sideOf(ry); stage.dataset.side = s; bF && bF.setAttribute('aria-pressed', s === 'front'); bB && bB.setAttribute('aria-pressed', s === 'back'); };
    const snap = side => { const off = side === 'back' ? 180 : 0; ry = Math.round((ry - off) / 360) * 360 + off + (side === 'back' ? 18 : -22); apply(); mark(); };
    stage.addEventListener('pointerdown', e => { if (e.target.closest('button, a')) return; dragging = true; startX = e.clientX; startRy = ry; stage.classList.add('drag'); stage.setPointerCapture(e.pointerId); });
    stage.addEventListener('pointermove', e => { if (!dragging) return; ry = startRy + (e.clientX - startX) * .6; apply(); mark(); });
    const end = () => { if (!dragging) return; dragging = false; stage.classList.remove('drag'); snap(sideOf(ry)); };
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    bF && bF.addEventListener('click', () => snap('front')); bB && bB.addEventListener('click', () => snap('back'));
    apply();
  });

  // Visuels produit : inclinaison au pointeur + retournement face / dos
  $$('.shot').forEach(shot => {
    const flip = $('.flip', shot), btn = $('.side', shot);
    if (!flip) return;
    btn && btn.addEventListener('click', e => {
      e.preventDefault();
      const on = btn.getAttribute('aria-pressed') !== 'true';
      btn.setAttribute('aria-pressed', on); btn.textContent = on ? btn.dataset.front : btn.dataset.back;
      flip.style.setProperty('--turn', on ? '180deg' : '0deg');
    });
    if (calm || !hover) return;
    shot.addEventListener('pointermove', e => { const r = shot.getBoundingClientRect(); shot.classList.add('live'); flip.style.setProperty('--mx', ((e.clientX - r.left) / r.width - .5).toFixed(3)); flip.style.setProperty('--my', ((e.clientY - r.top) / r.height - .5).toFixed(3)); });
    shot.addEventListener('pointerleave', () => { shot.classList.remove('live'); flip.style.setProperty('--mx', 0); flip.style.setProperty('--my', 0); });
  });

  // Affiche : légère rotation au pointeur
  $$('.frame').forEach(fr => {
    if (calm || !hover) return;
    fr.addEventListener('pointermove', e => { const r = fr.getBoundingClientRect(); fr.classList.add('live'); fr.style.setProperty('--mx', ((e.clientX - r.left) / r.width - .5).toFixed(3)); fr.style.setProperty('--my', ((e.clientY - r.top) / r.height - .5).toFixed(3)); });
    fr.addEventListener('pointerleave', () => { fr.classList.remove('live'); fr.style.setProperty('--mx', 0); fr.style.setProperty('--my', 0); });
  });

  // Filtre des pièces (section d'accueil)
  $$('[data-piece-filter]').forEach(seg => seg.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    $$('button', seg).forEach(x => x.setAttribute('aria-pressed', x === b));
    $$('.piece', seg.closest('section')).forEach(p => p.hidden = b.dataset.f !== 'all' && p.dataset.t !== b.dataset.f);
  }));

  // Guide des tailles : colonne surlignée
  $$('[data-size-guide]').forEach(box => {
    const pick = $('.seg', box), table = $('table', box); if (!pick || !table) return;
    const hl = i => $$('tr', table).forEach(tr => [...tr.children].forEach((c, j) => c.classList.toggle('hl', j === i)));
    pick.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const bs = $$('button', pick); bs.forEach(x => x.setAttribute('aria-pressed', x === b)); hl(bs.indexOf(b) + 1); });
    const cur = $$('button', pick).findIndex(b => b.getAttribute('aria-pressed') === 'true'); if (cur >= 0) hl(cur + 1);
  });

  // Fiche produit : miniatures
  $$('.thumbs').forEach(th => th.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    $$('button', th).forEach(x => x.setAttribute('aria-pressed', x === b));
    const main = $('#pdp-main'); if (main) { main.src = b.dataset.src; main.srcset = ''; }
    const flip = $('.pdp .flip'); if (flip) flip.style.setProperty('--turn', '0deg');
  }));

  // Fiche produit : la combinaison d'options choisit la variante
  $$('form[data-variants]').forEach(form => {
    let variants = []; try { variants = JSON.parse($('script[type="application/json"]', form).textContent); } catch (e) {}
    const id = $('input[name="id"]', form), btn = $('button[type="submit"]', form), price = $('[data-price]', form.closest('.info') || document);
    const sync = () => {
      const opts = $$('fieldset.opt', form).map(f => { const c = $('input:checked', f); return c ? c.value : null; });
      const v = variants.find(v => v.options.every((o, i) => o === opts[i]));
      if (!v) { btn.disabled = true; btn.textContent = T.unavailable || 'Indisponible'; return; }
      id.value = v.id; btn.disabled = !v.available; btn.textContent = v.available ? (T.add || 'Ajouter au panier') : (T.soldout || 'Épuisé');
      if (price && v.price_html) price.innerHTML = v.price_html;
    };
    form.addEventListener('change', sync); if (variants.length) sync();
  });

  // Ajout au panier sans quitter la page
  $$('form[action$="/cart/add"]').forEach(form => form.addEventListener('submit', async e => {
    const needs = $$('[data-size-required]', form);
    if (needs.length && !$('input[name="id"]:checked', form)) { e.preventDefault(); say(T.pick || 'Choisis une taille avant d’ajouter'); return; }
    if (!window.fetch) return;
    e.preventDefault();
    const btn = $('button[type="submit"]', form); btn.disabled = true;
    try {
      const res = await fetch((T.root || '/') + 'cart/add.js', { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.description || data.message);
      const cart = await (await fetch((T.root || '/') + 'cart.js')).json();
      $$('[data-cart-count]').forEach(n => n.textContent = cart.item_count);
      const bag = $('.bag'); if (bag) { bag.classList.remove('bump'); void bag.offsetWidth; bag.classList.add('bump'); }
      say(data.title ? `${data.title} : ${T.added || 'ajouté au panier'}` : (T.added || 'Ajouté au panier'));
    } catch (err) { say(err.message || (T.error || 'Ajout impossible, réessaie')); }
    btn.disabled = false;
  }));

  // Collection : le tri recharge la page avec le bon paramètre
  $$('select[data-sort]').forEach(sel => sel.addEventListener('change', () => { const u = new URL(location.href); u.searchParams.set('sort_by', sel.value); u.searchParams.delete('page'); location.href = u.toString(); }));
})();
