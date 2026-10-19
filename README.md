# The Art is Coming from Inside the House: website

Static site, no build step. Open `index.html` in a browser.

- `index.html`: home (art, process, Stitch Library teaser, shop, journal, fairs, newsletter sign-up)
- `techniques.html`: Stitch Library, one card per technique from the landscape pattern
- `dye.html`: Dye Notes (supplies, methods, dye log, truffle post). Add a log entry per batch
- `assets/site.css`: shared styles and brand colors
- `assets/logo/`: logo in SVG, transparent PNG and cream PNG
- `print/signup-sheet.html`: clipboard sign-up sheet for the booth
- `docs/marketing-plan.md`: email rhythm, timely topics, pricing research, Stitch Library plan
- `docs/welcome-email.md`: welcome email draft

## To do before it goes live
- Photos still needed: runners, placemats, Ace of Cups, Graybeard, and the turned edge, roving and hand-stitch cards
- Prices are left off the site on purpose until there is online shopping or Etsy listings
- The Join page sign-up form adds each sign-up to Kristi's private Google Sheet ("Website email sign-ups") via `SHEET_URL` in `join.html` (script: `docs/signup-sheet-script.gs`)
- Stitch Library "Watch the reel" links are hidden until the real reels are in (look for the HTML comments). Process page video cards can show a screenshot: add <img class="thumb"> as the card's first line
- Add the 2012 upcycling posts to the journal
