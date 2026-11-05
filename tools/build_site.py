#!/usr/bin/env python3
"""Gorilla Tables website: one shell, several pages.

    python3 tools/build_site.py          -> writes index.html, tables/, design/, how/, shop/, faq/, contact/, legal/

Every page shares the header, footer and <head> from here, so the navigation and the metadata stay the same
everywhere. The web developer can read each page's body as plain HTML; nothing here is a template language.
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://safetydav3.github.io/gorilla-tables-site/'
PHONE = '920-246-9567'
TEL = 'tel:9202469567'
EMAIL = 'sales@fabricationtables.com'
ADDR = '3190 Water Division Rd · Denmark, WI 54208'

# The 2026 price list (same figures as the designer's shop settings): W, L, kit, welded
LIST = [(30, 40, 1199, 1599), (36, 48, 1299, 1699), (30, 60, 1399, 1799), (48, 48, 1749, 2199), (30, 80, 1799, 2399),
        (36, 72, 1899, 2499), (36, 96, 2399, 3199), (48, 72, 2399, 3199), (60, 60, 2449, 3299), (48, 96, 3599, 4699), (60, 120, 5299, 6499)]
POPULAR = {(36, 48), (36, 72), (48, 72), (48, 96)}
FROM = {'files': 59, 'parts': min(r[2] for r in LIST), 'built': min(r[3] for r in LIST)}
money = lambda n: '$' + f'{n:,}'

NAV = [('tables/', 'Standard tables'), ('design/', 'Design your own'), ('how/', 'Kit or welded'), ('shop/', 'The shop'), ('faq/', 'FAQ'), ('contact/', 'Contact')]


def head(title, desc, rel, path, extra=''):
    url = SITE + path
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{rel}assets/img/gorilla.png">
<meta property="og:site_name" content="Gorilla Tables">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/img/og.jpg?v=2">
<meta property="og:image:secure_url" content="{SITE}assets/img/og.jpg?v=2">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Gorilla Tables: welding tables built for the bold">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:image" content="{SITE}assets/img/og.jpg?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800;900&family=DM+Sans:wght@400;500;600;700&family=Hanken+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="{rel}assets/css/site.css">
{extra}</head>
'''


def header(rel, active, over=False):
    items = ''.join(f'<li><a href="{rel}{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="gft gft-hdr{' gft-hdr-over' if over else ''}" id="gft-hdr">
  <a class="gft-hdr-logo" href="{rel if rel else './'}">
    <img src="{rel}assets/img/gorilla.png" alt="Gorilla Tables" width="60" height="60">
    <span class="gft-hdr-type"><span class="gft-hdr-l1">GORILLA</span><span class="gft-hdr-l2">Tables</span></span>
  </a>
  <nav class="gft-hdr-nav" aria-label="Main"><ul>{items}</ul></nav>
  <div class="gft-hdr-right">
    <a class="gft-hdr-tel" href="{TEL}">{PHONE}</a>
    <a class="gft-btn gft-hdr-cta" href="{rel}design/">Build your table</a>
    <button class="gft-hdr-burger" id="gft-hdr-burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
  </div>
  <div class="gft-hdr-mobile" id="gft-hdr-mobile">
    <ul>{items}</ul>
    <div class="gft-hdr-mobile-foot"><a class="gft-btn" href="{rel}design/">Build your table</a><a class="gft-hdr-tel" href="{TEL}">{PHONE}</a></div>
  </div>
</header>
'''


def footer(rel):
    return f'''<footer class="gft gft-footer">
  <div class="gft-footer-top">
    <div class="gft-footer-brand">
      <img src="{rel}assets/img/gorilla.png" alt="" width="44" height="44">
      <div><b>Gorilla Tables</b><span>Fixture-block welding tables, laser-cut and welded in Denmark, Wisconsin.</span></div>
    </div>
    <div class="gft-footer-col"><b>Tables</b><a href="{rel}tables/">Standard tables</a><a href="{rel}design/">Design your own</a><a href="{rel}how/">Kit or welded</a></div>
    <div class="gft-footer-col"><b>Company</b><a href="{rel}shop/">The shop</a><a href="{rel}faq/">FAQ</a><a href="{rel}contact/">Contact</a><a href="https://gerardenfabrication.com">Gerarden Fabrication</a></div>
    <div class="gft-footer-col"><b>Get in touch</b><a href="{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>{ADDR}</span></div>
  </div>
  <div class="gft-footer-bottom">
    <span>© 2026 Gerarden Fabrication &amp; Design LLC · Gorilla Tables is a Gerarden Fabrication brand</span>
    <span><a href="{rel}legal/terms.html">Terms of sale</a> · <a href="{rel}legal/files.html">File licence</a> · <a href="{rel}legal/privacy.html">Privacy</a> · <a href="{rel}webdev/">For the web developer</a></span>
  </div>
</footer>
<script src="{rel}assets/js/site.js" defer></script>
</body>
</html>
'''


def page_head(title, lede, extra=''):
    return f'''  <section class="gft gft-page-head">
    <h1>{title}<span class="gft-cy">.</span></h1>
    <p class="gft-lede">{lede}</p>{extra}
  </section>
'''


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w') as f: f.write(html)
    print('wrote', path, len(html))


# ------------------------------------------------------------------------------------------------- home ---
def home():
    rel = ''
    sizes = ''.join(f'''<a class="gft-size-card{' gft-pop' if (w, l) in POPULAR else ''}" href="tables/#t{w}x{l}">{'<span class="gft-tag">Popular</span>' if (w, l) in POPULAR else ''}<b>{w}×{l}</b><span>kit {money(k)} · welded {money(b)}</span></a>''' for w, l, k, b in LIST)
    body = f'''<body class="gft-home">
{header(rel, None, over=True)}
<main id="gft-home" class="gft-home-main">

  <div class="gft gft-hero" id="gft-stage">
    <img class="gft-hero-photo" id="gft-hero-photo" src="assets/img/hero-table.jpg" width="2788" height="1556" alt="Gorilla Tables fixture-block welding table with clamp rack, grinder holster and locking casters">
    <div class="gft-glow-a"></div><div class="gft-glow-b"></div>
    <div class="gft-hero-content">
      <h1>Welding tables built for the bold<span class="gft-cy">.</span></h1>
      <p class="gft-lede">Fixture-block tables laser-cut and welded in Denmark, Wisconsin. Dead flat, endlessly clampable, and priced like you actually plan to buy one.</p>
      <div class="gft-hero-ctas"><a class="gft-btn" href="tables/">See the standard tables</a><a class="gft-btn gft-ghost" href="design/">Design your own</a></div>
    </div>
    <button class="gft-dot" data-f="0" data-fx=".815" data-fy=".295" aria-label="Feature 1"><span></span></button>
    <button class="gft-dot" data-f="1" data-fx=".615" data-fy=".395" aria-label="Feature 2"><span></span></button>
    <button class="gft-dot" data-f="2" data-fx=".555" data-fy=".565" aria-label="Feature 3"><span></span></button>
    <button class="gft-dot" data-f="3" data-fx=".685" data-fy=".715" aria-label="Feature 4"><span></span></button>
    <button class="gft-dot" data-f="4" data-fx=".715" data-fy=".885" aria-label="Feature 5"><span></span></button>
    <aside class="gft-panel" id="gft-panel">
      <div class="gft-panel-img" id="gft-panel-img"></div>
      <button class="gft-panel-x" id="gft-panel-x" aria-label="Close">✕</button>
      <div class="gft-panel-body"><h3 id="gft-panel-title"></h3><div id="gft-panel-text"></div></div>
      <div class="gft-panel-foot">
        <div class="gft-p-dots" id="gft-p-dots"></div>
        <div class="gft-p-nav"><button class="gft-p-arrow" id="gft-p-prev" aria-label="Previous">←</button><button class="gft-p-arrow gft-next" id="gft-p-next" aria-label="Next">→</button></div>
      </div>
    </aside>
    <div class="gft-hero-meta">
      <span>Kits from <b>{money(FROM['parts'])}</b></span><span>Welded from <b>{money(FROM['built'])}</b></span><span><b>Any size</b> to 5' x 10'</span><span>1/4", 3/8" &amp; 1/2" plate tops</span><span>Ships nationwide</span>
    </div>
  </div>

  <section class="gft gft-details" id="details">
    <div class="gft-giant gft-reveal">The difference is in the details<span class="gft-cy">.</span></div>
    <div class="gft-cards">
      <div class="gft-card gft-card-text gft-reveal"><h3>A top that means it</h3><p>1/4", 3/8" or 1/2" steel plate, laser-cut with 5/8" fixture holes on a precise 2" grid (or 16 mm on 50 mm, if that's your tooling). Flat where it counts, with clamping anywhere on the surface, and enough mass to shrug off years of grinding and hammer work.</p><span class="gft-foot">Laser-cut plate top</span></div>
      <div class="gft-card gft-card-photo gft-reveal"><img src="assets/img/table-raw.jpg" loading="lazy" alt="Raw steel fixture table"></div>
      <div class="gft-card gft-card-text gft-reveal"><h3>Clamp from every edge</h3><p>Perforated side skirts wrap the full perimeter, so fixture blocks, stops and clamps work on all four sides, not just the top. Square once, clamp everywhere, weld with both hands free.</p><span class="gft-foot">Full-perimeter hole grid</span></div>
      <div class="gft-card gft-card-photo gft-reveal"><img src="assets/img/table-ribs.jpg" loading="lazy" alt="Ribbed substructure"></div>
      <div class="gft-card gft-card-photo gft-reveal"><img src="assets/img/table-powder.jpg" loading="lazy" alt="Powder coated welding table"></div>
      <div class="gft-card gft-card-text gft-reveal"><h3>Rigid by design</h3><p>An interlocking ribbed substructure ties the top to heavy tube legs, resisting twist, sag and drum. It goes together square and it stays that way, on casters or planted on fixed feet. Every table carries a rated load worked out from its own plate and ribs.</p><span class="gft-foot">Ribbed substructure</span></div>
      <div class="gft-card gft-card-photo gft-reveal"><img src="assets/img/hero-table.jpg" loading="lazy" alt="Loaded fixture table"></div>
      <div class="gft-card gft-card-text gft-reveal"><h3>Cut and built in Wisconsin</h3><p>Every table is laser-cut, formed and welded by the crew at Gerarden Fabrication in Denmark, Wisconsin. The same hands that build our custom commercial work build your table.</p><span class="gft-foot">Gerarden Fabrication</span></div>
    </div>
  </section>

  <section class="gft gft-sizes" id="sizes">
    <div class="gft-sizes-head gft-reveal">
      <div><h2 class="gft-sec-title">Eleven standard sizes<span class="gft-cy">.</span></h2>
      <p class="gft-lede">Each one priced as a kit you weld or a table we weld. 1/4" top, 6" deep, bolt-on legs and locking casters; add a thicker top or a tool pan on the tables page.</p></div>
      <a class="gft-btn gft-ghost" href="tables/">All the tables</a>
    </div>
    <div class="gft-size-cards gft-reveal">{sizes}</div>
    <p class="gft-sizes-foot gft-reveal">Need another size? <a href="design/">Design your own</a>, any size up to 60" x 120", priced as you go.</p>
  </section>

  <section class="gft gft-ways" id="ways">
    <div class="gft-ways-head gft-reveal">
      <h2 class="gft-sec-title">Three ways to get one<span class="gft-cy">.</span></h2>
      <p class="gft-lede">Cut it yourself from our files, weld our kit, or let our fabricators hand you a finished table.</p>
    </div>
    <div class="gft-way-grid gft-three">
      <div class="gft-way gft-reveal">
        <div class="gft-ph"><img src="assets/img/table-ribs.jpg" loading="lazy" alt="Laser files for a fixture table"><span class="gft-price">From <b>{money(FROM['files'])}</b></span></div>
        <div class="gft-way-body"><h3>Files only</h3><p>Laser-ready DXF files for every part of the table you designed, with the drawing and the assembly guide. Cut it on your own laser, or have a local shop cut it.</p>
          <ul><li>Any size, your hole system</li><li>Drawing and step-by-step guide included</li><li>Download after your order is approved</li></ul>
          <a class="gft-btn gft-on-dark" href="design/?tier=files">Price the files</a></div>
      </div>
      <div class="gft-way gft-reveal">
        <div class="gft-ph"><img src="assets/img/table-raw.jpg" loading="lazy" alt="Table kit"><span class="gft-price">From <b>{money(FROM['parts'])}</b></span></div>
        <div class="gft-way-body"><h3>The kit</h3><p>Every part laser-cut, tabbed and slotted so the structure self-fixtures square. You weld it out in an afternoon and know your table inside and out.</p>
          <ul><li>CNC laser-cut parts, deburred, with hardware</li><li>Ships flat-pack for lower freight</li><li>The best first weldment you'll ever make</li></ul>
          <a class="gft-btn gft-on-dark" href="design/?tier=parts">Price a kit</a></div>
      </div>
      <div class="gft-way gft-reveal">
        <div class="gft-ph"><img src="assets/img/table-powder.jpg" loading="lazy" alt="Fully welded table"><span class="gft-price">From <b>{money(FROM['built'])}</b></span></div>
        <div class="gft-way-body"><h3>Fully welded</h3><p>Our fabricators build it, weld it and check it flat before it leaves the shop. Uncrate it, lock the casters, strike an arc.</p>
          <ul><li>Welded and inspected in Denmark, WI</li><li>Arrives ready to work, zero assembly</li><li>Powder-coated legs in any RAL colour</li></ul>
          <a class="gft-btn gft-on-dark" href="design/?tier=built">Price a welded table</a></div>
      </div>
    </div>
    <p class="gft-ways-more gft-reveal"><a href="how/">How the three compare, and how a kit goes together →</a></p>
  </section>

  <section class="gft gft-designer-teaser" id="designer">
    <div class="gft-teaser-grid">
      <div class="gft-reveal">
        <h2 class="gft-sec-title">Or design exactly the table you want<span class="gft-cy">.</span></h2>
        <p class="gft-lede">Any size to 5' x 10'. Pick the top, the hole system, the ribs, the legs and the finish, spin it in 3D, and watch the price, weight and rated load update as you go. Five short steps, no email required.</p>
        <div class="gft-hero-ctas"><a class="gft-btn" href="design/">Open the designer</a><a class="gft-btn gft-ghost" href="how/#assembly">See how it's built</a></div>
      </div>
      <a class="gft-teaser-shot gft-reveal" href="design/" aria-label="Open the designer"><img src="assets/img/designer.jpg" loading="lazy" alt="The Gorilla Tables designer: a 3D table with live price and rated load"></a>
    </div>
  </section>

  <section class="gft gft-story" id="shop">
    <div class="gft-story-grid">
      <div class="gft-reveal">
        <h2>Built by hand. Designed with purpose<span class="gft-cy">.</span></h2>
        <p>Gorilla Tables is built by Gerarden Fabrication, the Denmark, Wisconsin shop behind custom staircases, commercial weldments and one-off builds for people who notice the difference.</p>
        <p>We built our first fixture table because we needed one that was flat, rigid and didn't cost more than the welder sitting next to it. Then other shops started asking for them.</p>
        <p class="gft-addr">{ADDR}</p>
        <a class="gft-btn gft-on-dark" href="shop/">About the shop</a>
      </div>
      <div class="gft-story-img gft-reveal"><img src="assets/img/table-powder.jpg" loading="lazy" alt="A powder-coated Gorilla table in the Gerarden Fabrication shop"></div>
    </div>
  </section>

  <section class="gft gft-final">
    <div class="gft-ghost2 gft-reveal">Stop working on<br>a wobbly table<span class="gft-cy">.</span></div>
    <p class="gft-lede gft-reveal">Pick a standard size or spec your own in a minute. Built flat in Wisconsin and shipped to your floor.</p>
    <div class="gft-hero-ctas gft-center gft-reveal"><a class="gft-btn" href="tables/">Standard tables</a><a class="gft-btn gft-ghost" href="design/">Design your own</a></div>
  </section>
</main>
'''
    write('index.html', head('Gorilla Tables — Welding tables built for the bold', 'Fixture-block welding tables laser-cut and welded in Denmark, Wisconsin. Eleven standard sizes or design your own: live price, 3D preview, kit or fully welded.', rel, '', '<link rel="preload" as="image" href="assets/img/hero-table.jpg">\n') + body + footer(rel))


# ----------------------------------------------------------------------------------------------- tables ---
def tables():
    rel = '../'
    rows = ''.join(f'<tr id="t{w}x{l}"{" class=\"gft-pop\"" if (w, l) in POPULAR else ""}><td><b>{w} × {l}</b>{" <span class=\"gft-tag\">Popular</span>" if (w, l) in POPULAR else ""}</td><td>{w * l / 144:.1f} sq ft</td><td>{money(k)}</td><td>{money(b)}</td><td><a href="{rel}design/?Table_W={w}&amp;Table_L={l}&amp;tier=parts">Kit</a> · <a href="{rel}design/?Table_W={w}&amp;Table_L={l}&amp;tier=built">Welded</a></td></tr>' for w, l, k, b in LIST)
    body = f'''<body class="gft-page gft-tables-page">
{header(rel, 'tables/')}
<main>
{page_head('Standard tables', 'Eleven sizes we build all the time, priced as a kit you weld or a table we weld. Pick one below, change the top, legs, feet or tool pan with the dropdowns, and send it to the designer or straight to the cart.')}
  <section class="gft gft-embed">
    <div class="gft-designer-frame gft-tall">
      <iframe id="gft-designer" src="{rel}design/app.html?embed=1&amp;tab=standard" title="Gorilla Tables standard tables" allow="fullscreen"></iframe>
    </div>
    <div class="gft-designer-bar">
      <span>Every card shows the kit and welded price for that size with the options you pick.</span>
      <span>"Use this table" opens it in the designer for the fine details.</span>
      <a href="{rel}design/">Open the full designer →</a>
    </div>
  </section>

  <section class="gft gft-pricelist">
    <div class="gft-reveal">
      <h2 class="gft-sec-title">The price list<span class="gft-cy">.</span></h2>
      <p class="gft-lede">Standard tables: 1/4" plate top and frame, 6" deep, 5/8" fixture holes on a 2" grid, 2" square tube legs, 4" locking casters, raw steel. Welded = kit + the welding.</p>
    </div>
    <table class="gft-table gft-reveal">
      <thead><tr><th>Size (W × L)</th><th>Area</th><th>Kit</th><th>Fully welded</th><th>Open</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <div class="gft-adders gft-reveal">
      <div><b>3/8" top</b><span>+$400 to +$1,250 by size</span></div>
      <div><b>Tool pan (lower shelf)</b><span>+$275 to +$500 by size</span></div>
      <div><b>Top only, no legs</b><span>−$150 to −$300 by size</span></div>
      <div><b>Powder-coated legs</b><span>+$425 satin black · +$525 any RAL colour</span></div>
      <div><b>Liftgate delivery</b><span>+$149</span></div>
      <div><b>Custom sizes</b><span>Priced between the sizes above, in the <a href="{rel}design/">designer</a></span></div>
    </div>
  </section>

  <section class="gft gft-final gft-final-slim">
    <p class="gft-lede gft-reveal">Don't see your size? Any size up to 60" × 120", priced on the spot.</p>
    <a class="gft-btn gft-reveal" href="{rel}design/">Design your own</a>
  </section>
</main>
'''
    write('tables/index.html', head('Standard tables — Gorilla Tables', 'Eleven standard fixture-block welding table sizes from 30 x 40 to 60 x 120, priced as a kit or fully welded. 1/4" plate top, 2" hole grid, locking casters.', rel, 'tables/') + body + footer(rel))


# ----------------------------------------------------------------------------------------------- design ---
def design():
    rel = '../'
    extra = '''<style>
  body.gft-design-page main.gft-design-stage { padding-top: 0; flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; }
  .gft-design-stage iframe { flex: 1 1 auto; width: 100%; height: calc(100vh - 104px); min-height: 560px; border: 0; display: block; }
  .gft-design-page .gft-hdr { position: sticky; top: 0; }
  @media (max-width: 900px) { .gft-design-stage iframe { height: calc(100vh - 84px); } }
</style>
'''
    body = f'''<body class="gft-page gft-design-page">
{header(rel, 'design/')}
<main class="gft-design-stage">
  <iframe id="gft-designer" src="app.html?embed=1" title="Gorilla Tables designer" allow="fullscreen"></iframe>
</main>
<script>
  // A design in this page's address (from a link on the site) goes through to the designer
  (function () {{
    var q = location.search.replace(/^\\?/, '');
    if (q) document.getElementById('gft-designer').src = 'app.html?embed=1&' + q;
  }})();
</script>
'''
    write('design/index.html', head('Design your own table — Gorilla Tables', 'Design your fixture-block welding table: any size to 60 x 120, live price, 3D preview, rated load. Files, kit or fully welded.', rel, 'design/', extra) + body + footer(rel))


# -------------------------------------------------------------------------------------------------- how ---
def how():
    rel = '../'
    body = f'''<body class="gft-page">
{header(rel, 'how/')}
<main>
{page_head('Kit or welded', 'The same table three ways: the laser files, a kit you weld, or a table our fabricators finish. Here is what each one gets you, and how a kit goes together.')}
  <section class="gft gft-compare">
    <table class="gft-table gft-reveal">
      <thead><tr><th></th><th>Files only</th><th>The kit</th><th>Fully welded</th></tr></thead>
      <tbody>
        <tr><td>What you get</td><td>Laser-ready DXFs, drawing, assembly guide</td><td>Every part cut and deburred, hardware, casters or feet, the guide</td><td>The finished table, checked flat, crated</td></tr>
        <tr><td>You need</td><td>A laser (yours or a local shop's), a welder</td><td>A welder, clamps, two sawhorses, an afternoon</td><td>A place to put it</td></tr>
        <tr><td>Flatness</td><td>Yours to achieve: the guide shows how</td><td>Self-fixturing tabs and the U-bolt method keep it flat</td><td>Checked with a straightedge before it ships</td></tr>
        <tr><td>Finish</td><td>Your call</td><td>Raw steel, ready to paint or oil</td><td>Raw, or powder-coated legs in satin black or any RAL colour</td></tr>
        <tr><td>Freight</td><td>None</td><td>Flat-pack on a skid, LTL</td><td>Crated on a skid, LTL; liftgate available</td></tr>
        <tr><td>From</td><td><b>{money(FROM['files'])}</b></td><td><b>{money(FROM['parts'])}</b></td><td><b>{money(FROM['built'])}</b></td></tr>
      </tbody>
    </table>
  </section>

  <section class="gft gft-how" id="assembly">
    <div class="gft-reveal"><h2 class="gft-sec-title">How a kit goes together<span class="gft-cy">.</span></h2>
    <p class="gft-lede">One person can build it. The parts are tabbed and slotted so the structure fixtures itself square, and the top is pulled flat with U-bolts before anything is welded.</p></div>
    <ol class="gft-steps gft-reveal">
      <li><b>Top plate face down</b><span>On a flat surface. Knock the slag off every part and check the tabs drop into their slots.</span></li>
      <li><b>Ribs in</b><span>Cross ribs into the top's slots, long ribs over them so the half-laps interlock. A straightedge across the rib edges shows any high spot.</span></li>
      <li><b>Clamp and tack</b><span>Clamp each rib to the top and put small tacks at the crossings and rib ends. Just enough to hold it for the flip.</span></li>
      <li><b>Flip onto horses and U-bolt</b><span>A U-bolt in every bay hooks under each rib, legs up through the fixture holes, plate and nuts on top. Run them down from the middle out until no light shows under a straightedge.</span></li>
      <li><b>Weld the top</b><span>Tack every tab, then weld the pockets in short stitches from the middle out, letting it cool between passes. The tabs sit just below the surface so the welds dress flush.</span></li>
      <li><b>Walls on</b><span>Flip it back with the U-bolts still on, slide the walls over the rib ends, draw them in with bar clamps, check the diagonals, tack and weld.</span></li>
      <li><b>Leg plates, legs, feet</b><span>U-bolts off, leg plates in the corners, weld out, bolt on the legs with casters or levelers, stand it up and lock the wheels.</span></li>
    </ol>
    <p class="gft-how-foot gft-reveal">Every kit ships with the full guide: an exploded picture for each step, the U-bolt sizes for your hole system, and the hardware list. You can preview it for any table in the <a href="{rel}design/">designer</a> ("Assembly plan").</p>
  </section>

  <section class="gft gft-final gft-final-slim">
    <p class="gft-lede gft-reveal">Ready? Pick a standard size or design your own.</p>
    <div class="gft-hero-ctas gft-center gft-reveal"><a class="gft-btn" href="{rel}tables/">Standard tables</a><a class="gft-btn gft-ghost" href="{rel}design/">Design your own</a></div>
  </section>
</main>
'''
    write('how/index.html', head('Kit or welded — Gorilla Tables', 'Files, kit or fully welded: what each option includes, and how a Gorilla Tables kit goes together with the U-bolt method.', rel, 'how/') + body + footer(rel))


# ------------------------------------------------------------------------------------------------- shop ---
def shop():
    rel = '../'
    body = f'''<body class="gft-page">
{header(rel, 'shop/')}
<main>
{page_head('The shop', 'Gorilla Tables is a brand of Gerarden Fabrication &amp; Design, a custom metal fabrication shop in Denmark, Wisconsin.')}
  <section class="gft gft-story">
    <div class="gft-story-grid">
      <div class="gft-reveal">
        <h2>Built by hand. Designed with purpose<span class="gft-cy">.</span></h2>
        <p>Gerarden Fabrication builds custom staircases, commercial weldments and one-off pieces for people who notice the difference. The fixture tables started the way most good tools do: we needed one that was flat, rigid and didn't cost more than the welder next to it, so we built it. Then other shops started asking.</p>
        <p>Every Gorilla table is laser-cut on our own 4 kW laser, formed and welded here, and checked flat before it leaves. The kits are cut on the same machine from the same files; the only difference is whose hands do the welding.</p>
        <p class="gft-addr">{ADDR}</p>
        <a class="gft-btn gft-on-dark" href="https://gerardenfabrication.com">Visit Gerarden Fabrication</a>
      </div>
      <div class="gft-story-img gft-reveal"><img src="{rel}assets/img/table-powder.jpg" loading="lazy" alt="A powder-coated Gorilla table in the Gerarden Fabrication shop"></div>
    </div>
  </section>
  <section class="gft gft-shop-facts">
    <div class="gft-cards gft-reveal">
      <div class="gft-card gft-card-text"><h3>Laser-cut in house</h3><p>Plate up to 1/2" cut on our own CO2 laser, nested and cut from the same files the designer writes.</p><span class="gft-foot">Mild steel plate</span></div>
      <div class="gft-card gft-card-text"><h3>Welded and checked</h3><p>Built on the U-bolt method that keeps the top flat, then checked with a straightedge before it is crated.</p><span class="gft-foot">Every welded table</span></div>
      <div class="gft-card gft-card-text"><h3>Finished your way</h3><p>Raw steel ready for oil or paint, or powder-coated legs in satin black or any RAL colour.</p><span class="gft-foot">Powder coat</span></div>
      <div class="gft-card gft-card-text"><h3>Shipped nationwide</h3><p>Kits flat-pack on a skid; welded tables crate up and ship LTL, with liftgate delivery if you have no dock.</p><span class="gft-foot">LTL freight</span></div>
    </div>
  </section>
  <section class="gft gft-final gft-final-slim">
    <p class="gft-lede gft-reveal">Questions about a build? Call the shop at <a href="{TEL}">{PHONE}</a> or <a href="{rel}contact/">send a note</a>.</p>
  </section>
</main>
'''
    write('shop/index.html', head('The shop — Gorilla Tables', 'Gorilla Tables are built by Gerarden Fabrication & Design in Denmark, Wisconsin: laser-cut, welded and checked flat in house.', rel, 'shop/') + body + footer(rel))


# -------------------------------------------------------------------------------------------------- faq ---
FAQ = [
    ('How hard is the kit to assemble?', 'If you can run a bead, you can build it. Parts are laser-cut with interlocking tabs and slots that fixture the structure square, and every table ships with a step-by-step assembly guide with a picture for each step. One person can do it with two sawhorses, a few clamps and a set of U-bolts; most customers have a table standing in an afternoon.'),
    ("What's the lead time?", 'Files are sent once your order is approved, usually the same business day. Kits typically cut and ship within 5 to 7 business days. Welded tables run 2 to 3 weeks depending on finish and queue; powder-coated builds add a few days. You get a tracking number the day it leaves Denmark.'),
    ('How does shipping work for something this heavy?', 'Tables ship LTL freight on a skid, nationwide. If you don\'t have a forklift or dock, add liftgate delivery at checkout and the driver brings it down to the ground for you.'),
    ('1/4", 3/8" or 1/2" top, which should I get?', '1/4" is flat, rigid and right for most fab and hobby work. Go 3/8" if you regularly hammer, press or build heavy weldments on your table, or you just want the extra mass in reserve. 1/2" is for the biggest frames and the hardest use. The designer shows the rated load for each.'),
    ('Do you build custom sizes?', 'Yes, that\'s the whole point. Type any size up to 60" x 120" into the designer and it prices it on the spot, with the same ribs, tabs and hole grid as the standard sizes. Need something bigger? Request a quote and we\'ll build it in sections that bolt together.'),
    ('What hole system do you use?', '5/8" holes on a 2" grid is the standard and fits the common fixture blocks, clamps and stops. 16 mm on 50 mm and 28 mm on 100 mm are a click away in the designer if that is your tooling.'),
    ('What is the rated load?', 'An engineering estimate of the evenly spread load the table carries, worked out from its own plate, ribs, legs and feet with a safety factor of 3 on the steel\'s yield strength and a sag limit of 1/16" between the legs. The designer shows which part sets the limit. It is not a certified rating.'),
    ('What do I get with the files?', 'A laser-ready DXF for every part, sorted by plate thickness, plus the customer drawing and the assembly guide. They\'re for cutting your own table; reselling the files or parts cut from them isn\'t allowed. See the file licence.'),
    ('Can I get casters and leveling feet?', 'Every table comes with 4" locking polyurethane casters, leveling feet, or leveling casters that roll and then wind down onto a foot. Pick it in the designer.'),
    ('What is the tool pan?', 'A lower shelf: 3/16" plate with 1" lips, bolted to the stand on laser-cut clips. On a kit the bend lines are slotted so you can bend the lips by hand over a bench edge; on a welded table we bend it for you.'),
]


def faq():
    rel = '../'
    items = ''.join(f'<div class="gft-faq-item"><button type="button" class="gft-faq-q">{q}</button><div class="gft-faq-a"><p>{a}</p></div></div>' for q, a in FAQ)
    schema = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]})
    body = f'''<body class="gft-page">
{header(rel, 'faq/')}
<main>
{page_head('Good questions', f'Can\'t find yours? Call the shop at <a href="{TEL}">{PHONE}</a> or <a href="{rel}contact/">send a note</a>.')}
  <section class="gft gft-faq gft-faq-page">
    <div class="gft-faq-list gft-reveal">{items}</div>
  </section>
</main>
<script type="application/ld+json">{schema}</script>
'''
    write('faq/index.html', head('FAQ — Gorilla Tables', 'Answers about Gorilla Tables fixture-block welding tables: assembly, lead times, shipping, plate thickness, custom sizes, hole systems and load ratings.', rel, 'faq/') + body + footer(rel))


# ---------------------------------------------------------------------------------------------- contact ---
def contact():
    rel = '../'
    body = f'''<body class="gft-page">
{header(rel, 'contact/')}
<main>
{page_head('Contact', 'Talk to someone who has actually built one.')}
  <section class="gft gft-contact">
    <div class="gft-contact-grid">
      <div class="gft-reveal">
        <div class="gft-contact-card">
          <b>Call the shop</b><a class="gft-big" href="{TEL}">{PHONE}</a><span>Weekdays, Central time</span>
        </div>
        <div class="gft-contact-card">
          <b>Email</b><a class="gft-big" href="mailto:{EMAIL}">{EMAIL}</a><span>Quotes, orders, questions about a build</span>
        </div>
        <div class="gft-contact-card">
          <b>The shop</b><span class="gft-big">Gerarden Fabrication &amp; Design</span><span>{ADDR}</span><a href="https://maps.google.com/?q=3190+Water+Division+Rd+Denmark+WI+54208">Directions</a>
        </div>
      </div>
      <form class="gft-form gft-reveal" id="gft-contact-form" action="mailto:{EMAIL}" method="get">
        <h2>Request a quote</h2>
        <label>Name<input name="name" required autocomplete="name"></label>
        <label>Email<input name="email" type="email" required autocomplete="email"></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
        <label>Ship-to ZIP<input name="zip" inputmode="numeric" autocomplete="postal-code"></label>
        <label class="gft-wide">What do you need?<textarea name="body" rows="5" placeholder="Size, kit or welded, top thickness, legs, anything special. Or paste a design from the designer."></textarea></label>
        <button class="gft-btn" type="submit">Send</button>
        <p class="gft-form-note">On this demo the form opens your email program with the details filled in. On the live site it will send straight to the shop.</p>
      </form>
    </div>
  </section>
</main>
'''
    write('contact/index.html', head('Contact — Gorilla Tables', 'Call, email or visit Gerarden Fabrication in Denmark, Wisconsin, or request a quote for a fixture-block welding table.', rel, 'contact/') + body + footer(rel))


# ------------------------------------------------------------------------------------------------ legal ---
DRAFT = '<div class="gft-draft">Draft for review by DeWitt LLP before the site goes live. Not yet in effect.</div>'


def legal():
    rel = '../'
    terms = f'''<body class="gft-page">
{header(rel, None)}
<main>
{page_head('Terms of sale', 'How ordering, payment, shipping and returns work for Gorilla Tables products.', DRAFT)}
  <section class="gft gft-prose">
    <h2>1. Who we are</h2>
    <p>Gorilla Tables is a brand of Gerarden Fabrication &amp; Design LLC ("Gerarden", "we"), {ADDR}. These terms apply to every order placed through fabricationtables.com, by phone or by email.</p>
    <h2>2. Products</h2>
    <p>We sell (a) laser-cut parts kits, (b) fully welded tables and (c) digital file sets for a table you design on our site. Dimensions, weights, prices and load ratings shown on the site and in the designer are generated from your design at the time you view it and may change if the design or our prices change before you order.</p>
    <h2>3. Prices and payment</h2>
    <p>Prices are in US dollars and exclude sales tax, freight and liftgate delivery, which are shown before you pay. Custom-size and custom-option prices are calculated by the designer from your design. Payment in full is due at the time of order unless we agree otherwise in writing. We may correct an obvious pricing error before accepting an order.</p>
    <h2>4. Custom work</h2>
    <p>Every table other than a standard size is built to your design. Once we have cut steel for a custom order it cannot be cancelled or returned, except for a defect in our workmanship.</p>
    <h2>5. Lead times and shipping</h2>
    <p>Lead times shown on the site are estimates. Products ship by LTL freight on a skid to the address you give us. Risk of loss passes to you when the carrier takes the shipment. Inspect the shipment before signing for it and note any damage on the delivery receipt; tell us within 48 hours of delivery so we can file a claim with the carrier.</p>
    <h2>6. Load ratings and use</h2>
    <p>Rated loads are engineering estimates for an evenly spread static load on a table standing on a flat floor, and are not certified ratings. Do not exceed them, do not use a table as a lifting point or a platform for people, and keep casters locked when working. Welding, grinding and heavy fabrication are hazardous; you are responsible for using the table safely.</p>
    <h2>7. Kits</h2>
    <p>A kit is a set of parts that you assemble and weld. The assembly guide describes one proven method; the flatness, strength and safety of the finished table depend on your work. Gerarden is not responsible for the result of assembly carried out by you or a third party.</p>
    <h2>8. Warranty</h2>
    <p>We warrant fully welded tables against defects in materials and workmanship for one year from delivery, and kit parts against defects in cutting for 30 days from delivery. The remedy is repair, replacement or refund of the affected item at our option. The warranty does not cover damage from misuse, overloading, modification, corrosion of raw steel, or assembly by anyone other than Gerarden. Except as stated here, products are provided without any other warranty, express or implied, including merchantability or fitness for a particular purpose.</p>
    <h2>9. Returns</h2>
    <p>Standard-size kits and tables in unused, uncut and unwelded condition may be returned within 14 days of delivery for a refund less return freight and a 15% restocking charge. Custom sizes, custom options, powder-coated items and digital files are not returnable.</p>
    <h2>10. Digital files</h2>
    <p>File sets are licensed, not sold, under the <a href="files.html">File licence</a>. They are delivered after we approve the order and are not refundable once delivered.</p>
    <h2>11. Limitation of liability</h2>
    <p>To the fullest extent permitted by law, Gerarden's total liability for any claim arising from an order is limited to the amount you paid for the product concerned, and Gerarden is not liable for indirect, incidental or consequential losses, including lost production or profit.</p>
    <h2>12. Law and disputes</h2>
    <p>These terms are governed by the laws of the State of Wisconsin. Any dispute will be brought in the state or federal courts for Brown County, Wisconsin.</p>
    <h2>13. Changes</h2>
    <p>We may update these terms; the version in force when you place an order applies to that order.</p>
    <p class="gft-prose-foot">Questions: <a href="mailto:{EMAIL}">{EMAIL}</a> · {PHONE}</p>
  </section>
</main>
'''
    files = f'''<body class="gft-page">
{header(rel, None)}
<main>
{page_head('File licence', 'What you may and may not do with a Gorilla Tables file set.', DRAFT)}
  <section class="gft gft-prose">
    <p>When you buy a file set from Gorilla Tables (Gerarden Fabrication &amp; Design LLC), you receive laser-cutting files, drawings and an assembly guide for the table you designed. You are buying a licence to use them, not the design itself.</p>
    <h2>You may</h2>
    <ul>
      <li>Cut one table from the files for your own use, on your own equipment or at a shop you hire to cut it for you.</li>
      <li>Keep a copy of the files for your records and cut replacement parts for that table.</li>
      <li>Modify the files to suit your own table.</li>
    </ul>
    <h2>You may not</h2>
    <ul>
      <li>Resell, share, publish, post or give away the files, in whole or in part, modified or not.</li>
      <li>Cut tables or parts from the files for sale, or for anyone other than yourself, without written permission from Gerarden.</li>
      <li>Use the Gorilla Tables name, logo or etched marks on anything you make from the files.</li>
    </ul>
    <h2>Ownership</h2>
    <p>The table design, the designer software, the drawings and the guide are the property of Gerarden Fabrication &amp; Design LLC and are protected by copyright. Each file set carries the order number it was made for.</p>
    <h2>No warranty on the result</h2>
    <p>The files describe parts that, cut and assembled as the guide shows, make a table like the one in the designer. Cutting accuracy, assembly and the flatness, strength and safety of the finished table are your responsibility.</p>
    <h2>If the licence is broken</h2>
    <p>The licence ends at once if you break these terms, and Gerarden may pursue the remedies available to it.</p>
    <p class="gft-prose-foot">Questions: <a href="mailto:{EMAIL}">{EMAIL}</a> · {PHONE}</p>
  </section>
</main>
'''
    privacy = f'''<body class="gft-page">
{header(rel, None)}
<main>
{page_head('Privacy', 'What we collect when you use the site and the designer, and what we do with it.', DRAFT)}
  <section class="gft gft-prose">
    <h2>What we collect</h2>
    <ul>
      <li><b>Designs.</b> The designer runs in your browser. A design you are working on is saved in your browser's own storage so you can come back to it; it is not sent to us until you add it to the cart, request a quote or place an order.</li>
      <li><b>Orders and quotes.</b> Your name, contact details, shipping address and the design, so we can build, ship and bill it. Payments are handled by our payment processor; we do not store card numbers.</li>
      <li><b>Site use.</b> Standard web server logs and basic analytics (pages viewed, browser type) to keep the site working and improve it.</li>
    </ul>
    <h2>How we use it</h2>
    <p>To fulfil orders, answer quotes, send order updates, and improve the site and the products. We do not sell personal information. We share it only with the carriers, payment processors and service providers needed to complete your order, and when the law requires.</p>
    <h2>Cookies</h2>
    <p>The site uses the browser storage and cookies needed for the designer, the cart and basic analytics. You can clear them in your browser at any time; a saved design will be cleared with them.</p>
    <h2>Your choices</h2>
    <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> to see, correct or delete the personal information we hold about you, or to stop marketing email.</p>
    <h2>Contact</h2>
    <p>Gerarden Fabrication &amp; Design LLC, {ADDR}, {PHONE}.</p>
  </section>
</main>
'''
    for path, title, desc, body in [('legal/terms.html', 'Terms of sale — Gorilla Tables', 'Terms of sale for Gorilla Tables kits, welded tables and file sets (draft).', terms),
                                    ('legal/files.html', 'File licence — Gorilla Tables', 'Licence terms for Gorilla Tables laser file sets (draft).', files),
                                    ('legal/privacy.html', 'Privacy — Gorilla Tables', 'Privacy notice for fabricationtables.com and the table designer (draft).', privacy)]:
        write(path, head(title, desc, rel, path) + body + footer(rel))


def extras():
    pages = ['', 'tables/', 'design/', 'how/', 'shop/', 'faq/', 'contact/', 'legal/terms.html', 'legal/files.html', 'legal/privacy.html']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in pages) + '</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
    rel = ''
    body = f'''<body class="gft-page">
{header(rel, None)}
<main>
{page_head("That page isn't here", 'The link may be old. The tables, the designer and the shop are all in the menu above.')}
  <section class="gft gft-final gft-final-slim"><div class="gft-hero-ctas gft-center"><a class="gft-btn" href="./">Home</a><a class="gft-btn gft-ghost" href="design/">Design your own</a></div></section>
</main>
'''
    write('404.html', head('Not found — Gorilla Tables', 'Page not found.', rel, '404.html') + body + footer(rel))


if __name__ == '__main__':
    home(); tables(); design(); how(); shop(); faq(); contact(); legal(); extras()
