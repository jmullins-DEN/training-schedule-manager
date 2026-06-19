# Training Schedule Manager

Single-file HTML app for managing DEN client training schedules. Cindy edits client
schedules and curriculum here instead of the spreadsheet. Client list is seeded from
the customer folders in the "Weekly Dashboards" Drive folder.

- `index.html` — self-contained app (seed data inlined)
- `seed.json` — source seed (45 clients, 23-month Standard Track curriculum)

Deploys to Cloudflare Pages (Connect to Git → select this repo).

## Next steps on PC

1. **Clone & view locally**
   ```
   git clone https://github.com/jmullins-DEN/training-schedule-manager.git
   cd training-schedule-manager
   ```
   Open `index.html` in any browser to see it render (faster/cleaner than the GitHub htmlpreview link).

2. **Connect Cloudflare Pages (one-time, only you can do this)**
   - Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
   - Select `training-schedule-manager`
   - Build command: *none* · Output directory: `/`
   - Deploy → you get a `*.pages.dev` URL — that's the shared version for Cindy.
   - After this, every push auto-redeploys.

3. **Edit → push → auto-deploy**
   ```
   git add -A && git commit -m "..." && git push
   ```

## Adding clients

- **No-dashboard / training-only clients:** add directly in the app ("+ Add client").
- **New dashboard clients (onboarding):** after the Drive dashboard folder is created, run
  ```
  python3 sync_client.py --name "<Folder-Name>" --folder-id "<id>"
  ```
  then commit & push. This keeps `seed.json` and the inlined `SEED` in `index.html` in lockstep.

## Notes

- The app saves Cindy's edits to her browser (localStorage). New seeded clients merge in on load without wiping her edits.
- Source of truth for the client list = customer folders in the "Weekly Dashboards" Drive folder.
