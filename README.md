# The Animesy Magazine — website

Static website for **The Animesy Magazine**, the free magazine of
[The Animesy](https://theanimesy.com) — the symphony orchestra dedicated to anime music.

No build step: plain HTML, CSS and a few lines of JS. Fonts are self-hosted (no Google Fonts requests — relevant for DSGVO).

```
index.html          Home page
css/site.css        All layout and theme styles (classes, responsive rules)
css/fonts.css       @font-face rules for the self-hosted fonts
js/site.js          Newsletter form (opens a mail to support@theanimesy.com until a provider is wired in)
assets/logos/       Magazine, The Animesy, GoodRaht, Anime Connect World logos
assets/covers/      Issue covers
assets/photos/      Orchestra photos
```

## Run locally

Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

## Deploy

Hosted with GitHub Pages from the `main` branch (root).
To use a custom domain (e.g. `magazine.theanimesy.com`), add a `CNAME` file with
the domain and point a DNS `CNAME` record to `soler95.github.io`.

## Deploy to HubSpot (theanimesy.com/magazine)

Every push to `main` also deploys the site to HubSpot CMS
(`.github/workflows/deploy-hubspot.yml`). `scripts/build_hubspot_theme.py` turns the
static files into a HubSpot theme (`index.html` becomes the page template
`the-animesy-magazine/templates/magazine.html`); the issue PDFs go to the HubSpot
File Manager and are linked as `/hubfs/the-animesy-magazine/issues/…`.

One-time setup:

1. In HubSpot, create a personal access key (https://app.hubspot.com/l/personal-access-key)
   with the **Design Manager** and **Files** scopes.
2. In this repo: Settings → Secrets and variables → Actions →
   secret `HUBSPOT_PERSONAL_ACCESS_KEY` and variable `HUBSPOT_ACCOUNT_ID` (your Hub ID).
3. Run the workflow (Actions → Deploy to HubSpot → Run workflow).
4. In HubSpot: Content → Website pages → Create → choose the theme/template
   **The Animesy Magazine**, set the URL to `theanimesy.com/magazine`, publish.

After that, every change merged into `main` updates the live page automatically.
To build locally: `python3 scripts/build_hubspot_theme.py` (output in `build/`, git-ignored).

## Editing

- Colours: change `--accent` / `--accent2` in `css/site.css`.
- Content: edit the text directly in `index.html` (sections: `#top`, `#issue`,
  `#issues`, `#orchestra`, `#season`, `#about`, `#partners`, `#newsletter`, `footer`).
- Japanese text: if you add characters that are not on the site yet, copy the matching
  Noto Sans JP slices from `@fontsource/noto-sans-jp` into `assets/fonts/` and add their
  `@font-face` rules to `css/fonts.css` (see the comment there).
- New issue: drop the PDF in `assets/issues/`, add a cover to `assets/covers/` and a card in `#issues`.
- The "Issue 03" card contains `[MONTH YEAR]` / `[Next cover story]` placeholders.

© GoodRaht GmbH · The ANIMESY 2026.
