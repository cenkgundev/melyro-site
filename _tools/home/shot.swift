// shot <width> <viewportHeight> <url> <out.png> [scrollY|full] [js]
// Loads a page in WKWebView (the Safari engine). "full" grows the view to the document height and
// snapshots everything; a number scrolls there and snapshots one viewport. Output is 2x.
import AppKit
import WebKit

let a = Array(CommandLine.arguments.dropFirst())
let width = CGFloat(Double(a[0])!), vh = CGFloat(Double(a[1])!)
let url = URL(string: a[2])!, out = a[3]
let mode = a.count > 4 ? a[4] : "full"
let js = a.count > 5 ? a[5] : ""

final class Shot: NSObject, WKNavigationDelegate {
    let web: WKWebView
    let window: NSWindow
    override init() {
        let config = WKWebViewConfiguration()
        web = WKWebView(frame: CGRect(x: 0, y: 0, width: width, height: vh), configuration: config)
        window = NSWindow(contentRect: CGRect(x: -30000, y: -30000, width: width, height: vh),
                          styleMask: [.borderless], backing: .buffered, defer: false)
        super.init()
        window.contentView = web
        window.orderFrontRegardless()
        web.navigationDelegate = self
        web.load(URLRequest(url: url))
    }
    func webView(_ w: WKWebView, didFinish n: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.6) { self.prepare() }
    }
    func prepare() {
        web.evaluateJavaScript(js.isEmpty ? "0" : js) { _, _ in
            if self.mode == "full" {
                self.web.evaluateJavaScript("document.documentElement.scrollHeight") { h, _ in
                    let height = CGFloat((h as? NSNumber)?.doubleValue ?? Double(vh))
                    self.window.setContentSize(NSSize(width: width, height: height))
                    self.web.frame = CGRect(x: 0, y: 0, width: width, height: height)
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2.2) { self.snap(height) }
                }
            } else {
                self.web.evaluateJavaScript("window.scrollTo(0, \(self.mode))") { _, _ in
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1.6) { self.snap(vh) }
                }
            }
        }
    }
    var mode: String { return modeArg }
    func snap(_ height: CGFloat) {
        let c = WKSnapshotConfiguration()
        c.rect = CGRect(x: 0, y: 0, width: width, height: height)
        c.snapshotWidth = NSNumber(value: Double(width * 2))
        web.takeSnapshot(with: c) { image, error in
            guard let image, let tiff = image.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
                  let png = rep.representation(using: .png, properties: [:]) else { print("FAIL", error as Any); exit(1) }
            try! png.write(to: URL(fileURLWithPath: out))
            print("ok", out, Int(height)); exit(0)
        }
    }
}
let modeArg = mode
let app = NSApplication.shared
let shot = Shot()
DispatchQueue.main.asyncAfter(deadline: .now() + 90) { print("timeout"); exit(1) }
app.run()
