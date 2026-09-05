# Hisho FPL Hub v5 — Production-ready build

Professional Fantasy Premier League intelligence application with official FPL data, Understat shot enrichment, weekly current-player/transfer enrichment, mini-league intelligence, transfer planning, account login and privacy-aware usage analytics.

## v5 highlights

- **Current player image resolver**: weekly current-player dataset is matched to FPL players and used for refreshed player portraits, with official Premier League/FPL image fallback.
- **Transfers tab**: date, player, from club, to club, fee, market value, season and movement type, refreshed from the public weekly `dcaribou/transfermarkt-datasets` dataset.
- **Accounts**: email/password registration and login with scrypt password hashing and HttpOnly 30-day sessions.
- **Product analytics**: background interaction events for product improvement. Passwords, tokens, emails in event metadata and secrets are excluded from analytics payloads. The sign-in screen tells users that usage events are collected.
- **Admin activity export**: `/api/admin/activity?token=ADMIN_TOKEN`.
- All existing v4.2 features remain: Player Lab, distance filters, N/A-last sorting, fixture difficulty, 3–5 GW simulator, transfer planner, league leverage, comparisons, news and history.

## Data sources

1. Official Fantasy Premier League public endpoints — players, current prices, teams, fixtures, ownership, manager teams/leagues and live GW points.
2. Understat — shot-level enrichment where matching is available.
3. `dcaribou/transfermarkt-datasets` — CC0 weekly refreshed player/transfer dataset, used for transfer history and additional current player images.
4. Google News RSS — player/team headline discovery.

Third-party fields can be temporarily unavailable. FPL remains the primary source for FPL price/team identity.

## Run locally

```bash
npm install
npm start
```

Open `http://localhost:4173`.

## Deploy

This repository includes `render.yaml`, `Dockerfile` and `.nvmrc`. Push the repository to GitHub, then create a Render Web Service from it. Render assigns an HTTPS `*.onrender.com` domain automatically.

> Important: the included account store uses server files. On a free Render service, local files are ephemeral. For a public production launch with permanent accounts, use a persistent disk or migrate the account/activity store to Postgres/Supabase. The application itself works without accounts if the storage is reset.

## Git Bash push

```bash
git init && git add . && git commit -m "Launch Hisho FPL Hub v5" && git branch -M main && git remote add origin https://github.com/YOUR_USERNAME/hisho-fpl-hub.git && git push -u origin main
```

## Privacy

Analytics are intended for product improvement only. Do not store passwords, authentication secrets, private FPL credentials, or sensitive form content in activity metadata. Users are informed at sign-in that product usage events are collected.


## v5.1 — iPhone / iPad mobile web app

This build is installable as an iOS Progressive Web App (PWA).

### Install on iPhone / iPad
1. Open the hosted Hisho FPL Hub URL in **Safari**.
2. Tap the **Share** button.
3. Tap **Add to Home Screen**.
4. Launch **Hisho FPL Hub** from the new Home Screen icon.

The app then opens in standalone mode without the normal Safari toolbar.

### iOS changes
- PWA manifest + service worker.
- Apple Home Screen icon.
- iPhone safe-area support for Dynamic Island/notch and Home indicator.
- Bottom mobile navigation contains all app sections and scrolls horizontally.
- Larger touch targets and form fields to prevent Safari input zoom.
- Standalone/full-screen style.
- Static app shell caching; live FPL/API data remains network-fresh.
- Improved iPhone tables, dialogs, filters, cards and fixture views.
