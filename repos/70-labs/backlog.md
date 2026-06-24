# 70 Labs — Backlog

The shipped 10 are in `/public/apps/`. Everything below is the idea bank, roughly
prioritised. Each line notes the **tech to learn** and **who it's for** (Work = Infinity
Media / brands, Me = personal interests, Learn = tech showcase).

Legend: ⭐ = strong next pick · 🧪 = mostly a tech-learning vehicle · 💼 = real utility

---

## ✅ Shipped (v1)
1. Caption Forge — AI brand captions (Workers AI · Llama 3.3) — Work
2. Link & QR Studio — UTM + branded QR (client) — Work
3. Palette Lab — image → colour tokens (Canvas) — Work
4. Image Squeeze — compress/convert WebP/AVIF (client) — Work
5. Salah Compass — prayer times + Qibla (Geo/sensors) — Me
6. Ride Lab — cycling calculators (offline) — Me
7. Particle Storm — GPU particle galaxy (WebGPU compute) — Learn
8. Live Cursors — realtime presence (Durable Objects) — Learn
9. AI Vision — image → description/alt (Llama Vision) — Learn
10. Voice Notes — record→transcribe→summarise→TTS (Whisper) — Learn

---

## ⭐ Next up (high value)
11. ⭐💼 **Brand Brain (RAG)** — upload brand guides/PDFs → chat grounded in them. *Workers AI + Vectorize + AutoRAG.*
12. ⭐💼 **Post Scheduler Lite** — calendar of brand posts synced to ClickUp via API. *Workers + D1 + Cron Triggers.*
13. ⭐💼 **Carousel Maker** — type bullet points → export 1080×1080 IG carousel PNGs. *Canvas/OffscreenCanvas.*
14. ⭐💼 **Stock-Lookup** — scan a barcode → pull Gearz/TecRoot stock from the xlsx/D1. *BarcodeDetector API + D1.*
15. ⭐🧪 **Edge Chat** — streaming multi-model chat (Llama 4 Scout, gpt-oss-120b, Kimi). *Workers AI streaming + SSE.*
16. ⭐💼 **Invoice Forge** — fill a branded invoice, export PDF. *pdf-lib in the browser.*
17. ⭐🧪 **Realtime Whiteboard** — multiplayer drawing room. *Durable Objects + Canvas + CRDT-lite.*
18. ⭐💼 **Hashtag Lab** — niche hashtag sets + reach tiers for SL cycling/tech. *Workers AI + curated lists.*
19. ⭐🧪 **AI Background Remover** — cut out product from photo, on-device. *Transformers.js / WebGPU (RMBG model).*
20. ⭐💼 **SL Delivery Cost** — courier price calculator (Pronto/Koombiyo/Domex) by district/weight. *client.*

## 💼 Work / agency utilities
21. UTM Library — saved campaigns in KV, team-shareable.
22. Caption A/B — generate two variants, vote, log winners (D1).
23. Brand Voice Tuner — store each brand's tone prompt; reuse across tools (KV).
24. Alt-text Batch — drop many product photos → CSV of alt-text (Llama Vision).
25. Reels Hook Writer — 10 scroll-stopping first lines for a topic.
26. Comment Responder — draft on-brand replies to customer comments.
27. Story Poll/Quiz maker — generate IG story interactive ideas.
28. SEO Title/Meta writer — for gear.lk product pages.
29. Product Description writer — bike/tech specs → marketing copy.
30. Email Subject Lab — subject lines + preview text + spam-score heuristic.
31. WhatsApp Broadcast composer — formatted promo messages + emoji.
32. Price Tag generator — printable shelf labels from stock sheet.
33. Receipt/Warranty card generator — branded PDF.
34. Logo-on-image watermarker — batch, client-side.
35. Aspect-ratio cropper — smart crop to IG/FB/TikTok/YouTube sizes.
36. GIF maker — frames/video → optimised GIF (WASM ffmpeg).
37. Video trimmer — quick clip cutter (WebCodecs).
38. Thumbnail tester — preview a thumbnail at feed sizes.
39. Content Calendar — month grid, export ICS, ClickUp sync.
40. Campaign brief generator — fill brief → structured doc.
41. Competitor watch — paste a competitor IG/site → positioning notes (AI).
42. Ad copy multiplier — one concept → 15 ad variations (RSA-style).
43. Lead capture form builder — embeddable, posts to D1.
44. QR menu/catalog — Gearz product catalog behind one QR.
45. Link-in-bio builder — branded bio page per brand on a subpath.
46. Review collector — QR → star rating → D1, gate 5★ to Google.
47. NPS micro-survey — one-tap, stored, charted.
48. Expense splitter — for shoots/events (client).
49. Shoot shotlist planner — AI shotlist from a creative brief.
50. Brand asset board — drop logos/fonts/colours, share a link.

## 🧪 Learn-the-tech showcases
51. WebGPU fluid sim — Navier-Stokes on the GPU.
52. WebGPU image filters — realtime camera filters (compute).
53. WebGPU raymarched scene — SDF shapes + lighting.
54. WebTransport demo — low-latency datagrams vs WebSocket.
55. WebRTC video room — peer video via a Workers signaling DO.
56. Collaborative cursor chat — cursors + ephemeral messages (DO).
57. Multiplayer Pong/Snake — DO game loop authority.
58. Spatial audio room — Web Audio panner + DO presence.
59. Local LLM in-browser — WebLLM (WebGPU) tiny model, no server.
60. Transformers.js playground — sentiment/NER/zero-shot on-device.
61. Speech-to-speech translator — Whisper → translate → MeloTTS.
62. Live captions — mic → streaming transcription overlay.
63. Image gen — text→image via Workers AI (Flux/SDXL).
64. Vector search demo — embeddings + Vectorize nearest-neighbours.
65. AutoRAG starter — point at a site, ask questions.
66. AI Agent (tools) — function-calling agent on Workers (Agents SDK).
67. Durable Workflows demo — multi-step retryable pipeline.
68. Queues demo — fan-out job processing visual.
69. R2 file drop — upload to R2, signed URLs, gallery.
70. D1 mini-CRM — contacts CRUD with Drizzle.
71. Hyperdrive demo — query a Postgres from the edge.
72. Cron dashboard — scheduled tasks status board.
73. Rate-limit visualiser — Workers rate limiting in action.
74. Geo-personalisation — content by `cf` country/colo.
75. Turnstile demo — bot-proof a form end-to-end.
76. WebAuthn passkey login — passwordless auth demo.
77. Web Bluetooth — connect a heart-rate/cadence sensor (ties to Ride Lab!).
78. Web Serial — talk to an Arduino/ESP32 from the browser.
79. WebUSB demo — device handshake.
80. WebCodecs — hardware video encode/decode.
81. WebGPU ML inference — run a small ONNX model.
82. Offline-first PWA — installable, background sync.
83. File System Access API — edit local files from web.
84. Web Share Target — accept shared content as an app.
85. View Transitions — silky cross-page animations across the labs.
86. CSS Houdini paint worklet — generative backgrounds.
87. WebXR peek — AR product viewer (place a bike in your room).
88. Canvas physics — Matter.js playground.
89. Shader toy — live GLSL editor with hot reload.
90. Audio sequencer — Web Audio step sequencer.

## 🌱 Personal / interest
91. Hadith/Dua of the day — curated, offline, shareable cards.
92. Quran audio player — reciter picker, last-position memory.
93. Tasbih counter — haptics + DO sync across devices.
94. Zakat calculator — gold/cash/business assets, LKR.
95. Halal additive checker — scan E-numbers.
96. Ramadan planner — fasting log + suhoor/iftar countdown.
97. Mosque finder — nearest masjid map (SL).
98. Bike maintenance log — service intervals, parts, reminders.
99. Strava-style ride map — GPX upload → elevation + stats.
100. Group ride planner — route + meetup time + share link (DO).
101. Tyre pressure calc — by weight/width/surface.
102. Sri Lanka weather-for-riding — wind/rain window finder.
103. LKR currency + import duty calc — for bike/tech imports.
104. Home server dashboard — unraid stats tile (ties to your homelab).
105. Personal link shortener — `7.gear.lk/x` slugs in KV.
106. Read-it-later — save articles, AI TL;DR.
107. Habit tracker — streaks, synced via DO.
108. Pomodoro + ambient soundscapes — Web Audio generative.

---

### Architecture notes for future apps
- One Worker, static assets in `/public`, `/api/*` runs the Worker (see `wrangler.jsonc`).
- Add an app: create `public/apps/<slug>/index.html`, add a card to `APPS[]` in `public/index.html`.
- Server features: add a route in `src/index.js`. AI = `env.AI`, realtime = a Durable Object, data = add D1/KV/R2 bindings.
- Keep client-only apps client-only (free, fast, offline). Reserve the Worker for AI/realtime/data.
