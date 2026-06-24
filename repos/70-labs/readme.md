# 70 Labs

A hub of **10 wild, edge-native mini-apps** on a single Cloudflare Worker — built to learn
the newest web/AI tech *and* to actually get work done for Infinity Media & its brands.

**Live:** https://7.gear.lk · fallback https://seventy-labs.shehan.workers.dev

## The 10
| # | App | Path | Tech |
|---|-----|------|------|
| 1 | Caption Forge | `/apps/caption/` | Workers AI · Llama 3.3 70B |
| 2 | Link & QR Studio | `/apps/utm/` | client-only |
| 3 | Palette Lab | `/apps/palette/` | Canvas quantization |
| 4 | Image Squeeze | `/apps/squeeze/` | Canvas/WASM encode |
| 5 | Salah Compass | `/apps/salah/` | Geolocation + DeviceOrientation |
| 6 | Ride Lab | `/apps/ride/` | offline physics |
| 7 | Particle Storm | `/apps/webgpu/` | **WebGPU compute shaders** |
| 8 | Live Cursors | `/apps/cursors/` | **Durable Objects + WebSockets** |
| 9 | AI Vision | `/apps/vision/` | Llama Vision (Workers AI) |
| 10 | Voice Notes | `/apps/voice/` | Whisper + Llama + MeloTTS |
| 11 | Coach | `/apps/coach/` | AI fitness coach · Workers AI + offline-first localStorage (planned to spin out into its own app) |

## Architecture
- **One Worker.** `public/` is served as static assets (fast, cached). Only `/api/*` runs the Worker.
- **Workers AI** (`env.AI`) powers Caption Forge, AI Vision, Voice Notes (transcribe/summarise/TTS).
- **Durable Object** `CursorRoom` powers Live Cursors via hibernatable WebSockets.
- No build step, no framework — each app is a self-contained `index.html`. Shared theme in `public/shared/`.

## Develop
```bash
npm install        # only pulls wrangler
npm run dev        # local dev at http://localhost:8787
npm run deploy     # deploy to Cloudflare
npm run tail       # live logs
```

## Add an app
1. `public/apps/<slug>/index.html` (link `/shared/labs.css` + `/shared/labs.js`, call `mountTopbar("Name")`).
2. Add a card to the `APPS` array in `public/index.html`.
3. Server logic? Add a route in `src/index.js`.

See `BACKLOG.md` for 100+ more ideas, prioritised.

## Notes
- AI endpoints degrade gracefully and never store user data; images/audio are processed in-memory.
- Custom domain `7.gear.lk` is attached via `routes` in `wrangler.jsonc` (Workers Custom Domain).
