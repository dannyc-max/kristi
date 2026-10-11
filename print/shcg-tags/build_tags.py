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
    dict(n=1, title="Graybeard Mtn Panoramic", lines=["Art quilt · 33 × 35 in", "Upcycled denim, hand-dyed linen & cotton double gauze"], price=770),
    dict(n=2, title="Ace of Cups", lines=["Art quilt · tarot series · 18 × 24 in"], price=650),
    dict(n=3, title="Landscape Art Quilt Sample", lines=["Made from the pattern, with binding", "and a macramé dowel hanger"], price=160),
    dict(n=4, title="Small Art Quilt", lines=["Landscape art quilt", "Smaller than 15 × 15 in"], price=250),
    dict(n=4, title="Small Art Quilt", lines=["Landscape art quilt", "Smaller than 15 × 15 in"], price=250),
    dict(n=8, title="Linen Ice Dye Purse", lines=["Large · ice-dyed linen", "Lined with denim"], price=165),
    dict(n=9, title="Upholstery Purse", lines=["Sewn from upholstery fabric", "One of a kind"], price=95),
    dict(n=9, title="Upholstery Purse", lines=["Sewn from upholstery fabric", "One of a kind"], price=95),
]
PATTERN = dict(n=5, title="Landscape Art Quilt Pattern", lines=["Pattern only, no kit", "Finishes approx. 10 × 10 in"], price=15)
KIT = dict(n=6, title="Landscape Art Quilt Kit", lines=["Pattern + fabric kit", "Finishes approx. 10 × 10 in"], price=40)
# sheet 2: 15 labels, 2.625 x 2 in: 6 patterns + 5 kits on the list, plus 2 spares of each
SHEET2 = [PATTERN] * 8 + [KIT] * 7
BOOKMARK = dict(n=10, title="Bookmark", lines=["Stitched fabric", "art bookmark"], price=15)
# sheet 3: 16 labels, 1.8 x 2.4 in: 6 bookmarks on the list, plus 10 for restocking
SHEET3 = [BOOKMARK] * 16
THROW = dict(n=7, title="Shibori Reversible Throw", lines=["Hand-dyed shibori, cotton", "Reversible · approx. 50 × 60 in"], price=185)

WORDMARK = (
    '<div class="wm" aria-label="The Art is Coming from Inside the House">'
    '<span class="a">THE</span><span class="b">ART</span><span class="c">is</span><span class="d">COMING</span>'
    '<span class="a">from</span><span class="b">INSIDE</span><span class="c">the</span><span class="d">HOUSE</span></div>'
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
.wm{display:flex;flex-wrap:wrap;gap:1.5pt 2pt;line-height:1;font-weight:900}
.wm span{padding:1pt 2.5pt;display:inline-block}
.wm .a{font-family:"Special Elite",monospace;font-weight:400;border:.75pt solid #000}
.wm .b{background:#000;color:#fff;font-family:"Archivo",sans-serif;font-weight:900}
.wm .c{font-family:"Fraunces",Georgia,serif;font-style:italic;font-weight:700;border:.75pt solid #000}
.wm .d{font-family:"Archivo",sans-serif;font-weight:900;border:.75pt dashed #000}
h2{margin:0;font-weight:900;line-height:1.05}
.lines{margin:0;line-height:1.25}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:6pt}
.who{font-family:"Special Elite",monospace;line-height:1.25}
.price{font-weight:900;font-variant-numeric:tabular-nums;line-height:1}
.inv{font-family:"Special Elite",monospace;color:#000}

/* large: 4 x 2.5 */
.L .tag{width:4in;height:2.5in;gap:5pt}
.L .wm{font-size:7pt}
.L h2{font-size:15pt}
.L .lines{font-size:8.5pt}
.L .who{font-size:7pt}
.L .price{font-size:22pt}
/* medium: 2.625 x 2 */
.M .tag{width:2.625in;height:2in;gap:4pt;padding:.1in .11in}
.M .wm{font-size:5pt;gap:1pt 1.5pt}
.M .wm span{padding:.7pt 1.6pt}
.M h2{font-size:10.5pt}
.M .lines{font-size:7pt}
.M .who{font-size:5.6pt}
.M .price{font-size:16pt}
/* small: 1.8 x 2.4 */
.S .tag{width:1.8in;height:2.4in;gap:4pt;padding:.1in .1in}
.S .wm{font-size:4.6pt;gap:1pt 1.4pt}
.S .wm span{padding:.6pt 1.4pt}
.S h2{font-size:11pt}
.S .lines{font-size:7pt}
.S .foot{flex-direction:column;align-items:flex-start;gap:3pt}
.S .who{font-size:5.4pt}
.S .price{font-size:16pt}
/* cardstock throw tag: 3.5 x 5, hole at top */
.T .tag{width:3.5in;height:5in;gap:7pt;padding:.5in .22in .2in}
.T .hole{position:absolute;top:.16in;left:50%;width:.22in;height:.22in;margin-left:-.11in;border:.75pt solid #000;border-radius:50%}
.T .wm{font-size:8pt}
.T h2{font-size:17pt}
.T .lines{font-size:9.5pt}
.T .care{font-size:8pt;line-height:1.3;border-top:.75pt solid #000;padding-top:5pt}
.T .who{font-size:7.5pt}
.T .price{font-size:26pt}
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Fraunces:ital,opsz,wght@1,9..144,700&family=Special+Elite&display=swap">'


def tag(item, extra=""):
    lines = "<br>".join(escape(l) for l in item["lines"])
    return (
        f'<div class="tag">{extra}{WORDMARK}'
        f'<h2>{escape(item["title"])}</h2><p class="lines">{lines}</p>'
        f'<div class="foot"><div class="who">{ARTIST}<br>{HANDLE}<br><span class="inv">CORIDEN #{item["n"]}</span></div>'
        f'<div class="price">${item["price"]}</div></div></div>'
    )


def page(cls, cols, items, note):
    cells = "".join(tag(i) for i in items)
    return (f'<section class="page {cls}"><p class="note">{escape(note)}</p>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},auto)">{cells}</div></section>')


def doc(title, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{FONTS}'
            f'<style>{CSS}</style></head><body>{body}</body></html>')


stickers = doc("SHCG Sticker Tags", "".join([
    page("L", 2, ART, "Sheet 1 of 3 · art quilts & purses · Avery 5265 · print at 100%, black and white · cut on dashed lines"),
    page("M", 3, SHEET2, "Sheet 2 of 3 · patterns (8) & kits (7), includes 2 spares of each · cut on dashed lines"),
    page("S", 4, SHEET3, "Sheet 3 of 3 · bookmarks (16), 6 for the list + 10 for restocking · cut on dashed lines"),
]))
open("sticker-sheets.html", "w").write(stickers)

care = ('<p class="care">Colorway: ______________________<br><br>Hand-dyed, so every one is different.<br>'
        'Wash cold with like colors. Tumble dry low.<br>Gets softer with every wash.</p>')
throw_tag = tag(THROW, '<span class="hole"></span>').replace('<div class="foot">', care + '<div class="foot">')
throws = doc("SHCG Throw Tags", (
    '<section class="page T"><p class="note">Cardstock · print at 100%, black and white · cut on dashed lines, punch the circle, '
    'thread 3/8 in pink ribbon · 2 for the throws + 2 spares</p>'
    f'<div class="grid" style="grid-template-columns:repeat(2,auto)">{throw_tag * 4}</div></section>'))
open("throw-tags-cardstock.html", "w").write(throws)
print("ok")
