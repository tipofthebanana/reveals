# Ingredient Glossary

Self-contained static page, same pattern as the Search Posts archive at the repo root.

- `index.html` — search UI and detail pages. Data is inlined in `<script id="glossary-data">` so the page works if opened as a file or served alone.
- `glossary.json` — same payload; the page fetches this when it can, and falls back to the inlined copy.

Live embed: the beehiiv page at https://tipofthebanana.com/glossary iframes this folder with `?embed=1`. In an iframe, or with that query, the page hides its own site header and footer, lets the parent document scroll (no inner scrollbar), and posts `{type:'totb-height', height}` to the parent whenever the view changes. Standalone visits still show the full chrome.

Internal glossary links use hash routes (`#/slug`) so they stay inside the iframe. Links to tipofthebanana.com use `target="_top"` when embedded and also post `{type:'totb-nav', url}`.
