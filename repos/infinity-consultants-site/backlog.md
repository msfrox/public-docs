# Infinity Consultants site — Backlog

_Internal-only. Started 2026-06-12._

## In progress — design variant test (2026-06-12)

Five monochrome design variants are deployed for the owner to compare:
`/v1` Pulse (interactive dark) · `/v2` Editorial (paper white) · `/v3` Terminal
(brutalist mono) · `/v4` Cinema (full-screen scenes) · `/v5` Studio (split panel).
Root `/` is a chooser page (noindex).

- [ ] **Owner picks the winning variant** (mixing elements allowed) → promote it to `/`,
      delete the others + the chooser, restore proper `<title>`/OG tags.
- [ ] WhatsApp number `94775569953` (found in other Infinity projects) is now used on all
      variants — **owner to confirm** it's the right number for IC.

## Before go-live (owner actions)

- [ ] **Replace placeholder contact details** in `public/index.html` (search `TODO(owner)`):
      WhatsApp number, email address, phone number. Currently `+94 77 000 0000` /
      `hello@infinityconsultants.lk` are placeholders.
- [ ] **Decide production domain** (infinityconsultants.lk?) and update `wrangler.jsonc`
      routes + `og:url` in `index.html` (see DEPLOY.md go-live checklist).
- [ ] **Connect Workers Builds** to the GitHub repo so pushes auto-deploy
      (dashboard step — see DEPLOY.md). Until then, deploys are manual `npx wrangler deploy`.
- [ ] **Add the content editor** as a GitHub collaborator on the private repo.

## Ideas / later

- [ ] Contact form with server-side email (Cloudflare Email Service / Worker) instead of
      WhatsApp-only. Add Turnstile to stop bots.
- [ ] Case-studies / portfolio section once client results can be published.
- [ ] Testimonials strip (needs real quotes + permission).
- [ ] Sinhala / Tamil language toggle if the client base needs it.
- [ ] Lightweight analytics (Cloudflare Web Analytics — free, no cookies).
- [ ] Custom OG images per section / campaign landing pages for ads.
