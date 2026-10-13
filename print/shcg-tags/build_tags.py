"""Builds the SHCG hang tags (black and white) as HTML pages.

Sticker sheets: Avery 5265 full-sheet labels, letter size, cut apart by hand.
Throw tags: letter cardstock, cut out and hole-punched for ribbon.
Run: python3 build_tags.py  -> writes sticker-sheets.html and throw-tags-cardstock.html
"""
from html import escape

ARTIST = "Kristi Coriden"
HANDLE = "@artiscomingfrominsidethehouse"

# From the SHCG inventory list sent to Local Cloth (Oct 9). n = line on the list.
ART = [  # sheet 1: large tags, 4 x 2.5 in, to stick on cardstock or the back of a piece
    dict(n=1, title="Graybeard Mtn Panoramic", lines=["Art quilt · 33 × 35 in · Framed · Signed", "Hand-dyed linen, rayon & cotton (shibori & ice dyeing)", "with upcycled denim & cotton", "Hand-finished; quilted with seed stitch & couching"], price=770),
    dict(n=2, title="Ace of Cups", lines=["Art quilt · tarot series · 18 × 24 in", "Signed in thread: KJC"], price=650),
    dict(n=3, title="Landscape Art Quilt Sample", lines=["Made from the pattern, with binding", "and a macramé dowel hanger"], price=160),
    dict(n=4, title="Clouds and Sunset", lines=["Small art quilt"], price=250),
    dict(n=4, title="Elemental Landscapes", lines=["Small art quilt"], price=250),
    dict(n=8, title="Linen Ice Dye Purse", lines=["Large · ice-dyed linen", "Lined with denim"], price=165),
    dict(n=9, title="Upholstery Purse", lines=["Sewn from upholstery fabric", "One of a kind"], price=95),
    dict(n=9, title="Upholstery Purse", lines=["Sewn from upholstery fabric", "One of a kind"], price=95),
]
PATTERN = dict(n=5, title="Landscape Art Quilt Pattern", lines=["Pattern only, no kit", "Finishes approx. 10 × 10 in"], price=15)
KIT = dict(n=6, title="Landscape Art Quilt Kit", lines=["Pattern + fabric kit", "Finishes approx. 10 × 10 in"], price=40)
# sheet 2: 15 labels, 2.625 x 2 in: 6 patterns + 5 kits on the list, plus 2 spares of each
SHEET2 = [PATTERN] * 8 + [KIT] * 7
BOOKMARK = dict(n=10, title="Bookmark", lines=["Stitched fabric", "art bookmark"], price=15)
# Bookmarks go on one sheet of 2 x 4 in labels (Avery 8363/5163 layout, 10 per sheet):
# 6 on the list + 4 that stay on the sheet for restocking.
THROW = dict(n=7, title="Shibori Reversible Throw", lines=["Hand-dyed shibori, cotton", "Reversible · approx. 50 × 60 in"], price=185)

WORDMARK = (
    '<div class="wm" aria-label="The Art is Coming from Inside the House">'
    '<span class="w1">THE</span><span class="w2">ART</span><span class="w3">is</span><span class="w4">COMING</span>'
    '<span class="w5">from</span><span class="w6">INSIDE</span><span class="w7">the</span><span class="w8">HOUSE</span></div>'
)

# Needle with thread, drawn across the top of each tag.
NEEDLE = (
    '<svg class="needle" viewBox="0 0 300 16" preserveAspectRatio="none" aria-hidden="true">'
    '<path d="M2,9 C20,1 34,15 52,8 S80,4 92,8" fill="none" stroke="#777" stroke-width="1.2"/>'
    '<path d="M92,8 C92,5.6 96,5.4 102,5.6 L290,7.6 L299,8 L290,8.4 L102,10.4 C96,10.6 92,10.4 92,8 Z" fill="#555"/>'
    '<rect x="97" y="7.3" width="9" height="1.4" rx=".7" fill="#fff"/>'
    '<path d="M101,8 L292,8" stroke="#bbb" stroke-width=".5"/>'
    '</svg>'
)

# Small stork embroidery scissors (Gingher style): handles are the legs, blades are the beak.
SCISSORS = (
    '<svg class="scissors" viewBox="0 0 64 26" aria-hidden="true">'
    '<ellipse cx="8" cy="7" rx="6" ry="4.6" fill="none" stroke="#000" stroke-width="1.6"/>'
    '<ellipse cx="8" cy="19" rx="6" ry="4.6" fill="none" stroke="#000" stroke-width="1.6"/>'
    '<path d="M13.5,9 L19,12 M13.5,17 L19,14" stroke="#000" stroke-width="1.6" fill="none"/>'
    '<path d="M17,13 C18,7 26,5.5 33,8.5 C36,10 37,12 36,13.6 C33,18 24,19.5 17,13 Z" fill="#888" stroke="#000" stroke-width=".9"/>'
    '<path d="M21,12 C25,10 29,10.5 32,12.5" fill="none" stroke="#000" stroke-width=".7"/>'
    '<circle cx="37.5" cy="10.5" r="3.4" fill="#555" stroke="#000" stroke-width=".8"/>'
    '<circle cx="38.4" cy="9.8" r=".8" fill="#fff"/>'
    '<path d="M40.5,10 L63,12.2 L40.5,11.6 Z" fill="#000"/>'
    '<path d="M40.5,12 L63,12.6 L40,13.4 Z" fill="#555"/>'
    '<circle cx="31" cy="12.4" r="1" fill="#000"/>'
    '</svg>'
)

CSS = """
@page{size:letter;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#000;font-family:"Archivo",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;display:grid;place-items:center;page-break-after:always;position:relative}
.page:last-child{page-break-after:auto}
.note{position:absolute;top:.12in;left:0;right:0;text-align:center;font-family:"Special Elite",monospace;font-size:7pt;color:#777}
.grid{display:grid}
.tag{padding:.12in .14in;display:flex;flex-direction:column;overflow:hidden;position:relative}
.wm{display:flex;flex-wrap:wrap;justify-content:center;gap:2pt 2.5pt;line-height:1;font-weight:900;margin:0 auto}
.wm span{padding:1.2pt 3pt;display:inline-block}
.wm .w1{font-family:"Special Elite",monospace;font-weight:400;border:.75pt solid #000;transform:rotate(-3deg)}
.wm .w2{background:#000;color:#fff;transform:rotate(2deg)}
.wm .w3{font-family:"Fraunces",Georgia,serif;font-style:italic;font-weight:700;background:#777;color:#fff;transform:rotate(-2deg)}
.wm .w4{background:#c4c4c4;color:#000;border:.75pt dashed #000;transform:rotate(1deg)}
.wm .w5{font-family:"Special Elite",monospace;font-weight:400;background:#999;color:#000;transform:rotate(-1.5deg)}
.wm .w6{background:#444;color:#fff;border:.75pt dashed #444;box-shadow:0 0 0 .75pt #000;transform:rotate(-1deg)}
.wm .w7{font-family:"Fraunces",Georgia,serif;font-style:italic;font-weight:700;border:.75pt solid #000;transform:rotate(2deg)}
.wm .w8{border:1.25pt solid #000;transform:rotate(1deg)}
.tag{align-items:center;text-align:center}
.needle{display:block;width:100%;height:9pt;flex:none}
h2{margin:0;font-weight:900;line-height:1.05}
.lines{margin:0;line-height:1.25;color:#222}
.price{font-weight:900;font-variant-numeric:tabular-nums;line-height:1}
.foot{margin-top:auto;display:flex;flex-direction:column;align-items:center;gap:2pt}
.scissors{display:block;height:auto}
.who{font-family:"Special Elite",monospace;line-height:1.25;color:#333}

/* large: 4 x 2.5 */
.L .tag{width:4in;height:2.5in;gap:4pt}
.L .wm{font-size:8.5pt}
.L h2{font-size:15pt}
.L .lines{font-size:8.5pt}
.L .price{font-size:20pt}
.L .scissors{width:.75in}
.L .who{font-size:6.6pt}
/* medium: 2.625 x 2 */
.M .tag{width:2.625in;height:2in;gap:3pt;padding:.09in .11in}
.M .needle{height:7pt}
.M .wm{font-size:5.6pt;gap:1.5pt 2pt}
.M .wm span{padding:.8pt 2pt}
.M h2{font-size:10pt}
.M .lines{font-size:6.8pt}
.M .price{font-size:14pt}
.M .scissors{width:.45in}
.M .who{font-size:5pt}
/* small: 1.8 x 2.4 */
.S .tag{width:1.8in;height:2.4in;gap:3.5pt;padding:.1in .1in}
.S .needle{height:7pt}
.S .wm{font-size:5.2pt;gap:1.5pt 1.8pt}
.S .wm span{padding:.7pt 1.8pt}
.S h2{font-size:11pt}
.S .lines{font-size:7pt}
.S .price{font-size:15pt}
.S .scissors{width:.45in}
.S .who{font-size:4.8pt}
.S .sep{display:none}
.S .hd{display:block}
/* cardstock throw tag: 3.5 x 5, hole at top */
.T{place-items:start center;padding-top:.4in}
.T .tag{width:3.5in;height:5in;gap:4pt;padding:.42in .22in .14in}
.T .hole{position:absolute;top:.14in;left:50%;width:.22in;height:.22in;margin-left:-.11in;border:.75pt solid #000;border-radius:50%}
.T .needle{height:11pt}
.T .wm{font-size:10pt}
.T h2{font-size:17pt}
.T .lines{font-size:9.5pt}
.T .care{font-size:7.6pt;line-height:1.3;border-top:.75pt solid #777;padding-top:6pt;width:100%;margin:0}
.T .price{font-size:22pt}
.T .scissors{width:.75in}
.T .who{font-size:7pt}
/* logo-in-the-middle layout (all tags except the throws) */
.tag.mid{gap:3pt}
.mid h2{order:0}
.logo-zone{flex:1 1 auto;display:grid;place-items:center;width:100%;min-height:0}
.wm.stack{display:flex;flex-direction:column;align-items:center;gap:3pt}
.wm.stack .row{display:flex;justify-content:center;gap:3pt}
.wm.stack span{padding:2pt 5pt}
.bottom{display:flex;align-items:flex-end;justify-content:space-between;width:100%;gap:6pt}
.bottom .who{text-align:left}
.bottom .price{text-align:right}
.L .mid .needle,.M .mid .needle{height:6pt}
.L .mid h2{font-size:14pt}
.L .mid .lines{font-size:8pt}
.L .wm.stack{font-size:13.5pt;gap:2pt}
.L .dense .wm.stack{font-size:10pt;gap:1.5pt}
.L .dense .wm.stack .row{gap:2pt}
.L .dense .wm.stack span{padding:1.4pt 3.5pt}
.L .bottom .price{font-size:18pt}
.L .bottom .scissors{width:.55in}
.L .bottom .who{font-size:5.6pt}
.M .tag.mid{gap:2pt}
.M .mid h2{font-size:9.5pt}
.M .mid .lines{font-size:6.4pt}
.M .wm.stack{font-size:11.5pt;gap:2pt}
.M .wm.stack .row{gap:2pt}
.M .wm.stack span{padding:1.2pt 3.2pt}
.M .bottom .price{font-size:13pt}
.M .bottom .scissors{width:.38in}
.M .bottom .who{font-size:4.2pt}
/* QR code to the website, with the Instagram call-out beside it */
.qrbox{display:flex;align-items:center;gap:4pt;text-align:left}
.qr{display:block;flex:none;width:.55in;height:.55in}
.L .qr{width:.58in;height:.58in}
.M .qr{width:.5in;height:.5in}
.M .qrbox .who{font-size:4.4pt}
.T .qr{width:.68in;height:.68in}
.T .qrbox .who{font-size:7pt;text-align:left}
/* back of tag */
.page.top{place-items:start center;padding-top:.4in}
.tag.back{align-items:center;justify-content:center;gap:5pt}
.back .bk{display:flex;align-items:center;justify-content:center;gap:10pt;width:100%}
.back .qrcol{display:flex;flex-direction:column;align-items:center;gap:3pt;flex:none}
.back .scan{margin:0;text-align:center;font-weight:700;line-height:1.2}
.back .contact{margin:0;text-align:left;font-family:"Special Elite",monospace;line-height:1.45;min-width:0;overflow-wrap:anywhere}
.back .contact b{font-family:"Archivo",sans-serif;font-weight:900}
.L .back .qr{width:1.15in;height:1.15in}
.L .back .qrcol{width:1.45in}
.L .back .scan{font-size:6.6pt}
.L .back .contact{font-size:7pt}
.L .back .wm{font-size:7pt}
.M .tag.back{gap:3pt}
.M .back .bk{gap:6pt}
.M .back .qr{width:.9in;height:.9in}
.M .back .qrcol{width:1.05in}
.M .back .scan{font-size:5pt}
.M .back .contact{font-size:4.8pt}
.M .back .wm{font-size:4.6pt;gap:1pt 1.4pt}
.M .back .wm span{padding:.6pt 1.4pt}
.T .tag.back{justify-content:flex-start;padding-top:.5in;gap:10pt}
.T .back .bk{flex-direction:column;gap:12pt}
.T .back .qr{width:1.6in;height:1.6in}
.T .back .qrcol{width:2.4in}
.T .back .scan{font-size:10pt}
.T .back .contact{font-size:8.5pt;text-align:center}
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Fraunces:ital,opsz,wght@1,9..144,700&family=Special+Elite&display=swap">'


def tag(item, extra=""):
    lines = "<br>".join(escape(l) for l in item["lines"])
    return (
        f'<div class="tag">{extra}{NEEDLE}{WORDMARK}'
        f'<h2>{escape(item["title"])}</h2><p class="lines">{lines}</p>'
        f'<div class="price">${item["price"]}</div>'
        f'<div class="foot">{SCISSORS}<div class="who">{ARTIST} · {MEMBER}</div></div></div>'
    )


QR = open("qr-signup.svg").read()  # opens the newsletter sign-up page
EMAIL = "kristicoriden@gmail.com"
ETSY = "etsy.com/shop/ArtHouseArtQuilts"
MEMBER = "Local Cloth member"

WORDS = {"THE": "w1", "ART": "w2", "is": "w3", "COMING": "w4", "from": "w5", "INSIDE": "w6", "the": "w7", "HOUSE": "w8"}
ROWS3 = [["THE", "ART", "is"], ["COMING", "from"], ["INSIDE", "the", "HOUSE"]]
ROWS4 = [["THE", "ART"], ["is", "COMING"], ["from", "INSIDE"], ["the", "HOUSE"]]


def stacked_logo(rows):
    """The logo stacked into rows so it reads as a squarer block."""
    body = "".join('<div class="row">' + "".join(f'<span class="{WORDS[w]}">{w}</span>' for w in r) + "</div>" for r in rows)
    return f'<div class="wm stack" aria-label="The Art is Coming from Inside the House">{body}</div>'


def tag_mid(item, rows):
    """Name, then description, then the logo filling the middle, then price, scissors and maker."""
    lines = "<br>".join(escape(l) for l in item["lines"])
    return (
        f'<div class="tag mid{" dense" if len(item["lines"]) >= 4 else ""}">{NEEDLE}'
        f'<h2>{escape(item["title"])}</h2><p class="lines">{lines}</p>'
        f'<div class="logo-zone">{stacked_logo(rows)}</div>'
        f'<div class="bottom"><div class="who">{ARTIST}<br>{MEMBER}</div>'
        f'{SCISSORS}<div class="price">${item["price"]}</div></div></div>'
    )



def back(extra=""):
    """Back of a tag: QR to the newsletter sign-up, then Instagram, Etsy, email, Local Cloth member."""
    return (
        f'<div class="tag back">{extra}{WORDMARK}<div class="bk">'
        f'<div class="qrcol">{QR}<p class="scan">Scan to get email announcements about upcoming in-person events</p></div>'
        f'<p class="contact"><b>Instagram</b> {HANDLE}<br><b>Etsy</b> {ETSY}<br><b>Email</b> {EMAIL}<br>{MEMBER}</p>'
        f'</div></div>'
    )


def backs(cls, cols, count, note):
    cells = back() * count
    return (f'<section class="page {cls} top"><p class="note">{escape(note)}</p>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},auto)">{cells}</div></section>')


def page(cls, cols, items, note, rows=ROWS3):
    cells = "".join(tag_mid(i, rows) for i in items)
    return (f'<section class="page {cls}"><p class="note">{escape(note)}</p>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},auto)">{cells}</div></section>')


def doc(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{FONTS}'
            f'<style>{CSS}</style></head><body>{body}</body></html>')


stickers = doc("SHCG Sticker Tags", "".join([
    page("L", 2, ART, "Sheet 1 of 4 · FRONTS · art quilts & purses · Avery 5265 · print at 100%, black and white"),
    page("M", 3, SHEET2, "Sheet 2 of 4 · FRONTS · patterns (8) & kits (7), includes 2 spares of each"),
    backs("L", 2, 8, "Sheet 3 of 4 · BACKS · art quilts & purses · stick on the back of each cardstock tag"),
    backs("M", 3, 12, "Sheet 4 of 4 · BACKS · patterns & kits · fits the 7/8 sheet (top 4 rows)"),
]))
open("sticker-sheets.html", "w").write(stickers)

# Colour version of the art & purse fronts, in the logo palette
COLOR_CSS = """
.color{color:#4A2436}
.color .tag{color:#4A2436}
.color .lines{color:#4A2436}
.color .wm .w1{background:#4A2436;color:#F1EBDF;border-color:#4A2436}
.color .wm .w2{background:#A14B34;color:#F1EBDF}
.color .wm .w3{background:#fff;color:#1B3F8D;border:.9pt solid #1B3F8D}
.color .wm .w4{background:#8C9DAF;color:#4A2436;border-color:#4A2436}
.color .wm .w5{background:#5A5C2E;color:#F1EBDF}
.color .wm .w6{background:#1B3F8D;color:#F1EBDF;border-color:#1B3F8D;box-shadow:none}
.color .wm .w7{background:#6E8B67;color:#F1EBDF;border-color:#6E8B67}
.color .wm .w8{background:#F1EBDF;color:#4A2436;border-color:#4A2436}
.color .price{color:#000}
.color .who{color:#4A2436}
"""
color = doc("SHCG Art Tags Color", "<style>" + COLOR_CSS + "</style>" + page(
    "L color", 2, ART, "COLOR · art quilts & purses fronts · Avery 5265 · print at 100%"))
open("art-tags-color.html", "w").write(color)

care = ('<p class="care">Colorway: ______________________<br><br>'
        '<b>Care:</b> Wash cold, by itself. Do not wash with anything else.<br><br>'
        'Hand-dyed and treated with a dye fixative detergent, so colors should not bleed. '
        'Natural fibers will lighten naturally in the sun over time.</p>')
throw_tag = tag(THROW, '<span class="hole"></span>').replace('<div class="price">', care + '<div class="price">')
throws = doc("SHCG Throw Tags", (
    '<section class="page T"><p class="note">Cardstock · print at 100%, punch circle, '
    'pink ribbon · keep the unused bottom half</p>'
    f'<div class="grid" style="grid-template-columns:repeat(2,auto)">{throw_tag * 2}</div></section>'
    '<section class="page T"><p class="note">BACK · print double-sided, flip on long edge</p>'
    f'<div class="grid" style="grid-template-columns:repeat(2,auto)">{back(chr(60)+"span class=hole></span>") * 2}</div></section>'))
open("throw-tags-cardstock.html", "w").write(throws)
# 2 x 4 label sheet: 2 columns x 5 rows, 0.5 in top margin, 0.156 in side margin, 0.1875 in gutter.
# Each label is printed sideways so it reads top to bottom on a 2 in wide bookmark.
cells = []
for i in range(10):
    col, row = i % 2, i // 2
    left, top = 0.15625 + col * (4 + 0.1875), 0.5 + row * 2
    cells.append(f'<div class="cell" style="left:{left}in;top:{top}in"><div class="rot">{tag_mid(BOOKMARK, ROWS4)}</div></div>')
bm_css = """
.B{display:block;overflow:hidden}
.B .cell{position:absolute;width:4in;height:2in}
.B .rot{position:absolute;left:1in;top:-1in;width:2in;height:4in;transform:rotate(90deg)}
.B .tag{width:2in;height:4in;border:0;gap:5pt;padding:.16in .14in}
.B .needle{height:7pt}
.B h2{font-size:16pt}
.B .lines{font-size:8.5pt}
.B .wm.stack{font-size:15pt;gap:4pt}
.B .wm.stack .row{gap:3pt}
.B .bottom{flex-direction:column;align-items:center;gap:3pt}
.B .bottom .qrbox{order:3;flex-direction:column;gap:2pt}
.B .bottom .who{order:3;text-align:center;font-size:5.4pt}
.B .qr{width:.6in;height:.6in}
.B .bottom .scissors{order:2;width:.55in}
.B .bottom .price{order:1;font-size:20pt;text-align:center}
"""
bookmarks = doc("SHCG Bookmark Labels", (
    '<style>' + bm_css + '</style><section class="page B"><p class="note">Avery 8363 · 2 x 4 in labels · print at 100% · '
    'test on plain paper first · 6 for the list + 4 for restocking</p>' + "".join(cells) + '</section>'))
open("bookmark-labels-8363.html", "w").write(bookmarks)
open("bookmark-labels-8363-color.html", "w").write(
    bookmarks.replace('<section class="page B">', '<style>' + COLOR_CSS + '</style><section class="page B color">'))
# --- Colour backs, sized a little larger than the fronts so the back frames the piece ---
CELL_CSS = """
.sheet{display:grid}
.cell{position:relative;overflow:hidden}
.cell .tag{border:0}
"""
# Art & purse backs: 5 x 3.5 in (the 4 x 2.5 front plus 1/2 in all around).
# Printed sideways, 4 to a sheet, so the 8 backs take 2 sheets instead of 3.
XL_CSS = """
.XL .cell{width:3.5in;height:5in}
.XL .rot{position:absolute;left:-.75in;top:.75in;width:5in;height:3.5in;transform:rotate(90deg)}
.XL .tag{width:5in;height:3.5in;padding:.22in .3in;gap:9pt}
.XL .back .wm{font-size:10pt}
.XL .back .bk{gap:16pt}
.XL .back .qr{width:1.45in;height:1.45in}
.XL .back .qrcol{width:1.75in}
.XL .back .scan{font-size:7.8pt}
.XL .back .contact{font-size:8pt}
"""
# Bookmark backs: 2 x 5 in. Same 2 in width as the bookmark, 1/2 in longer than the
# 2 x 4 front at each end. 8 on one sheet (6 on the list + 2 spares).
BB_CSS = """
.BB .cell{width:2in;height:5in}
.BB .tag{width:2in;height:5in;padding:.22in .14in;justify-content:center;gap:12pt}
.BB .back .wm{font-size:9pt}
.BB .back .bk{flex-direction:column;gap:12pt}
.BB .back .qr{width:1.35in;height:1.35in}
.BB .back .qrcol{width:1.6in;gap:5pt}
.BB .back .scan{font-size:7pt}
.BB .back .contact{font-size:6.4pt;text-align:center}
"""


def sheet(cls, cols, cells, note):
    return (f'<section class="page {cls} color"><p class="note">{escape(note)}</p>'
            f'<div class="sheet" style="grid-template-columns:repeat({cols},auto)">{cells}</div></section>')


def colordoc(title, extra_css, body):
    return doc(title, "<style>" + COLOR_CSS + CELL_CSS + extra_css + "</style>" + body)


xl = '<div class="cell"><div class="rot">' + back() + '</div></div>'
art_backs = colordoc("SHCG Art Backs Color", XL_CSS, "".join(
    sheet("XL", 2, xl * 4, f"COLOR · BACKS {k} of 2 · art quilts & purses · 5 x 3.5 in · Avery 5265 · print at 100%")
    for k in (1, 2)))
open("art-backs-color.html", "w").write(art_backs)

bm_backs = colordoc("SHCG Bookmark Backs Color", BB_CSS, sheet(
    "BB", 4, ('<div class="cell">' + back() + '</div>') * 8,
    "COLOR · bookmark BACKS · 2 x 5 in · Avery 5265 · print at 100% · 6 + 2 spares"))
open("bookmark-backs-color.html", "w").write(bm_backs)

# Shibori throw tags in colour: 4 on one sheet of cardstock, double-sided.
# The grid is centred, so flipping on the long edge lines the backs up with the fronts.
TC_CSS = """
.TC{place-items:start;padding:0}
.TC .note{display:none}
.TC .cell{width:4.25in;height:5.5in}
.TC .tag{width:4.25in;height:5.5in;padding:.5in .4in .3in}
.TC .tag.mid,.TC .tag:not(.back){gap:7pt}
.TC .tag:not(.back) .wm{font-size:11.5pt}
.TC .tag:not(.back) h2{font-size:20pt}
.TC .tag:not(.back) .lines{font-size:10.5pt}
.TC .care{font-size:8.6pt}
.TC .tag:not(.back) .price{font-size:26pt}
.TC .back .wm{font-size:11pt}
"""
hole = '<span class="hole"></span>'
throws_color = colordoc("SHCG Throw Tags Color", TC_CSS, (
    sheet("T TC", 2, ('<div class="cell">' + throw_tag + '</div>') * 4,
          "COLOR · FRONT · Shibori throw tags · cardstock · print at 100% · 2 for SHCG + 2 for Waynesville") +
    sheet("T TC", 2, ('<div class="cell">' + back() + '</div>') * 4,
          "BACK · print double-sided, flip on long edge")))
open("throw-tags-color.html", "w").write(throws_color)
print("ok")
