# M.U.K. Accounting — website

Static one-page site for M.U.K. Accounting (Mariam Krevskaia, CPA, Kent, WA). Live at https://mukaccounting.net.

## How it is published
- Hosting: **GitHub Pages** from this repo (`ivanwts/muk-accounting`, branch `main`, root). Every push to `main` redeploys in about a minute; there is no build step.
- Domain `mukaccounting.net` is registered at GoDaddy (Ivan's account); DNS there points to GitHub Pages (four A records + `www` CNAME). `CNAME` file in the repo keeps the custom domain.
- HTTPS is enforced by GitHub Pages.

## Files
- `index.html` — the page. `privacy.html`, `terms.html`, `404.html` — the extra pages.
- `config.js` — **everything firm-specific in one place**: phones, e-mail, address, hours, the booking link (`bookingUrl`) and the lead endpoint (`leadUrl`). Change facts here, not in the HTML.
- `script.js` — all texts in English and Russian (`T.en` / `T.ru`, keys match `data-i18n` attributes), language switch, the request form, structured data for search engines.
- `styles.css` — styles. `legal.js` — tiny script for the legal pages.
- `images/logo-source.png` — the master logo (as supplied). Everything else in `images/` and `favicon.ico` is generated from it by `python3 tools/make_brand_assets.py` (needs Pillow). Do not hand-edit the generated files.
- `robots.txt`, `sitemap.xml` — for search engines.

## Cache-busting
Browsers cache `styles.css`, `script.js`, `config.js` hard. After changing one of them, bump its `?v=` query in **every** HTML file that references it (index, privacy, terms, 404), otherwise phones keep the old version.

## Where requests go
- The form posts JSON to the WorkTime cabinet (`CONFIG.leadUrl`): a card appears in Воронка → Новые клиенты and Mariam gets an e-mail. If that endpoint is unreachable, the form falls back to opening an e-mail to `CONFIG.email`. A honeypot-filled POST is a safe test (the server answers ok and writes nothing); a real submission creates a real card.
- "Pick a day and time" opens the firm's own booking page in the WorkTime cabinet (`CONFIG.bookingUrl`); availability is managed there by Mariam.

## Rules
- No photo of Mariam anywhere (site, share image, icons) — her decision. The logo only.
- Brand is written **M.U.K. Accounting** (with the final dot).
- Don't claim credentials beyond CPA; never promise a client portal or document upload; the form must not ask for SSN/EIN/bank details.
- Keep the modern, light look (Manrope + Playfair italic accent, cream background, dark green + terracotta). The first vintage design was rejected.
- The privacy policy says there is no analytics — if analytics is ever added, update the policy.
