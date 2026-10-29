# Dry Spool Guides (DRAFT, unpublished)
Build: `python3 build.py` -> `dist/`. Preview: `python3 -m http.server -d dist 8080`.
Deploy later: Netlify (netlify.toml included) or GitHub Pages (publish `dist/`).
Before publishing: set SITE url in build.py, replace `{{AFFILIATE:...}}` placeholders in src/ with real links, re-check all prices.
