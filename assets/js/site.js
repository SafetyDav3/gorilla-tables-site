/* Gorilla Tables — front-end
   Header, hero hotspot explorer, scroll reveal, FAQ, and the quick quote. The quick quote prices every
   choice with the real table engine (assets/js/engine.js) in a Web Worker, so the page never waits. */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const fmt = n => '$' + Math.round(n).toLocaleString('en-US');

  /* ---------- header ---------- */
  const hdr = $('#gft-hdr');
  if (hdr) {
    const onScroll = () => hdr.classList.toggle('gft-scrolled', scrollY > 10);
    addEventListener('scroll', onScroll, { passive: true }); onScroll();
    const burger = $('#gft-hdr-burger');
    if (burger) burger.addEventListener('click', () => {
      const open = hdr.classList.toggle('gft-hdr-open');
      burger.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    $$('.gft-hdr-mobile a', hdr).forEach(a => a.addEventListener('click', () => { hdr.classList.remove('gft-hdr-open'); document.body.style.overflow = ''; }));
  }

  /* ---------- hero: hotspots, feature panel, cursor light ---------- */
  const hero = $('#gft-stage');
  if (hero) {
    const FEATURES = [
      { title: 'A dead-flat, laser-cut top', pos: '84% 22%',
        text: ['1/4", 3/8" or 1/2" steel plate, laser-cut with 5/8" fixture holes on a precise grid. Flat where it counts, with clamping anywhere on the surface.', 'Standard fixture blocks, stops and clamps drop straight in, so setups repeat perfectly every time.'] },
      { title: 'Clamping access on every edge', pos: '60% 38%',
        text: ['Perforated side skirts wrap the full perimeter of the table, so you can fixture from all four sides, not just the top.', 'Square a frame once, clamp it everywhere, and weld with both hands free.'] },
      { title: 'Your tools, always at hand', pos: '52% 58%',
        text: ['The integrated rack keeps clamps, squares and stops docked at the table edge, off the work surface and out of the sparks.', 'A dedicated grinder holster with battery clearance means the grinder is always where you left it.'] },
      { title: 'Structure that stays square', pos: '70% 76%',
        text: ['An interlocking ribbed substructure ties the top to heavy tube legs, resisting twist, sag and drum.', 'Run it raw steel, or have the legs powder-coated in jet black or any RAL colour before it ships.'] },
      { title: 'Rolls to the work, plants for the weld', pos: '73% 96%',
        text: ['Heavy-duty locking casters roll the table to the job, then lock down solid when you strike an arc.', 'Prefer it planted? Order the table with leveling feet instead, or take the top only and run your own base.'] },
    ];
    const panel = $('#gft-panel'), pDots = $('#gft-p-dots'), photo = $('#gft-hero-photo');
    FEATURES.forEach(() => pDots.insertAdjacentHTML('beforeend', '<i></i>'));
    let fIdx = -1;
    function openFeature(i) {
      fIdx = (i + FEATURES.length) % FEATURES.length;
      const f = FEATURES[fIdx];
      $('#gft-panel-title').textContent = f.title;
      $('#gft-panel-text').innerHTML = f.text.map(t => '<p>' + t + '</p>').join('');
      $('#gft-panel-img').style.backgroundPosition = f.pos;
      $$('.gft-dot', hero).forEach(d => d.classList.toggle('gft-active', +d.dataset.f === fIdx));
      Array.from(pDots.children).forEach((d, j) => d.classList.toggle('gft-on', j === fIdx));
      panel.classList.add('gft-show');
    }
    function closePanel() { panel.classList.remove('gft-show'); fIdx = -1; $$('.gft-dot', hero).forEach(d => d.classList.remove('gft-active')); }
    $$('.gft-dot', hero).forEach(d => d.addEventListener('click', e => { e.stopPropagation(); const i = +d.dataset.f; i === fIdx ? closePanel() : openFeature(i); }));
    $('#gft-panel-x').addEventListener('click', closePanel);
    $('#gft-p-prev').addEventListener('click', () => openFeature(fIdx - 1));
    $('#gft-p-next').addEventListener('click', () => openFeature(fIdx + 1));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closePanel(); });

    const NAT = { w: 2752, h: 1536 };
    function layoutDots() {
      const hr = hero.getBoundingClientRect(), pr = photo.getBoundingClientRect();
      if (!pr.width || !pr.height) return;
      const op = (getComputedStyle(photo).objectPosition || '50% 50%').split(' ');
      const px = parseFloat(op[0]) / 100, py = parseFloat(op[1] || '50%') / 100;
      const s = Math.max(pr.width / NAT.w, pr.height / NAT.h), DW = NAT.w * s, DH = NAT.h * s;
      const offX = pr.left - hr.left, offY = pr.top - hr.top;
      const ox = offX + (pr.width - DW) * px, oy = offY + (pr.height - DH) * py;
      $$('.gft-dot', hero).forEach(d => {
        const x = ox + parseFloat(d.dataset.fx) * DW, y = oy + parseFloat(d.dataset.fy) * DH;
        d.style.left = x + 'px'; d.style.top = y + 'px';
        const inside = x > offX + 22 && x < offX + pr.width - 22 && y > offY + 22 && y < offY + pr.height - 22;
        d.style.display = inside ? 'grid' : 'none';
      });
    }
    addEventListener('resize', layoutDots);
    addEventListener('orientationchange', () => setTimeout(layoutDots, 300));
    if (photo.complete) layoutDots(); else photo.addEventListener('load', layoutDots);
    setTimeout(layoutDots, 400); setTimeout(layoutDots, 1500);

    let tx = .6, ty = .5, cx = .6, cy = .5, raf = null;
    function tick() {
      cx += (tx - cx) * .075; cy += (ty - cy) * .075;
      hero.style.setProperty('--gx', (cx * 100) + '%'); hero.style.setProperty('--gy', (cy * 100) + '%');
      if (Math.abs(tx - cx) > .0005 || Math.abs(ty - cy) > .0005) raf = requestAnimationFrame(tick); else raf = null;
    }
    hero.addEventListener('mousemove', e => {
      const r = hero.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width; ty = (e.clientY - r.top) / r.height;
      hero.classList.add('gft-lit');
      if (!raf) raf = requestAnimationFrame(tick);
    });
    hero.addEventListener('mouseleave', () => hero.classList.remove('gft-lit'));
  }

  /* ---------- scroll reveal + FAQ ---------- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('gft-in'); io.unobserve(e.target); } }), { threshold: .1 });
    $$('.gft-reveal').forEach(el => io.observe(el));
  } else { $$('.gft-reveal').forEach(el => el.classList.add('gft-in')); }
  $$('.gft-faq-q').forEach(q => q.addEventListener('click', () => {
    const item = q.parentElement, a = $('.gft-faq-a', item), open = item.classList.contains('gft-open');
    $$('.gft-faq-item.gft-open').forEach(i => { i.classList.remove('gft-open'); $('.gft-faq-a', i).style.maxHeight = 0; });
    if (!open) { item.classList.add('gft-open'); a.style.maxHeight = a.scrollHeight + 'px'; }
  }));

  /* ====================================================================
     QUICK QUOTE: the real engine, in a worker
     ==================================================================== */
  const grid = $('#gft-size-grid');
  if (!grid) return;
  const SIZES = [[30, 40], [36, 48, 1], [30, 60], [48, 48], [30, 80], [36, 72, 1], [36, 96], [48, 72, 1], [60, 60], [48, 96, 1], [60, 120]];
  const TIER = { files: 'Files only', parts: 'The kit', built: 'Fully welded' };
  const st = { w: 48, l: 72, tier: 'built', top: 0.25, legs: 'bolt', feet: 'caster', finish: 'raw', pan: false, metric: false };

  // The design, in the engine's own settings. The same object goes to the designer page and to the cart.
  function design(s) {
    const d = { Table_L: s.l, Table_W: s.w, Top_Thick: s.top, Legs: s.legs, Feet: s.feet, Tool_Pan: !!s.pan && s.legs !== 'none',
      Stand_Color: s.finish === 'black' ? 'Jet Black' : s.finish === 'custom' ? 'Custom' : 'Raw steel' };
    if (s.finish === 'custom') d.Stand_Custom = 'RAL 1003';
    if (s.metric) { d.Hole_Dia = 16 / 25.4; d.Hole_Pitch = 50 / 25.4; d.Rib_Spacing = 200 / 25.4; d.Rib_Spacing_Y = 200 / 25.4; }
    return d;
  }

  // ---- engine: in a worker when the page allows one, else on the main thread
  const ENGINE_URL = new URL('assets/js/engine.js', document.baseURI).href;
  let worker = null, seq = 0, waiting = new Map();
  const WORKER_SRC = `importScripts(${JSON.stringify(ENGINE_URL)});
    const E = self.GorillaEngine;
    function one(d) { const cfg = Object.assign(E.defaults(), d, E.casterPatch(d.Feet || 'caster')); const r = E.compute(cfg, E.DEFAULT_SHOP);
      if (r.err) return { err: r.err.msg }; const t = {}; for (const x of r.price.tiers) t[x.key] = x.available === false ? null : x.price;
      return { tiers: t, lb: Math.round(r.totals.lb), rated: r.rating.lb, limit: r.rating.limit.what, warnings: r.warnings.filter(w => !w.minor).map(w => w.msg) }; }
    self.onmessage = e => { const { id, jobs } = e.data; const out = {}; for (const k in jobs) { try { out[k] = one(jobs[k]); } catch (x) { out[k] = { err: String(x) }; } } self.postMessage({ id, out }); };`;
  function makeWorker() {
    try {
      const w = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: 'text/javascript' })));
      w.onmessage = e => { const cb = waiting.get(e.data.id); waiting.delete(e.data.id); if (cb) cb(e.data.out); };
      w.onerror = () => { worker = null; };          // fall back to the main thread
      return w;
    } catch (e) { return null; }
  }
  function mainThread(jobs) {
    const E = window.GorillaEngine, out = {};
    for (const k in jobs) {
      try {
        const d = jobs[k], cfg = Object.assign(E.defaults(), d, E.casterPatch(d.Feet || 'caster')); const r = E.compute(cfg, E.DEFAULT_SHOP);
        if (r.err) { out[k] = { err: r.err.msg }; continue; }
        const t = {}; for (const x of r.price.tiers) t[x.key] = x.available === false ? null : x.price;
        out[k] = { tiers: t, lb: Math.round(r.totals.lb), rated: r.rating.lb, limit: r.rating.limit.what, warnings: r.warnings.filter(w => !w.minor).map(w => w.msg) };
      } catch (x) { out[k] = { err: String(x) }; }
    }
    return out;
  }
  function price(jobs, cb) {
    if (worker === null && location.protocol !== 'file:') worker = makeWorker() || false;
    if (worker) { const id = ++seq; waiting.set(id, cb); worker.postMessage({ id, jobs }); }
    else if (window.GorillaEngine) setTimeout(() => cb(mainThread(jobs)), 0);
    else addEventListener('load', () => cb(mainThread(jobs)), { once: true });
  }

  // ---- the size grid
  SIZES.forEach(([w, l, pop]) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'gft-size-btn' + (pop ? ' gft-popular' : ''); b.dataset.w = w; b.dataset.l = l;
    b.innerHTML = '<span class="gft-dims">' + w + '×' + l + '</span><span class="gft-sqft" data-from>' + (w * l / 144).toFixed(1).replace(/\.0$/, '') + ' sq ft</span>';
    b.addEventListener('click', () => { st.w = w; st.l = l; $('#gft-w').value = w; $('#gft-l').value = l; render(); });
    grid.appendChild(b);
  });
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const onSize = () => { st.w = clamp(Math.round(+$('#gft-w').value || 48), 12, 60); st.l = clamp(Math.round(+$('#gft-l').value || 72), 12, 120); if (st.w > st.l) [st.w, st.l] = [st.l, st.w]; render(); };
  $('#gft-w').addEventListener('change', onSize); $('#gft-l').addEventListener('change', onSize);
  $$('[data-tier]').forEach(b => b.addEventListener('click', () => { st.tier = b.dataset.tier; render(); }));
  $$('[data-top]').forEach(b => b.addEventListener('click', () => { st.top = +b.dataset.top; render(); }));
  $$('[data-legs]').forEach(b => b.addEventListener('click', () => { st.legs = b.dataset.legs; render(); }));
  $$('[data-feet]').forEach(b => b.addEventListener('click', () => { st.feet = b.dataset.feet; render(); }));
  $$('[data-finish]').forEach(b => b.addEventListener('click', () => { st.finish = b.dataset.finish; render(); }));
  $('#gft-opt-pan').addEventListener('change', e => { st.pan = e.target.checked; render(); });
  $('#gft-opt-metric').addEventListener('change', e => { st.metric = e.target.checked; render(); });
  $$('[data-preset]').forEach(a => a.addEventListener('click', () => { st.tier = a.dataset.preset; render(); }));

  function specString() {
    return `${st.w}×${st.l} · ${TIER[st.tier]} · ${st.top === 0.25 ? '1/4"' : st.top === 0.375 ? '3/8"' : '1/2"'} top · ` +
      ({ bolt: 'bolt-on legs', hframe: 'welded H-frame', kd: 'knock-down H-frame', none: 'top only' })[st.legs] +
      (st.legs !== 'none' ? ' · ' + ({ caster: 'casters', levcaster: 'leveling casters', leveler: 'leveling feet' })[st.feet] : '') +
      ' · ' + ({ raw: 'raw steel', black: 'black legs', custom: 'custom colour' })[st.finish] + (st.pan && st.legs !== 'none' ? ' · tool pan' : '') + (st.metric ? ' · 16 mm holes' : '');
  }
  function designerQuery() {
    const d = design(st), q = new URLSearchParams(); for (const k in d) q.set(k, d[k]); q.set('tier', st.tier);
    return q.toString();
  }
  function designerLink() { return 'design/?' + designerQuery(); }
  // "Fine-tune in the designer": load this exact table into the designer on the page and scroll to it
  $('#gft-btn-design').addEventListener('click', e => {
    const f = $('#gft-designer'); if (!f) return;
    e.preventDefault();
    f.src = 'design/app.html?embed=1&' + designerQuery();
    $('#gft-designer-full').href = designerLink();
    $('#designer').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  // The designer talks to the page it sits in (on the live site: the WooCommerce cart)
  window.addEventListener('message', e => {
    const m = e.data; if (!m || typeof m.type !== 'string' || m.type.indexOf('gorilla-tables:') !== 0) return;
    console.log(m.type, m.order);
  });

  let gen = 0, last = null;
  function render() {
    const g = ++gen;
    $$('.gft-size-btn').forEach(b => b.classList.toggle('gft-sel', +b.dataset.w === st.w && +b.dataset.l === st.l));
    $$('[data-tier]').forEach(b => b.classList.toggle('gft-sel', b.dataset.tier === st.tier));
    $$('[data-top]').forEach(b => b.classList.toggle('gft-sel', +b.dataset.top === st.top));
    $$('[data-legs]').forEach(b => b.classList.toggle('gft-sel', b.dataset.legs === st.legs));
    $$('[data-feet]').forEach(b => b.classList.toggle('gft-sel', b.dataset.feet === st.feet));
    $('#gft-feet-row').style.opacity = st.legs === 'none' ? .4 : 1; $('#gft-feet-row').style.pointerEvents = st.legs === 'none' ? 'none' : '';
    $$('[data-finish]').forEach(b => b.classList.toggle('gft-sel', b.dataset.finish === st.finish));
    $('#gft-sum-title').textContent = `${st.w} × ${st.l} ${st.tier === 'files' ? 'files' : st.tier === 'parts' ? 'kit' : 'welded'}`;
    $('#gft-sum-sub').textContent = specString().split(' · ').slice(2).join(' · ');

    // this build, plus every alternative the option buttons show a price for
    const jobs = { main: design(st) };
    const alt = (k, patch) => { jobs[k] = design(Object.assign({}, st, patch)); };
    alt('t25', { top: 0.25 }); alt('t38', { top: 0.375 }); alt('t50', { top: 0.5 });
    alt('nolegs', { legs: 'none' }); alt('legs', { legs: st.legs === 'none' ? 'bolt' : st.legs });
    alt('raw', { finish: 'raw' }); alt('black', { finish: 'black' }); alt('custom', { finish: 'custom' });
    alt('pan0', { pan: false }); alt('pan1', { pan: true });
    SIZES.forEach(([w, l]) => alt('s' + w + 'x' + l, { w, l }));
    price(jobs, out => {
      if (g !== gen) return;                            // a newer render is on its way
      last = out;
      const m = out.main, tier = st.tier;
      const at = r => (r && !r.err && r.tiers[tier] != null) ? r.tiers[tier] : null;
      const total = at(m);
      if (m.err) { $('#gft-sum-total').textContent = '—'; $('#gft-sum-lines').innerHTML = '<div class="gft-sum-line"><span class="gft-k">' + m.err + '</span></div>'; return; }
      $('#gft-sum-total').textContent = total == null ? 'Quote' : fmt(total);
      $('#gft-sum-persq').textContent = total == null ? 'Request a quote for this one' : fmt(total / (st.w * st.l / 144)) + ' per sq ft';
      const lines = [[`${st.w}×${st.l} ${TIER[tier].toLowerCase()}, ${st.top === 0.25 ? '1/4"' : st.top === 0.375 ? '3/8"' : '1/2"'} top`, total == null ? 'quote' : fmt(total)]];
      $('#gft-sum-lines').innerHTML = lines.map(([k, v]) => `<div class="gft-sum-line"><span class="gft-k">${k}</span><span class="gft-v">${v}</span></div>`).join('') +
        (m.warnings.length ? `<div class="gft-sum-line"><span class="gft-k" style="color:#F2A33A">${m.warnings[0]}</span></div>` : '');
      $('#gft-sum-rated').textContent = m.rated.toLocaleString('en-US') + ' lb';
      $('#gft-sum-weight').textContent = m.lb.toLocaleString('en-US') + ' lb';
      for (const k of ['files', 'parts', 'built']) { const v = m.tiers[k]; $('#gft-pr-' + k).textContent = v == null ? 'Quote' : fmt(v); }
      const delta = (key, label) => { const v = at(out[key]); const el = $(label); if (!el) return; el.textContent = v == null || total == null ? '' : v === total ? 'Included' : (v > total ? '+' : '−') + fmt(Math.abs(v - total)); };
      delta('t38', '#gft-pr-t38'); delta('t50', '#gft-pr-t50'); delta('nolegs', '#gft-pr-nolegs');
      delta('black', '#gft-pr-black'); delta('custom', '#gft-pr-custom'); delta(st.pan ? 'pan0' : 'pan1', '#gft-pr-pan');
      if (st.pan) { const v = at(out.pan0); $('#gft-pr-pan').textContent = v == null || total == null ? '' : '+' + fmt(total - v); }
      $$('.gft-size-btn').forEach(b => { const v = at(out['s' + b.dataset.w + 'x' + b.dataset.l]); $('[data-from]', b).textContent = v == null ? (b.dataset.w * b.dataset.l / 144).toFixed(1).replace(/\.0$/, '') + ' sq ft' : 'from ' + fmt(v); });
    });
  }
  render();

  // "from" prices in the hero and the three cards: the cheapest standard size for each tier
  price(Object.fromEntries(SIZES.map(([w, l]) => ['s' + w + 'x' + l, design({ w, l, tier: 'built', top: 0.25, legs: 'bolt', feet: 'caster', finish: 'raw' })])), out => {
    const min = k => Math.min(...Object.values(out).filter(r => !r.err && r.tiers[k] != null).map(r => r.tiers[k]));
    const f = min('files'), p = min('parts'), b = min('built');
    if (isFinite(f)) $('#gft-from-files').textContent = fmt(f);
    if (isFinite(p)) { $('#gft-from-parts').textContent = fmt(p); $('#gft-from-price').textContent = fmt(p); }
    if (isFinite(b)) $('#gft-from-built').textContent = fmt(b);
  });

  /* ---- Add to cart (demo) and Request a quote ---- */
  $('#gft-btn-cart').addEventListener('click', () => {
    const btn = $('#gft-btn-cart'), total = last && last.main && last.main.tiers[st.tier];
    btn.textContent = 'Added ✓ (demo)';
    setTimeout(() => { btn.textContent = 'Add to cart'; }, 2200);
    // On the live site this is the WooCommerce add-to-cart call, with the design attached to the line item.
    console.log('gorilla-tables:add-to-cart', { design: design(st), tier: st.tier, price: total, spec: specString() });
  });
  $('#gft-btn-quote').addEventListener('click', () => {
    const total = last && last.main && last.main.tiers[st.tier];
    const body = `Hi Gorilla Tables,\n\nPlease quote this table:\n${specString()}${total != null ? ' · shown as ' + fmt(total) : ''}.\n\nDesign: ${JSON.stringify(design(st))}\n\nName:\nPhone:\nShip to ZIP:\nAnything else:\n`;
    location.href = 'mailto:sales@fabricationtables.com?subject=' + encodeURIComponent(`Quote request: ${st.w}x${st.l} fixture table`) + '&body=' + encodeURIComponent(body);
  });
})();
