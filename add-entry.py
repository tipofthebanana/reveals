#!/usr/bin/env python3
"""Add a reveal to data.json and sync the inline copy in index.html.

Example (Sunday teardown):
  python3 add-entry.py \\
    --type teardown \\
    --title "Your cinnamon is almost certainly cassia" \\
    --date 2026-09-23 \\
    --url https://tipofthebanana.com/p/cinnamon-is-cassia \\
    --finding "US labels need not say which tree your cinnamon came from." \\
    --product "ground cinnamon" \\
    --tags "Labels & Regulation,Process,Pantry" \\
    --ingredients "cassia,Cinnamomum verum" \\
    --claims "cinnamon"

Example (X note):
  python3 add-entry.py \\
    --type x-note \\
    --title "In-N-Out makes its own hamburger patties, in its own plants" \\
    --date 2026-11-08 \\
    --url https://x.com/TipOfTheBanana/status/2119482079373332601 \\
    --finding "In-N-Out makes its own hamburger patties, in its own plants." \\
    --product "hamburger patties" --brand "In-N-Out" --tags Process

Leave unknown fields off. Do not invent findings, products, or tags.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data.json"
INDEX = ROOT / "index.html"
ALLOWED_TAGS = {
    "Cost-outs",
    "Labels & Regulation",
    "Produce & Grain",
    "Process",
    "Pantry",
    "Dairy",
}
ALLOWED_TYPES = {"teardown", "x-note"}


def csv(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def slug_id(kind: str, url: str, title: str) -> str:
    if kind == "x-note":
        m = re.search(r"/status/(\d+)", url)
        if m:
            return f"x-{m.group(1)}"
    if "tipofthebanana.com/p/" in url:
        slug = url.rstrip("/").split("/p/")[-1]
        return f"td-{slug}"
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{kind[:2]}-{base[:60]}"


def load() -> dict:
    payload = json.loads(DATA.read_text())
    if "entries" not in payload:
        raise SystemExit("data.json is missing an entries array")
    return payload


def validate(entry: dict, existing: list[dict]) -> None:
    if entry["type"] not in ALLOWED_TYPES:
        raise SystemExit(f"type must be one of {sorted(ALLOWED_TYPES)}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", entry["date"]):
        raise SystemExit("date must be YYYY-MM-DD (America/New_York calendar date)")
    if not entry["title"] or not entry["finding"] or not entry["url"]:
        raise SystemExit("title, finding, and url are required")
    if not entry["url"].startswith("http"):
        raise SystemExit("url must be an https link to the teardown or X post")
    bad = [t for t in entry["tags"] if t not in ALLOWED_TAGS]
    if bad:
        raise SystemExit(f"unknown tags {bad}. Allowed: {sorted(ALLOWED_TAGS)}")
    ids = {e["id"] for e in existing}
    urls = {e["url"] for e in existing}
    if entry["id"] in ids or entry["url"] in urls:
        raise SystemExit("that id or url is already in data.json")


def sync_index(payload: dict) -> None:
    html = INDEX.read_text()
    start = html.find('<script id="archive-data" type="application/json">')
    end = html.find("</script>", start)
    if start == -1 or end == -1:
        raise SystemExit("could not find <script id=\"archive-data\"> in index.html")
    open_tag = '<script id="archive-data" type="application/json">'
    injected = open_tag + json.dumps(payload, indent=2, ensure_ascii=False) + "\n  "
    html = html[:start] + injected + html[end:]
    INDEX.write_text(html)


def main() -> int:
    p = argparse.ArgumentParser(description="Append a reveal and sync index.html")
    p.add_argument("--type", required=True, choices=sorted(ALLOWED_TYPES))
    p.add_argument("--title", required=True)
    p.add_argument("--date", required=True, help="YYYY-MM-DD in America/New_York")
    p.add_argument("--url", required=True)
    p.add_argument("--finding", required=True, help="One-line finding from the public post")
    p.add_argument("--product", default="")
    p.add_argument("--brand", default="")
    p.add_argument("--tags", default="", help="Comma-separated official site tags only")
    p.add_argument("--ingredients", default="")
    p.add_argument("--claims", default="")
    p.add_argument("--id", default="")
    args = p.parse_args()

    payload = load()
    entry = {
        "id": args.id or slug_id(args.type, args.url, args.title),
        "type": args.type,
        "title": args.title.strip(),
        "date": args.date.strip(),
        "product": args.product.strip(),
        "brand": args.brand.strip(),
        "finding": args.finding.strip(),
        "tags": csv(args.tags),
        "ingredients": csv(args.ingredients),
        "claims": csv(args.claims),
        "url": args.url.strip(),
    }
    validate(entry, payload["entries"])
    payload["entries"].insert(0, entry)
    DATA.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    sync_index(payload)
    print(f"added {entry['id']} ({len(payload['entries'])} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
