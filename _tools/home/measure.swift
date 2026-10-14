import AppKit
import WebKit
let urls = Array(CommandLine.arguments.dropFirst())
final class M: NSObject, WKNavigationDelegate {
    let web = WKWebView(frame: CGRect(x: 0, y: 0, width: 1440, height: 900))
    var queue: [String]
    init(_ q: [String]) { queue = q; super.init(); web.navigationDelegate = self; next() }
    func next() { guard let u = queue.first else { exit(0) }; web.load(URLRequest(url: URL(string: u)!)) }
    func webView(_ w: WKWebView, didFinish n: WKNavigation!) {
        let js = "var h=document.querySelector('.hero h1');h.style.fontSize='100px';h.style.animation='none';var r=[];h.querySelectorAll('span').forEach(s=>{s.style.whiteSpace='nowrap';s.style.display='inline-block';s.style.animation='none';r.push(s.getBoundingClientRect().width)});var c=document.querySelector('.hero-copy').getBoundingClientRect().width;JSON.stringify({spans:r,col:c})"
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            w.evaluateJavaScript(js) { r, e in print(self.queue.removeFirst(), r ?? e as Any); self.next() }
        }
    }
}
let app = NSApplication.shared
let m = M(urls)
app.run()
