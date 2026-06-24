# Coach — AI fitness, everywhere

An offline-first AI fitness coach that runs as a **web app (PWA)** and **native iOS/Android wrappers**,
on a single Cloudflare Worker. Spun out of [70 Labs](https://7.gear.lk).

**Live:** https://coach.gear.lk

## What it does
- **Plan** — enter your stats → live BMR/TDEE, calorie & protein targets, timeline to goal.
- **Train** — A/B full-body program with **auto weight suggestions** + an 8-week Foundation→Build→Deload cycle, and a focused **Workout Now** mode (set-by-set logging, rest timer, hydration, live heart rate).
- **Food** — quick-add (SL/halal database), **AI meal-photo** calorie/protein scan.
- **Progress** — Week / Month (calendar) / All views, weight chart, **body composition** (US Navy tape + AI photo scan).
- **Coach** — chat (free Cloudflare Workers AI by default; optional Claude), with persistent memory; also a floating chat bubble.
- **Health** — two-way **Apple Health** sync (steps, weight, body-fat, sleep, resting HR + push workouts/weight/food back). Live HR from an Amazfit over Bluetooth.
- **Looks** — light/dark, 3 designs, 4 colour themes. **Reminders** (native on device, web in browser). **Cross-device sync** (sync code, or zero-touch via Cloudflare Access).

## Architecture
- **One Worker.** `public/` is served as static assets; `/api/*` runs the Worker (Workers AI, sync via KV, push/VAPID + hourly cron, Strava, Apple Health helpers).
- **Local-first** state in `localStorage`, mirrored to **Cloudflare KV** when sync/Access is on (shares the same namespace as the original 70 Labs build, so existing data carries over).
- No build step — the app is one `public/index.html` + `public/shared/`.

## Develop
```bash
npm install      # pulls wrangler
npm run dev      # http://localhost:8787
npm run deploy   # → coach.gear.lk
```

## Native apps (`mobile/`)
Wrappers load `https://coach.gear.lk` and add native Bluetooth / HealthKit / notifications.
- **iOS:** `mobile/capacitor` (recommended) — see `mobile/BUILD.md`. CI builds an **unsigned IPA** and publishes a **GitHub Release** (you resign with your cert/profile).
- **Android:** `mobile/capacitor` too — the `Android APK` workflow builds a **debug-signed APK** you can sideload directly (no secrets).
- **Expo/RN** alternative in `mobile/expo`.

## Multi-platform
| Platform | How |
|---|---|
| **Windows / Mac / Linux** | Open https://coach.gear.lk in a browser → install as a PWA (address-bar install / "Add to Home screen"). |
| **iOS** | Install the wrapper IPA (App Store-free, sideloaded). |
| **Android** | Install the APK from Releases. |

## Optional setup (your keys — never handled by the build)
- **Claude AI:** `wrangler secret put ANTHROPIC_API_KEY` (needs paid API credits; off by default).
- **Strava import:** `wrangler secret put STRAVA_CLIENT_ID` + `STRAVA_CLIENT_SECRET` (callback domain `coach.gear.lk`).
- **Web push (browser background reminders):** `npx web-push generate-vapid-keys` → `wrangler secret put VAPID_PUBLIC` + `VAPID_PRIVATE`.
- **Zero-touch sync:** create a Cloudflare Access app over `coach.gear.lk` allowing your email — the app then keys data to your verified identity automatically.

> Not medical advice — see a professional for pain, injury, or medical conditions.
