#!/usr/bin/env python3
"""Tiny static site builder: src/*.html bodies + front-matter -> dist/. No deps."""
import pathlib, re, shutil, html
ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT/"src", ROOT/"dist"
SITE = {"name": "Dry Spool Guides", "url": "https://joehawth.github.io/filament-dryer-guides"}
DISC = ('<p class="disclosure"><strong>Affiliate disclosure:</strong> some links on this page are affiliate links. '
        'If you buy through them we may earn a small commission at no extra cost to you. '
        '<a href="{r}disclosure.html">Full disclosure</a>.</p>')
TPL = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | {site}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}"><meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{r}style.css"></head><body>
<header><a class="brand" href="{r}index.html">{site}</a>
<nav><a href="{r}index.html">Guides</a> <a href="{r}about.html">About</a> <a href="{r}disclosure.html">Disclosure</a></nav></header>
<main>{disc}{body}</main>
<footer><p>Research-based guides: we have not hands-on tested these products. Prices change; check the retailer.</p>
<p><a href="{r}disclosure.html">Affiliate disclosure</a> · <a href="{r}about.html">About</a></p></footer>
</body></html>"""
def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT/"static/style.css", OUT/"style.css")
    for f in SRC.rglob("*.html"):
        raw = f.read_text()
        m = re.match(r"---\n(.*?)\n---\n", raw, re.S)
        meta = dict(l.split(": ",1) for l in m.group(1).splitlines())
        body = raw[m.end():]
        rel = f.relative_to(SRC)
        r = "../" * (len(rel.parts)-1)
        # placeholder affiliate links -> visible draft marker, rel=sponsored
        body = re.sub(r'href="\{\{AFFILIATE:([a-z0-9-]+)\}\}"',
                      r'href="#AFFILIATE-\1" rel="sponsored nofollow" data-affiliate="\1"', body)
        body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
        page = TPL.format(title=html.escape(meta["title"]), desc=html.escape(meta["description"]),
            site=SITE["name"], url=f'{SITE["url"]}/{rel.as_posix()}', r=r,
            ogtype="article" if rel.parts[0]=="posts" else "website",
            disc=DISC.format(r=r) if meta.get("affiliate")=="yes" else "", body=body)
        dst = OUT/rel; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_text(page)
        print("built", dst)
if __name__ == "__main__": build()
