// Reveals sections as they enter the viewport. Without JavaScript, or with reduced motion, everything
// is simply visible: the hidden state only exists under the .js class this file sets.
(function () {
  var root = document.documentElement;
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  root.classList.add("js");
  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      seen.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
  document.querySelectorAll("[data-reveal]").forEach(function (el) { seen.observe(el); });
})();
