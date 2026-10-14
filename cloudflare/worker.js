// melyro.app: serves https://cenkgundev.github.io/melyro-site/ under the apex domain.
const ORIGIN = "https://cenkgundev.github.io/melyro-site";

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.hostname !== "melyro.app" || url.protocol === "http:") {
      return Response.redirect("https://melyro.app" + url.pathname + url.search, 301);
    }
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405 });
    }
    const upstream = await fetch(ORIGIN + url.pathname + url.search, {
      method: request.method,
      redirect: "manual",
      cf: { cacheTtl: 300, cacheEverything: true },
    });
    const headers = new Headers(upstream.headers);
    const location = headers.get("location");
    if (location) headers.set("location", location.replace(ORIGIN, "https://melyro.app").replace("http://cenkgundev.github.io/melyro-site", "https://melyro.app"));
    headers.delete("x-github-request-id");
    headers.set("strict-transport-security", "max-age=31536000");
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};
