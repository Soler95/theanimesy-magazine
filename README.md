# The Animesy Magazine — website

Static website for **The Animesy Magazine**, the free magazine of
[The Animesy](https://theanimesy.com) — the symphony orchestra dedicated to anime music.

No build step: plain HTML, CSS and a few lines of JS.

```
index.html          Home page
css/site.css        Theme variables, hover states, responsive overrides
js/site.js          Newsletter form (mailto fallback until a provider is wired in)
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

## Editing

- Colours: change `--accent` / `--accent2` in `css/site.css`.
- Content: edit the text directly in `index.html` (sections: `#top`, `#issue`,
  `#issues`, `#orchestra`, `#season`, `#partners`, `#newsletter`, `footer`).
- The "Issue 03" card contains `[MONTH YEAR]` / `[Next cover story]` placeholders.

© GoodRaht GmbH · The ANIMESY 2026.
