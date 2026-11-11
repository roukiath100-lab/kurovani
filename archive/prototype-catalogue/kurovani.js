// Kurovani — interactions (prototype + thème)
(() => {
  const root = document.documentElement;
  try { const t = localStorage.getItem('kv-theme'); if (t) root.dataset.theme = t; } catch (e) {}
  const header = document.querySelector('.site-header');
  const scrim = document.querySelector('.scrim');
  const filters = document.querySelector('.filters');
  const closeAll = () => {
    header?.classList.remove('menu-open');
    filters?.classList.remove('open');
    scrim?.classList.remove('on');
    document.body.style.overflow = '';
  };
  const open = (fn) => { fn(); scrim?.classList.add('on'); document.body.style.overflow = 'hidden'; };

  document.querySelector('.menu-toggle')?.addEventListener('click', () => open(() => header.classList.add('menu-open')));
  document.querySelector('.search-toggle')?.addEventListener('click', () => {
    header.classList.toggle('search-open');
    header.querySelector('.search input')?.focus();
  });
  document.querySelectorAll('.filter-open').forEach(b => b.addEventListener('click', () => open(() => filters.classList.add('open'))));
  document.querySelector('.filters-close')?.addEventListener('click', closeAll);
  scrim?.addEventListener('click', closeAll);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAll(); });

  // Sous-menus au toucher (mobile)
  document.querySelectorAll('.nav-item > button.nav-link').forEach(b => b.addEventListener('click', () => {
    const item = b.parentElement; const on = !item.classList.contains('open');
    item.classList.toggle('open', on); b.setAttribute('aria-expanded', on);
  }));

  // Groupes de puces à choix unique (tri) ou multiple (tailles, couleurs)
  document.querySelectorAll('[data-toggle-group]').forEach(group => {
    const single = group.dataset.toggleGroup === 'single';
    group.addEventListener('click', e => {
      const btn = e.target.closest('[aria-pressed]'); if (!btn) return;
      if (single) group.querySelectorAll('[aria-pressed]').forEach(b => b.setAttribute('aria-pressed', b === btn));
      else btn.setAttribute('aria-pressed', btn.getAttribute('aria-pressed') !== 'true');
    });
  });

  // Thème clair / sombre (sombre par défaut)
  document.querySelector('.theme-toggle')?.addEventListener('click', () => {
    const next = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.dataset.theme = next;
    try { localStorage.setItem('kv-theme', next); } catch (e) {}
  });
})();

// 3D : inclinaison et parallaxe qui suivent le pointeur
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const fine = matchMedia('(hover: hover)').matches;
  const track = (el, onMove, onLeave) => {
    let raf = 0;
    el.addEventListener('pointermove', e => {
      if (e.pointerType === 'touch') return;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const r = el.getBoundingClientRect();
        onMove((e.clientX - r.left) / r.width - .5, (e.clientY - r.top) / r.height - .5);
      });
    });
    el.addEventListener('pointerleave', () => { cancelAnimationFrame(raf); onLeave(); });
  };
  if (fine) {
    // Onglets de catégories
    document.querySelectorAll('.tab3d').forEach(el => track(el, (x, y) => {
      el.classList.add('tilting');
      el.style.setProperty('--ry', (x * 18).toFixed(2) + 'deg');
      el.style.setProperty('--rx', (-y * 16).toFixed(2) + 'deg');
    }, () => {
      el.classList.remove('tilting');
      el.style.setProperty('--ry', '0deg'); el.style.setProperty('--rx', '0deg');
    }));
    // Cartes produit, étapes, bandeau
    document.querySelectorAll('.card, .steps li, .collection-hero').forEach(el => track(el, (x, y) => {
      el.classList.add('tilting');
      el.style.setProperty('--mx', x.toFixed(3)); el.style.setProperty('--my', y.toFixed(3));
    }, () => {
      el.classList.remove('tilting');
      el.style.setProperty('--mx', 0); el.style.setProperty('--my', 0);
    }));
  }
  // Apparition en relief au défilement
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.card, .steps li').forEach((el, i) => {
      el.classList.add('reveal'); el.style.setProperty('--d', (i % 4) * 70 + 'ms'); io.observe(el);
    });
  }
})();
