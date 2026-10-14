# melyro.app

`melyro.app` is served by the Cloudflare Worker `melyro-web` (`worker.js`). It fetches each path from
GitHub Pages (`https://cenkgundev.github.io/melyro-site/`) and returns it under the domain, so this
repository stays the only copy of the site. `www.melyro.app` and plain `http://` redirect to
`https://melyro.app`. The old github.io addresses keep working.

Deploy after changing the Worker: `npx wrangler@4 deploy` in this folder. Changes to the pages need no
deploy; the Worker caches each response for five minutes.

Mail: `support@melyro.app` is forwarded to the developer's inbox by Cloudflare Email Routing.
