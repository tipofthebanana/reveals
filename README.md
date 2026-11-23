# Search Posts: searchable post archive

Self-contained static page. No backend, no CDN search library.

- `index.html` — search UI. Data is inlined in `<script id="archive-data">` so the page works if pasted into beehiiv, opened as a file, or served alone.
- `data.json` — same payload, for weekly edits when the two files are hosted together. The page fetches `data.json` when it can, and falls back to the inlined copy.
- `add-entry.py` — validates a new entry, prepends it to `data.json`, and syncs the inlined copy.

## Weekly process

1. After the Sunday teardown is published (and after any X note you want in the index), copy the public title, date, URL, and a one-line finding from the live post. Do not invent fields. Leave product, brand, tags, ingredients, or claims blank if they are not in the public text or on an official tag page.
2. Official tags only: `Cost-outs`, `Labels & Regulation`, `Produce & Grain`, `Process`, `Pantry`, `Dairy`.
3. From this folder:

```bash
python3 add-entry.py \
  --type teardown \
  --title "..." \
  --date 2026-11-15 \
  --url https://tipofthebanana.com/p/your-slug \
  --finding "One sentence from the public post." \
  --product "..." \
  --brand "..." \
  --tags "Process,Pantry"
```

4. Open `index.html` and search for the product to confirm it appears.
5. Publish: re-paste `index.html` into the beehiiv Custom HTML page, or git-push if hosted on a subdomain (Cloudflare Pages / GitHub Pages / Netlify).

Use `--type x-note` and an `https://x.com/TipOfTheBanana/status/...` URL for X notes.

## Local preview

```bash
python3 -m http.server 8765
# then open http://127.0.0.1:8765/?q=cassia
```

## Embedding on tipofthebanana.com

The beehiiv `/reveals` page iframes this archive with `?embed=1`. In an iframe, or with that query, the page hides its own site header and footer, lets the parent document scroll (no inner scrollbar), and posts `{type:'totb-height', height}` to the parent whenever the results change so the iframe can grow (search, filters, Load more). Standalone visits to this GitHub Pages URL still show the full chrome.

### Links when embedded

Teardown cards use `target="_top"` so a click opens the full post on tipofthebanana.com in the main window, not inside the iframe. X note cards use `target="_blank" rel="noopener"`. When embedded, a teardown click also posts `{type:'totb-nav', url}` to the parent so the beehiiv wrapper can move the top window if a browser ever blocks frame navigation. `add-entry.py` only writes data; the links are built in `index.html`.

## Ingredient Glossary

The Ingredient Glossary lives in `glossary/` and is served at `https://tipofthebanana.github.io/reveals/glossary/`. The beehiiv page at `/glossary` iframes it with `?embed=1`, same pattern as this archive.

