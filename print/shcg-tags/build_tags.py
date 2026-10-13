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
.grid{display:grid;border-top:.5pt dashed #999;border-left:.5pt dashed #999}
.tag{border-right:.5pt dashed #999;border-bottom:.5pt dashed #999;padding:.12in .14in;display:flex;flex-direction:column;overflow:hidden;position:relative}
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
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Fraunces:ital,opsz,wght@1,9..144,700&family=Special+Elite&display=swap">'


def tag(item, extra=""):
    lines = "<br>".join(escape(l) for l in item["lines"])
    return (
        f'<div class="tag">{extra}{NEEDLE}{WORDMARK}'
        f'<h2>{escape(item["title"])}</h2><p class="lines">{lines}</p>'
        f'<div class="price">${item["price"]}</div>'
        f'<div class="foot">{SCISSORS}<div class="qrbox">{QR}<div class="who">{ARTIST}<br>Scan for the website<br>'
        f'Instagram <span class="hd">{HANDLE}</span><br>CORIDEN #{item["n"]}</div></div></div></div>'
    )


QR = open("qr-website.svg").read()  # links to theartiscomingfrominsidethehouse.com

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
        f'<div class="bottom"><div class="qrbox">{QR}<div class="who">{ARTIST}<br>Scan for the website<br>'
        f'Instagram <span class="hd">{HANDLE}</span><br>CORIDEN #{item["n"]}</div></div>'
        f'{SCISSORS}<div class="price">${item["price"]}</div></div></div>'
    )


def page(cls, cols, items, note, rows=ROWS3):
    cells = "".join(tag_mid(i, rows) for i in items)
    return (f'<section class="page {cls}"><p class="note">{escape(note)}</p>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},auto)">{cells}</div></section>')


def doc(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{FONTS}'
            f'<style>{CSS}</style></head><body>{body}</body></html>')


stickers = doc("SHCG Sticker Tags", "".join([
    page("L", 2, ART, "Sheet 1 of 2 · art quilts & purses · Avery 5265 · print at 100%, black and white · cut on dashed lines"),
    page("M", 3, SHEET2, "Sheet 2 of 2 · patterns (8) & kits (7), includes 2 spares of each · cut on dashed lines"),
]))
open("sticker-sheets.html", "w").write(stickers)

care = ('<p class="care">Colorway: ______________________<br><br>'
        '<b>Care:</b> Wash cold, by itself. Do not wash with anything else.<br><br>'
        'Hand-dyed and treated with a dye fixative detergent, so colors should not bleed. '
        'Natural fibers will lighten naturally in the sun over time.</p>')
throw_tag = tag(THROW, '<span class="hole"></span>').replace('<div class="price">', care + '<div class="price">')
throws = doc("SHCG Throw Tags", (
    '<section class="page T"><p class="note">Cardstock · print at 100% · cut on dashed lines, punch circle, '
    'pink ribbon · keep the unused bottom half</p>'
    f'<div class="grid" style="grid-template-columns:repeat(2,auto)">{throw_tag * 2}</div></section>'))
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
.B .bottom .who{text-align:center;font-size:5.4pt}
.B .qr{width:.6in;height:.6in}
.B .bottom .scissors{order:2;width:.55in}
.B .bottom .price{order:1;font-size:20pt;text-align:center}
"""
bookmarks = doc("SHCG Bookmark Labels", (
    '<style>' + bm_css + '</style><section class="page B"><p class="note">Avery 8363 · 2 x 4 in labels · print at 100% · '
    'test on plain paper first · 6 for the list + 4 for restocking</p>' + "".join(cells) + '</section>'))
open("bookmark-labels-8363.html", "w").write(bookmarks)
print("ok")
