# melyro.app

The website of [Melyro](https://melyro.app), a media player for iPhone, iPad and Apple TV that plays sources the user supplies. It holds the product page, the privacy policy, the terms of use and the support page that the App Store listing and the app link to.

**Live at <https://melyro.app>.** The GitHub Pages address, <https://cenkgundev.github.io/melyro-site/>, also works.

## Pages

| Page | Turkish | English | German |
|---|---|---|---|
| Product page | [`index.html`](index.html) | [`index-en.html`](index-en.html) | [`index-de.html`](index-de.html) |
| Privacy policy | [`privacy.html`](privacy.html) | [`privacy-en.html`](privacy-en.html) | [`privacy-de.html`](privacy-de.html) |
| Terms of use | [`terms.html`](terms.html) | [`terms-en.html`](terms-en.html) | [`terms-de.html`](terms-de.html) |
| Support | [`support.html`](support.html) (all three languages on one page) | | |

The product pages set a canonical URL on `melyro.app`, and the translated pages link each other with `hreflang`.

## Files

```
index*.html, home.css, home.js   product page
privacy*.html, terms*.html,
support.html, style.css          legal and support pages
img/                             App Store screenshots per language (.webp), mark, icons, og.png
cloudflare/                      Worker that serves the site on melyro.app
.nojekyll                        serve files as they are, without Jekyll
```

The pages are plain HTML and CSS with no build step.

## Updating

Edit the HTML and push to `main`. GitHub Pages publishes the branch root within a minute or two, and the Worker on `melyro.app` caches each response for five minutes.

When you change a page, change its other languages in the same commit. The app and the App Store listing link to the privacy and support URLs, so keep those paths stable.

## Hosting

GitHub Pages serves the repository from `main` at `/`. A Cloudflare Worker (`cloudflare/worker.js`, named `melyro-web`) fetches each path from GitHub Pages and returns it under `melyro.app`; `www.melyro.app` and `http://` redirect to `https://melyro.app`. Page changes need no Worker deploy. After changing the Worker itself:

```sh
cd cloudflare
npx wrangler@4 deploy
```

See [`cloudflare/README.md`](cloudflare/README.md) for details. Contact address: support@melyro.app.
