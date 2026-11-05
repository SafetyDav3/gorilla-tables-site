# Gorilla Tables — website demo

A static copy of fabricationtables.com rebranded to Gorilla Tables, with the Gorilla Tables designer added as the
product configurator. It shows the web developer what the live site should do. See `webdev/index.html` (also
served at /webdev/) for how the pieces fit and what the live site needs.

- Pages: `index.html` (home), `tables/` (standard tables: the designer's Standard tables tab, plus the price list), `design/` (the designer full screen), `how/` (kit or welded), `shop/`, `faq/`, `contact/`, `legal/` (drafts for legal review)
- `design/app.html`: the table designer, customer version (one self-contained file, built from the private source repository)
- `tools/build_site.py`: generates every page from one shared header, footer and head

Built from the private repository `SafetyDav3/gorilla-tables-source`. This repository holds only built files.

Copyright 2026 Gerarden Fabrication & Design LLC. All rights reserved. The files here are for Gerarden
Fabrication's own use and for its contractors working on fabricationtables.com; see LICENSE.
