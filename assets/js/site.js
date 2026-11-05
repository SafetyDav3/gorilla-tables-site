/* Gorilla Tables — front-end
   Header, hero hotspot explorer, scroll reveal, FAQ, the contact form, and the message channel from the
   embedded designer. Pricing lives in the designer itself (design/app.html); the pages are static. */
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

  /* ---------- contact form: opens an email with the details (the live site posts it to the shop) ---------- */
  const form = $('#gft-contact-form');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const f = new FormData(form), g = k => (f.get(k) || '').toString().trim();
    const body = `Name: ${g('name')}\nEmail: ${g('email')}\nPhone: ${g('phone')}\nShip-to ZIP: ${g('zip')}\n\n${g('body')}\n`;
    location.href = 'mailto:sales@fabricationtables.com?subject=' + encodeURIComponent('Quote request from ' + (g('name') || 'the website')) + '&body=' + encodeURIComponent(body);
  });

  /* ---------- the embedded designer talks to the page it sits in (on the live site: the cart) ---------- */
  addEventListener('message', e => {
    const m = e.data; if (!m || typeof m.type !== 'string' || m.type.indexOf('gorilla-tables:') !== 0) return;
    console.log(m.type, m.order);
  });
})();
