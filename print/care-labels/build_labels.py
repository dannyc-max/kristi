"""Builds sew-on care labels for both booths, for 8.5 x 11 printable fabric sheets.

Each label is cut 2.5 x 2 in on the outer dashed line, then the 1/4 in border is
folded under and pressed (finished 2 x 1.5 in) and stitched onto the back or lining.
Run: python3 build_labels.py  -> writes care-labels.html
"""
from html import escape

FADE = "Natural fibers lighten in the sun over time."
FIXED = "Hand-dyed and set with dye fixative detergent, so colors should not bleed."

KINDS = {
    "throw": ("Hand-dyed throw", "Cotton", ["Wash cold, by itself.", FIXED, FADE]),
    "baby": ("Hand-dyed baby blanket", "Cotton double gauze", ["Wash cold, by itself.", FIXED, FADE]),
    "baby_white": ("Baby blanket", "Cotton double gauze", ["Wash cold, by itself.", FADE]),
    "ice_purse": ("Ice-dyed linen purse", "Linen, lined with denim", ["Spot clean only.", "Do not machine wash.", FADE]),
    "upholstery": ("Upholstery purse", "Upholstery fabric", ["Spot clean only.", "Do not machine wash."]),
    "treat_bag": ("Trick-or-treat bag", "Fabric", ["Spot clean, or wash cold", "and line dry."]),
}

# Counts for both booths (SHCG inventory list + Waynesville assortment plan). Edit and re-run.
SHEETS = [
    ("Sheet 1 of 2 · blankets & purses",
     ["throw"] * 4            # 2 shibori throws (SHCG) + 1 reversible throw each booth
     + ["baby"] * 3           # single-color baby blankets: 1 SHCG + 2 Waynesville
     + ["baby_white"] * 2     # white baby blanket(s) with pink bows
     + ["ice_purse"] * 1      # linen ice dye purse (SHCG)
     + ["upholstery"] * 4     # 2 upholstery purses (SHCG) + 2 clutches (Waynesville)
     + ["throw"]),            # 1 spare
    ("Sheet 2 of 2 · trick-or-treat bags · keep the unused bottom",
     ["treat_bag"] * 7),      # Waynesville
]

CSS = """
@page{size:letter;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#000;font-family:"Archivo",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;position:relative;display:grid;place-items:center;page-break-after:always}
.page:last-child{page-break-after:auto;place-items:start center;padding-top:.4in}
.note{position:absolute;top:.15in;left:0;right:0;text-align:center;font-family:"Special Elite",monospace;font-size:7pt;color:#777}
.grid{display:grid;grid-template-columns:repeat(3,2.5in);border-top:.5pt dashed #888;border-left:.5pt dashed #888}
.cut{width:2.5in;height:2in;border-right:.5pt dashed #888;border-bottom:.5pt dashed #888;padding:.25in;position:relative}
.cut::before{content:"";position:absolute;inset:.25in;border:.5pt dotted #bbb}
.lab{position:relative;height:100%;padding:.07in .09in;display:flex;flex-direction:column;gap:2pt;overflow:hidden}
.wm{display:flex;flex-wrap:wrap;gap:1pt 1.4pt;font-size:4.6pt;line-height:1;font-weight:900}
.wm span{padding:.6pt 1.4pt}
.wm .w1{font-family:"Special Elite",monospace;font-weight:400;border:.5pt solid #000}
.wm .w2{background:#000;color:#fff}
.wm .w3{font-family:"Fraunces",Georgia,serif;font-style:italic;background:#777;color:#fff}
.wm .w4{background:#c4c4c4;border:.5pt dashed #000}
.wm .w5{font-family:"Special Elite",monospace;font-weight:400;background:#999}
.wm .w6{background:#444;color:#fff}
.wm .w7{font-family:"Fraunces",Georgia,serif;font-style:italic;border:.5pt solid #000}
.wm .w8{border:.75pt solid #000}
h2{margin:0;font-size:9.5pt;font-weight:900;line-height:1.05}
.fiber{margin:0;font-family:"Special Elite",monospace;font-size:6.8pt}
.care{margin:0;font-size:6.8pt;line-height:1.25}
"""
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;900&family=Fraunces:ital,opsz,wght@1,9..144,700&family=Special+Elite&display=swap">'
WM = ('<div class="wm"><span class="w1">THE</span><span class="w2">ART</span><span class="w3">is</span><span class="w4">COMING</span>'
      '<span class="w5">from</span><span class="w6">INSIDE</span><span class="w7">the</span><span class="w8">HOUSE</span></div>')


def label(kind):
    title, fiber, care = KINDS[kind]
    return (f'<div class="cut"><div class="lab">{WM}<h2>{escape(title)}</h2><p class="fiber">{escape(fiber)}</p>'
            f'<p class="care">{" ".join(escape(c) for c in care)}</p></div></div>')


pages = "".join(
    f'<section class="page"><p class="note">{escape(note)} · printable fabric · print at 100% · cut on dashed lines, '
    f'fold the 1/4 in border under at the dotted line</p><div class="grid">{"".join(label(k) for k in kinds)}</div></section>'
    for note, kinds in SHEETS)
open("care-labels.html", "w").write(
    f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Care Labels</title>{FONTS}<style>{CSS}</style></head><body>{pages}</body></html>')
print("ok", [len(k) for _, k in SHEETS])
