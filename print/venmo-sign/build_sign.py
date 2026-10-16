# Venmo sign insert, 4 in wide x 5 in tall, for the acrylic sign holder at the booth.
# 1/4 in border, 3.5 in QR top-centred inside it, short call-out underneath.
# The QR is static (no redirect service), so it never expires. It points at the
# newsletter page rather than the PDF, so the pattern file can change without a reprint.
# Run: python3 build_sign.py   -> venmo-sign.html, venmo-sign.pdf, venmo-sign.png (300 dpi)
import segno
from playwright.sync_api import sync_playwright

URL = "https://theartiscomingfrominsidethehouse.com/join.html"

qr = segno.make(URL, error="q")
QR = qr.svg_inline(scale=1, border=4, dark="#000", light="#fff", svgclass="qr", omitsize=True)

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;900&family=Fraunces:ital,opsz,wght@1,9..144,700&family=Special+Elite&display=swap">'

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Venmo Sign Insert</title>{FONTS}
<style>
@page{{size:4in 5in;margin:0}}
html,body{{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.sign{{box-sizing:border-box;width:4in;height:5in;border:.25in solid #4A2436;background:#fff;
  display:flex;flex-direction:column;align-items:center;color:#4A2436;font-family:"Archivo",Arial,sans-serif}}
.qr{{display:block;width:3.5in;height:3.5in;flex:none}}
.copy{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3pt;text-align:center;padding:0 .12in .04in}}
.typed{{font-family:"Special Elite",monospace;font-size:9pt;letter-spacing:.04em;margin:0}}
h1{{font-family:"Fraunces",Georgia,serif;font-style:italic;font-weight:700;font-size:17pt;line-height:1.05;margin:0}}
.small{{font-size:7.5pt;margin:0;color:#6E5A62}}
</style></head><body>
<div class="sign">
  {QR}
  <div class="copy">
    <p class="typed">SCAN FOR A FREE PATTERN</p>
    <h1>Ridgeline Bookmarks</h1>
    <p class="small">with newsletter sign-up &middot; theartiscomingfrominsidethehouse.com</p>
  </div>
</div>
</body></html>"""
open("venmo-sign.html", "w").write(html)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    pg = b.new_page(viewport={"width": 384, "height": 480}, device_scale_factor=300 / 96)
    pg.set_content(html, wait_until="networkidle")
    pg.pdf(path="venmo-sign.pdf", width="4in", height="5in", print_background=True)
    pg.screenshot(path="venmo-sign.png", clip={"x": 0, "y": 0, "width": 384, "height": 480})
    b.close()
print("ok")
