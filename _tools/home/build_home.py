"""Writes the three home pages (index.html, index-en.html, index-de.html) into the site checkout.

    python3 build_home.py <site-dir>

Strings are in home_copy.py, the look in home.css, the motion in home.js. Images are copied from img/;
icons are Phosphor (regular) SVGs inlined from the npm package, the mark is render.py's geometry."""
import html, pathlib, re, shutil, sys
from home_copy import COPY, APP_STORE

HERE = pathlib.Path(__file__).parent
PHOSPHOR = HERE / "ph/package/assets/regular"
M_PATH = ("M240 350H340V716H240ZM462 482H562V716H462ZM684 482H784V716H684Z"
          "M240 482A161 161 0 0 1 562 482H462A61 61 0 0 0 340 482Z"
          "M462 482A161 161 0 0 1 784 482H684A61 61 0 0 0 562 482Z")
ORDER = ("tr", "en", "de")
e = html.escape


def icon(name, cls="ic"):
    svg = (PHOSPHOR / f"{name}.svg").read_text()
    return svg.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" focusable="false" ', 1)


def mark(size_class):
    # The app icon in its default colourway (Kor), from scripts/icon/render.py.
    return (f'<svg class="{size_class}" viewBox="0 0 1024 1024" aria-hidden="true">'
            f'<rect width="1024" height="1024" fill="#FF6B3D"/><path d="{M_PATH}" fill="#14100D"/>'
            f'<circle cx="762" cy="300" r="46" fill="#FFF6EC"/></svg>')


# The headline's longest line in ems of the expanded system font, measured in WebKit by
# measure.swift (span width at font-size 100px). The hero sizes the type so that line fits its column:
# 645px at 1440, about 44vw from 1024 up. Re-measure after changing h1a/h1b.
H1_EMS = {"tr": 8.95, "en": 10.51, "de": 12.01}


def h1max(c):
    return round(min(4.6, 645 * .96 / H1_EMS[c["lang"]] / 16), 2)


def h1v(c):
    return round(44 * .96 / H1_EMS[c["lang"]], 2)


def wordmark():
    return '<span class="wm">melyro<span class="lamp" aria-hidden="true"></span></span>'


def phone(src, alt, cls="", eager=False, w=640, h=1390):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="phone {cls}"><div class="dev"><img src="{src}" alt="{e(alt)}" width="{w}" height="{h}" {load}>'
            f'<span class="island" aria-hidden="true"></span></div></div>')


def cta(c, extra=""):
    return f'<a class="btn btn-primary {extra}" href="{APP_STORE}">{icon("apple-logo", "ic ic-btn")}<span>{e(c["cta"])}</span></a>'


def lang_links(c):
    out = []
    for code in ORDER:
        other = COPY[code]
        if code == c["lang"]:
            out.append(f'<strong aria-current="page">{code.upper()}</strong>')
        else:
            out.append(f'<a href="{other["file"]}" hreflang="{code}" lang="{code}">{code.upper()}</a>')
    return "".join(out)


def page(c):
    L = c["lang"]
    img = lambda n: f"img/{n}-{L}.webp"
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{k}" href="https://melyro.app/{"" if k == "tr" else COPY[k]["file"]}">'
        for k in ORDER)
    sources = "\n".join(
        f'''<li class="src" data-reveal>
      <span class="src-ic">{icon(ic)}</span>
      <h3>{e(name)}</h3>
      <p>{e(text)}</p>
    </li>''' for ic, name, text in c["sources"])
    pro = "\n".join(
        f'''<li data-reveal>{icon(ic)}<div><h3>{e(name)}</h3><p>{e(text)}</p></div></li>'''
        for ic, name, text in c["pro"])
    canonical = "https://melyro.app/" + ("" if L == "tr" else c["file"])
    return f'''<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="index">
<meta name="description" content="{e(c["description"])}">
<meta name="theme-color" content="#0D0C0B">
<meta name="color-scheme" content="dark">
<meta name="apple-itunes-app" content="app-id=6812315758">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["description"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://melyro.app/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<title>{e(c["title"])}</title>
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" href="img/mark.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" as="image" href="{img("player")}" fetchpriority="high">
<link rel="stylesheet" href="home.css">
<script src="home.js" defer></script>
</head>
<body class="home">
<a class="skip" href="#main">{e(c["nav_features"])}</a>
<header class="bar">
  <div class="bar-in">
    <a class="brand" href="{c["file"]}" aria-label="Melyro">{wordmark()}</a>
    <nav aria-label="Melyro">
      <a href="#ozellikler">{e(c["nav_features"])}</a>
      <a href="#pro">{e(c["nav_pro"])}</a>
      <a href="{c["privacy"]}">{e(c["nav_privacy"])}</a>
      <a href="{c["support"]}">{e(c["nav_support"])}</a>
    </nav>
    <div class="langs" role="group" aria-label="{e(c["langs"])}">{lang_links(c)}</div>
    <a class="btn btn-primary btn-small" href="{APP_STORE}">{e(c["cta_small"])}</a>
  </div>
</header>

<main id="main">
<section class="hero">
  <div class="hero-copy">
    <h1 style="--h1max:{h1max(c)}rem;--h1v:{h1v(c)}vw"><span class="l1">{e(c["h1a"])}</span><span class="l2">{e(c["h1b"])}</span></h1>
    <div class="now" aria-hidden="true"><span></span></div>
    <p class="hero-sub">{e(c["hero_sub"])}</p>
    <div class="ctas">
      {cta(c)}
      <a class="btn btn-ghost" href="#kaynaklar">{e(c["how"])}{icon("arrow-right", "ic ic-btn")}</a>
    </div>
  </div>
  <div class="hero-art">
    <div class="tablet"><div class="dev"><img src="{img("ipad-home")}" alt="{e(c["alt_ipad"])}" width="1400" height="1867"></div></div>
    {phone(img("player"), c["alt_phone"], "hero-phone", eager=True)}
  </div>
</section>

<section class="sources" id="kaynaklar">
  <h2 data-reveal>{e(c["src_h"])}</h2>
  <ol class="src-list">
    {sources}
  </ol>
  <div class="note" data-reveal>
    {icon("shield-check")}
    <p><strong>{e(c["note_b"])}</strong> {e(c["note"])}</p>
  </div>
</section>

<section class="features" id="ozellikler">
  <h2 class="two" data-reveal><span>{e(c["feat_h"][0])}</span><span>{e(c["feat_h"][1])}</span></h2>
  <div class="bento">
    <article class="cell c-live" data-reveal>
      <div class="cell-txt"><h3>{e(c["f_live"][0])}</h3><p>{e(c["f_live"][1])}</p></div>
      {phone(img("live"), c["alt_live"], "rise")}
    </article>
    <article class="cell c-player" data-reveal>
      <div class="cell-txt"><h3>{e(c["f_player"][0])}</h3><p>{e(c["f_player"][1])}</p></div>
      {phone(img("player"), c["alt_phone"], "rise peek")}
    </article>
    <article class="cell c-series" data-reveal>
      <div class="cell-txt"><h3>{e(c["f_series"][0])}</h3><p>{e(c["f_series"][1])}</p></div>
      {phone(img("series"), c["alt_series"], "rise peek")}
    </article>
    <article class="cell c-ipad" data-reveal>
      <div class="cell-txt"><h3>{e(c["f_ipad"][0])}</h3><p>{e(c["f_ipad"][1])}</p></div>
      <div class="tablet tablet-cell"><div class="dev"><img src="{img("ipad-player")}" alt="{e(c["alt_ipad_player"])}" width="1400" height="1867" loading="lazy" decoding="async"></div></div>
    </article>
    <article class="cell c-cast" data-reveal>
      <div class="cast-icons">{icon("airplay", "ic ic-xl")}{icon("screencast", "ic ic-xl")}{icon("picture-in-picture", "ic ic-xl")}</div>
      <div class="cell-txt"><h3>{e(c["f_cast"][0])}</h3><p>{e(c["f_cast"][1])}</p></div>
    </article>
    <article class="cell c-search" data-reveal>
      <div class="cell-txt"><h3>{e(c["f_search"][0])}</h3><p>{e(c["f_search"][1])}</p></div>
      {phone(img("search"), c["alt_search"], "rise peek")}
    </article>
  </div>
</section>

<section class="land">
  <div class="land-copy" data-reveal>
    <h2>{e(c["land_h"])}</h2>
    <p>{e(c["land_sub"])}</p>
  </div>
  <div class="land-stage">
    <div class="phone-land"><div class="dev"><img src="{img("landscape")}" alt="{e(c["alt_land"])}" width="1800" height="828" loading="lazy" decoding="async"><span class="island" aria-hidden="true"></span></div></div>
  </div>
</section>

<section class="privacy">
  <h2 data-reveal><span>{e(c["priv_h1"])}</span><span>{e(c["priv_h2"])}</span></h2>
  <p data-reveal>{e(c["priv_sub"])}</p>
  <a class="link" href="{c["privacy"]}" data-reveal>{e(c["priv_link"])}{icon("arrow-right", "ic ic-btn")}</a>
</section>

<section class="pro" id="pro">
  <div class="pro-copy">
    <h2 data-reveal>{e(c["pro_h"])}</h2>
    <p class="pro-sub" data-reveal>{e(c["pro_sub"])}</p>
    <ul class="pro-list">
      {pro}
    </ul>
  </div>
  <div class="pro-art" data-reveal>{phone(img("look"), c["alt_look"], "look")}</div>
</section>

<section class="end">
  <div data-reveal>{mark("end-mark")}</div>
  <h2 data-reveal>{e(c["end_h"])}</h2>
  <p data-reveal>{e(c["end_sub"])}</p>
  <div data-reveal>{cta(c)}</div>
</section>
</main>

<footer class="foot">
  <div class="foot-in">
    <a class="brand" href="{c["file"]}" aria-label="Melyro">{wordmark()}</a>
    <nav aria-label="Melyro">
      <a href="{c["privacy"]}">{e(c["nav_privacy"])}</a>
      <a href="{c["support"]}">{e(c["nav_support"])}</a>
      <a href="mailto:support@melyro.app">support@melyro.app</a>
    </nav>
    <div class="langs" role="group" aria-label="{e(c["langs"])}">{lang_links(c)}</div>
  </div>
  <p class="tm">{e(c["tm"])}</p>
  <p class="tm">© 2026 Melyro</p>
</footer>
</body>
</html>
'''


def main(site):
    site = pathlib.Path(site)
    (site / "img").mkdir(exist_ok=True)
    for f in (HERE / "img").glob("*.webp"):
        shutil.copy(f, site / "img" / f.name)
    for extra in ("mark.svg", "apple-touch-icon.png", "og.png"):
        if (HERE / "img" / extra).exists():
            shutil.copy(HERE / "img" / extra, site / "img" / extra)
    shutil.copy(HERE / "home.css", site / "home.css")
    shutil.copy(HERE / "home.js", site / "home.js")
    for code in ORDER:
        text = page(COPY[code])
        assert "—" not in text and "–" not in text, f"dash in {code}"
        (site / COPY[code]["file"]).write_text(text)
        print("wrote", COPY[code]["file"], len(text))


if __name__ == "__main__":
    main(sys.argv[1])
