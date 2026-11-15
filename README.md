# Searchable reveal archive (prototype)

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
