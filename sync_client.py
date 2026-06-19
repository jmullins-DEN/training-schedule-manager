#!/usr/bin/env python3
"""Add (or update) a client in the Training Schedule Manager.

Keeps seed.json and the inlined `const SEED = {...};` block in index.html in
lockstep. Run during new-client onboarding right after the Drive dashboard
folder is created, then `git push` so Cloudflare redeploys.

Usage:
  python3 sync_client.py --name "Indigo-Construction" --folder-id <DRIVE_FOLDER_ID> [--on-sheet] [--track "Standard Track"] [--contact "Cindy Simpson"]

Matching is by folder slug (falls back to name); re-running updates in place.
"""
import argparse, json, re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SEED_JSON = HERE / "seed.json"
INDEX = HERE / "index.html"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Display name / repo slug (e.g. Indigo-Construction)")
    ap.add_argument("--folder", default=None, help="Drive folder slug (defaults to --name)")
    ap.add_argument("--folder-id", default="", help="Drive folder id (empty = no dashboard)")
    ap.add_argument("--on-sheet", action="store_true", help="Mark as on Cindy's original training sheet")
    ap.add_argument("--track", default="Standard Track")
    ap.add_argument("--contact", default="Cindy Simpson")
    ap.add_argument("--start-month", default="")
    args = ap.parse_args()

    folder = args.folder or args.name
    data = json.loads(SEED_JSON.read_text())
    key = folder.lower()
    client = next((c for c in data["clients"] if (c.get("folder") or c.get("name", "")).lower() == key), None)
    action = "updated" if client else "added"
    if client is None:
        client = {}
        data["clients"].append(client)
    client.update({
        "name": args.name,
        "folder": folder,
        "folderId": args.folder_id,
        "onSheet": args.on_sheet or client.get("onSheet", False),
        "hasDashboard": bool(args.folder_id),
        "track": args.track,
        "contact": args.contact,
        "startMonth": args.start_month or client.get("startMonth", ""),
        "overrides": client.get("overrides", {}),
    })
    data["clients"].sort(key=lambda c: c["name"].lower())
    SEED_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    # Regenerate the inlined SEED block so the deployed app matches seed.json.
    html = INDEX.read_text()
    block = "const SEED = " + json.dumps(data, indent=2, ensure_ascii=False) + ";"
    new_html, n = re.subn(r"const SEED = \{.*?\n\};", block, html, count=1, flags=re.S)
    if n != 1:
        sys.exit("ERROR: could not locate the `const SEED = {...};` block in index.html")
    INDEX.write_text(new_html)
    print(f"{action} {args.name} ({'dashboard' if args.folder_id else 'no dashboard'}) — {len(data['clients'])} clients total")

if __name__ == "__main__":
    main()
