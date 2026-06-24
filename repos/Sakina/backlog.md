# Sakina — Backlog / pending work

Living list of what's pending so anyone (you or Claude) can pick up cold. Newest
context at top of each item. Mark `[x]` when shipped and move to "Done" with the
version it shipped in. Keep this in sync with the Version history table in
[`README.md`](./README.md).

## In progress

- [x] **i18n — Tamil + Sinhala + language toggle** (item 5). Framework in **v1.5.0**,
  all client-facing pages translated in **v1.6.0** (`src/i18n/`, code-split locales,
  top-bar toggle, localStorage persistence, English fallback). Covered: Landing, Auth,
  Dashboard, ProfileForm, Browse, ProfileView, Requests, Settings, Privacy, 404, and the
  shared marital/gender/contact-label constants. **Admin is intentionally English-only.**
  Still open:
  - [ ] **Native-speaker review** of all Tamil + Sinhala strings before launch
    (currently AI-drafted, flagged in the `src/i18n/ta.ts` / `si.ts` file headers).
  - [ ] Translate any **new** client copy added by future features (Stories, Guide) as
    they're built.

## Next up (small features)

- [ ] **Success Stories** (item 3): public `/stories` page + an admin tab to create/
  publish/hide stories. New `stories` DB table (Drizzle migration) mirroring existing
  admin CRUD patterns. *Bigger than it looks — touches the DB, so needs `db:generate` +
  `db:migrate:prod` on deploy. Do as a focused next session.*
- [x] **How-to-use / best-practices guide** (item 4): shipped in **v1.7.0** as public
  `/guide` (EN/Ta/Si), linked from landing top-bar + footer and Settings.
- [ ] **Moderator role + manage-moderators admin page** (user's plan, for later).
  Design: add a `'moderator'` role (DB, not env) with access limited to the **approval
  queue only** (approve / request-info / reject) — no ban, fields, stats, or all-profiles.
  Gate it in `worker/lib/middleware.ts` (a `moderatorMiddleware` / role check) and hide
  the other admin tabs in the UI for moderators. Add an **admin-only "Team" tab** to
  add/remove moderators by phone number (stores role on `users`, mirrors how ban looks up
  a user; promote on next login like ADMIN_PHONES, or set immediately if the user exists).
  Audit add/remove. RBAC plumbing across admin endpoints — a focused session.
- [ ] **Communicate a ban reason to the banned member.** Reason is now captured/stored/
  shown to admins (v1.8.0), but it's **not surfaced to the member**: sign-in is silent for
  banned numbers by design (anti-enumeration in `worker/routes/auth.ts` request-otp).
  Options to revisit with notifications: (a) SMS/email the reason on ban, or (b) a
  deliberate "your account was removed: <reason>" response at verify-otp (accepts
  revealing ban status to someone who proves they own the number). Pairs with item 11.

## Branding / design (do after features)

**Vision:** make every **client-facing** page feel coherent — like the user is
beginning their **wedding journey**, and this is the first step of it. Festive,
romantic, Indian-Muslim engagement-party vibe. Admin is out of scope. Keep
performance impact minimal throughout.

- [x] **Display font + serif headings** — self-hosted **Playfair Display 600** (23 KB,
  preloaded, swap) for headings; Poppins kept for logo/UI; body stays sans (v1.9.0).
- [x] **Decorative motifs** — Mughal **arch**, 8-point **star**, ornamental **divider**
  as inline SVG in `src/components/Ornaments.tsx` (v1.9.0).
- [x] **Color-palette testing** — semantic `--p-*` variables + 4 palettes + a floating
  **Theme** switcher (`src/components/PaletteSwitcher.tsx`), `data-palette` on `<html>` (v1.9.0).
- [x] **Wedding-invitation-card home page** — landing redesigned (v1.9.0).
- [ ] **Arch top — re-add once the user supplies the exact arch SVG.** Removed for now
  (the `ArchTop` ogee in `components/Ornaments.tsx` didn't match the reference). When the
  user provides the SVG path, wire it into `ArchTop` (gold stroke via currentColor + blush
  `--arch-fill`) and re-enable it as the card top in `Landing.tsx`.
- [ ] **Pick the final palette + set it as the default** in `:root` of `src/index.css`
  (currently defaults to teal). Then **remove or gate the PaletteSwitcher** (it's a preview
  tool rendered in `components/Root.tsx`).
- [ ] **Per-page ornament polish** — the palette + serif headings already apply to every
  page via shared tokens; optionally add light ornaments (a divider/star, arch headers) to
  Auth, Dashboard, Guide, ProfileForm etc. for extra "wedding journey" coherence. Also
  consider loading a 2nd Playfair weight if faux-bold on `font-bold` headings looks off.
- [ ] **Dark theme** — groundwork DONE (all colors flow through `--p-*` vars). To ship:
  add a `[data-theme='dark']` block in `index.css` overriding the neutral vars
  (`--p-sand-*`, `--p-ink`, `--p-muted`, and dark-tuned brand shades) + a toggle +
  `prefers-color-scheme` default.

## Later / larger projects

- [ ] **OCR / biodata auto-fill** (item 12): let a user upload a biodata file/image and
  auto-extract profile fields. Larger project — batch with the DB-encryption work below.
- [ ] **Database encryption-at-rest hardening + Postgres RLS (Row-Level Security)**:
  defence-in-depth so the DB enforces per-user access even if the app layer is bypassed.
  Pairs with the OCR work as the "later, larger" security batch.
- [x] **Real-phone signup test on the live domain** — DONE (2026-06-09). End-to-end OTP
  signup verified on `sakina.lk` with a real number: Turnstile → OTP SMS from **SakinaOTP**
  → account created (new prod encryption keys) → login. (Prod `TEXTLK_SENDER_ID` had been
  `TextLKDemo`, which was throttled; setting it to `SakinaOTP` fixed sending.)

## Deferred (decided)

- [ ] **Notifications** (item 11): *deferred* by decision. When revisited, the
  recommended cost-effective Phase 1 is **SMS via Text.lk for new-match events only**
  (rare, high-value, low volume), optionally adding **free PWA web-push** for installed
  users for lower-value updates (interest received, profile approved). Email is cheapest
  but we currently collect phone only, not email.
  - **Sender IDs ready:** OTP uses `SakinaOTP`; the approved **`Sakina`** / **`Sakina LK`**
    sender IDs are reserved for these non-OTP notification messages (pass a different
    `sender_id` to `sendSms` / add a `TEXTLK_SENDER_ID_ALERTS` env when building this).

## Repository & security

- **Remote:** `github.com/msfrox/Sakina` — **private**, branch `master`. (Worker name
  stays `nikah`; don't rename.)
- **Dependabot** vulnerability alerts + automated security fixes: **enabled**.
- **GitHub secret scanning / push protection:** NOT available free on private repos
  (needs paid GitHub Secret Protection). Free stand-in in place: a versioned
  **pre-commit secret guard** at `.githooks/pre-commit` (blocks `.env`/`.dev.vars`
  files + high-signal secret patterns). Auto-activates via the `prepare` npm script
  (`git config core.hooksPath .githooks`) on `npm install`.
  - [ ] *Optional upgrade:* swap the hand-rolled grep hook for **gitleaks** (more
    thorough) if you install it; or buy GitHub Secret Protection for server-side scanning.
- `.gitignore` excludes `dist`, `.env*`, `.dev.vars*`, `.wrangler` — no secrets tracked.
- [ ] *Low priority:* Dependabot flags `esbuild ≤0.24.2` (GHSA-67mh-4wv8-2f99) via
  **drizzle-kit** (dev dep). **Dev-server-only, does not affect production.** Do NOT
  `npm audit fix --force` (downgrades drizzle-kit, breaking). Clear it when drizzle-kit
  ships a build on a patched esbuild.

## CI/CD — deploy from GitHub (set up later; user wants a proper workflow)

Goal: deploy the Worker from GitHub instead of `npm run deploy` on a laptop.

- **Mechanism:** `.github/workflows/deploy.yml` using `cloudflare/wrangler-action@v3`:
  `npm ci` → `npm run build` → `wrangler deploy`.
- **Secrets split (important):**
  - **GitHub Actions secrets** (Settings → Secrets and variables → Actions) hold ONLY a
    `CLOUDFLARE_API_TOKEN` (+ `CLOUDFLARE_ACCOUNT_ID`) so CI may deploy. *Nothing else.*
  - **App runtime secrets** (`PHONE_ENC_KEY`, `SESSION_SECRET`, `TEXTLK_API_TOKEN`,
    `ADMIN_PHONES`, Turnstile, DB) stay in **Cloudflare** (`wrangler secret put`) — never
    in GitHub.
- **Cloudflare API token scope:** dash → My Profile → API Tokens → "Edit Cloudflare
  Workers" template, restricted to this account.
- **Trigger — decide:** (a) **manual** `workflow_dispatch` button *(recommended start —
  no surprise prod deploys)*, (b) `push` to `master` (auto), or (c) on tag/release.
- **DB migrations stay MANUAL:** run `npm run db:migrate:prod` locally before deploying.
  Don't automate schema migrations in CI (needs prod `DATABASE_URL` + risky).
- Optional: add a CI **check** workflow (build + lint + tsc) on PRs.
- TODO: create the workflow file once the user picks a trigger + adds the CF token.

## Secret backup / disaster recovery

- **Cloudflare secrets are write-only — you cannot read them back.** A self-generated
  prod key with no readable backup = unrecoverable if the Cloudflare secret is ever lost.
- [x] **Prod crypto keys rotated to known, backed-up values (2026-06-09).** The old
  unbacked `PHONE_ENC_KEY`/`PHONE_HASH_KEY` were rotated; new `PHONE_ENC_KEY`,
  `PHONE_HASH_KEY`, `SESSION_SECRET` were **user-generated locally** (CSPRNG), stored in
  the user's password manager, and set via `wrangler secret put`. Prod DB was **wiped
  clean** (`TRUNCATE` of all user tables) first, so no rows reference the old keys. Safe
  because prod had no real users yet.
- `TEXTLK_API_TOKEN` (re-copyable from Text.lk dashboard) and `TURNSTILE_SECRET`
  (Cloudflare dashboard) are recoverable from their providers — optionally mirror them in
  the password manager too.
- **RULE — never let the AI agent generate or see PRODUCTION secrets.** The agent writes
  code + instructions; the user generates prod key values locally (e.g.
  `[Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))`)
  and sets them via `wrangler secret put` so they never transit a chat/transcript.
- Losing the local `.env`/`.dev.vars` (DEV values) is low-impact: DB URL re-copy from
  Neon, Text.lk token from Text.lk, Turnstile test keys are public, dev crypto keys just
  regenerate. Prod is unaffected (it lives in Cloudflare, not these files).
- Repo itself is safe (pushed to private GitHub).

## Done

- [x] **v1.4.0 — Bug fixes & UX**: universal save in the field manager; styled 404 +
  `<ScrollRestoration>` + SPA `<Link>` nav; export-data blob download (was 404);
  visible "Edit my profile" button; landing top-bar Register/Support; `contact@sakina.lk`
  surfaced in footer, Settings, Privacy, 404, and on-hold screen.
