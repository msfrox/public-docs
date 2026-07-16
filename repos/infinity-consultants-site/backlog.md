# Infinity Consultants site — Backlog

_Internal-only. Started 2026-06-12._

## Done — v1.2 finalize (2026-07-16)

- [x] **Variant picked: Pulse.** Promoted to `/`; Editorial/Terminal/Cinema/Studio + the
      chooser removed. Proper `<title>`/OG tags restored.
- [x] **Info** section reworked in the Cinema style (struck "post & pray" statement + ∞ watermark).
- [x] **Process** section reworked as the Studio vertical timeline (dots light up on scroll).
- [x] **Work** + **Feed** sections added — data-driven (`public/data/clients.json`,
      `media.json`), auto-hide when empty. Decap/Sveltia CMS scaffolded (inactive) in `public/admin/`.
- [x] **Production domain infin8.agency** wired in `wrangler.jsonc` (worker `infinity-site`,
      account "infinity"); `og:url` updated; `ic.gear.lk` test domain dropped. `Other sources/` gitignored.

## Before go-live (owner actions)

- [ ] **Populate content:** add real clients to `public/data/clients.json` (+ images under
      `public/assets/clients/<id>/`) and real videos/images to `public/data/media.json`
      (+ files in `public/assets/media/`). Sections stay hidden until you do. See `public/data/README.md`.
- [ ] **Confirm the domain went live:** once `infin8.agency` is active on the "infinity"
      account and Workers Builds is connected to this repo, verify the push deployed
      (re-trigger the build if the first attempt ran before the zone existed).
- [ ] **Old test worker:** if `ic.gear.lk` should stop serving, disable that route on the
      OLD ("Shehan Feroze") account's `infinity-consultants` worker — not controlled from this repo.
- [ ] **Replace placeholder contact details** in `public/index.html` (search `TODO(owner)`):
      confirm WhatsApp number `94775569953`, email address, phone number.
- [ ] **Add the content editor** as a GitHub collaborator on the private repo.
- [ ] **(Optional) Activate the visual CMS:** wire a GitHub OAuth backend for `public/admin/`
      (Sveltia recommended for Cloudflare) so non-devs manage Clients/Feed via a form UI.

## Ideas / later

- [ ] Contact form with server-side email (Cloudflare Email Service / Worker) instead of
      WhatsApp-only. Add Turnstile to stop bots.
- [ ] Case-studies / portfolio section once client results can be published.
- [ ] Testimonials strip (needs real quotes + permission).
- [ ] Sinhala / Tamil language toggle if the client base needs it.
- [ ] Lightweight analytics (Cloudflare Web Analytics — free, no cookies).
- [ ] Custom OG images per section / campaign landing pages for ads.
