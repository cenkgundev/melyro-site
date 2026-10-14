# Home page generator

`index.html`, `index-en.html` and `index-de.html` are written by `build_home.py`; edit the sources
here, not the pages.

- `home_copy.py`: every visible string, per language. No em-dashes (the build refuses them). Each
  claim is in the approved App Store description or the privacy policy.
- `home.css`, `home.js`: the look and the motion. The build copies them to the site root.
- Images in `img/` are the App Store capture set (raw screens, fictional content), resized to WebP.

Build, from this folder:

    npm pack @phosphor-icons/core@2.1.1 && mkdir -p ph && tar -xzf phosphor-icons-core-2.1.1.tgz -C ph
    mkdir -p img && cp ../../img/*.webp ../../img/og.png ../../img/mark.svg ../../img/apple-touch-icon.png img/
    python3 build_home.py ../..

Check in WebKit (the Safari engine), with the site served on 127.0.0.1:8811:

    swiftc -O shot.swift -o shot && ./shot 1440 900 http://127.0.0.1:8811/index.html out.png full "$(cat final.js)"

`final.js` turns animations off, because WebKit pauses them in an off-screen window. If you change
the hero headline, re-run `measure.swift` and update `H1_EMS` in `build_home.py`, so each line still
fits on one row.
