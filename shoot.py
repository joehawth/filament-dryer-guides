import sys; from playwright.sync_api import sync_playwright
pages=["index","about","disclosure","posts/best-filament-dryers","posts/creality-space-pi-vs-sunlu-s4","posts/sovol-sh03-vs-sunlu-s4"]
out=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    for name,vp in [("desktop",dict(width=1366,height=900)),("mobile",dict(width=390,height=844))]:
        ctx=b.new_context(viewport=vp,device_scale_factor=1, is_mobile=(name=="mobile"))
        pg=ctx.new_page()
        for s in pages:
            pg.goto(f"http://localhost:8765/{s}.html")
            ov=pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            f=f"{out}/{name}-{s.replace('posts/','')}.png"; pg.screenshot(path=f,full_page=True)
            print(name,s,"overflow_px",ov)
    b.close()
