#!/usr/bin/env python3
"""
web_recon.py -- Reconocimiento automatizado de aplicaciones web
Uso:
    python3 web_recon.py --url http://objetivo.com
    python3 web_recon.py --url http://objetivo.com --full
    python3 web_recon.py --url http://objetivo.com --sensitive
"""
import argparse, subprocess, sys, urllib.request, urllib.error
from urllib.parse import urlparse

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";CYAN="[96m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def warn(m): print(C.YELLOW+"  [!] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [FOUND] "+C.RESET+m)

SENSITIVE_PATHS = [
    "/.git/HEAD","/.env","/.env.local","/.env.production",
    "/robots.txt","/sitemap.xml","/phpinfo.php","/info.php",
    "/admin/","/administrator/","/wp-admin/","/wp-login.php",
    "/backup.zip","/backup.tar.gz","/backup.sql","/dump.sql",
    "/.htaccess","/.htpasswd","/web.config","/config.php",
    "/config.yml","/config.json","/api/","/api/v1/","/swagger",
    "/swagger-ui","/api-docs","/openapi.json","/graphql",
    "/actuator","/actuator/health","/actuator/env",
]

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, len(r.read())
    except urllib.error.HTTPError as e:
        return e.code, 0
    except Exception:
        return None, 0

def get_headers(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return dict(r.headers)
    except Exception:
        return {}

def run_tool(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.stdout + r.stderr
    except FileNotFoundError:
        return ""
    except subprocess.TimeoutExpired:
        return ""

def banner():
    print(C.CYAN+C.BOLD+"""
  ╔═══════════════════════════════════════════╗
  ║   WEB_RECON -- Reconocimiento Web         ║
  ╚═══════════════════════════════════════════╝
"""+C.RESET)

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--url",       required=True)
    p.add_argument("--full",      action="store_true")
    p.add_argument("--sensitive", action="store_true")
    args = p.parse_args()

    url    = args.url.rstrip("/")
    parsed = urlparse(url)
    host   = parsed.netloc

    print("  URL    : "+url)
    print("  Host   : "+host)
    print()

    # 1. Cabeceras HTTP
    info("Analizando cabeceras HTTP...")
    headers = get_headers(url)
    interesting = ["Server","X-Powered-By","X-Generator","X-Framework",
                   "Set-Cookie","Access-Control-Allow-Origin","Content-Security-Policy"]
    for h in interesting:
        if h in headers:
            val = headers[h]
            ok(h+": "+val[:80])
            if h in ("Server","X-Powered-By","X-Generator"):
                crit("Tecnologia identificada: "+val[:60])

    print()

    # 2. WhatWeb
    info("Fingerprinting con WhatWeb...")
    ww = run_tool(["whatweb", url, "-q"])
    if ww:
        for line in ww.split("
")[:5]:
            if line.strip():
                ok(line.strip()[:100])

    print()

    # 3. Archivos sensibles
    if args.sensitive or args.full:
        info("Buscando archivos sensibles...")
        found = []
        for path in SENSITIVE_PATHS:
            full_url = url + path
            code, size = check_url(full_url)
            if code and code not in (404, 403, 400):
                crit(str(code)+" "+full_url)
                found.append(full_url)
        if not found:
            ok("No se encontraron archivos sensibles expuestos")
        print()

    # 4. Nikto si --full
    if args.full:
        info("Ejecutando nikto (puede tardar unos minutos)...")
        nk = run_tool(["nikto", "-h", url, "-maxtime", "60"])
        if nk:
            for line in nk.split("
"):
                if "+ " in line:
                    warn(line.strip()[:100])
        print()

    # 5. Resumen
    sep = "="*55
    print("  "+sep)
    print(C.BOLD+"  SIGUIENTE PASO"+C.RESET)
    print("  "+sep)
    print("  ffuf -u "+url+"/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fc 404")
    print("  python3 ../02-SQL-Injection/scripts/sqli_scanner.py --url "+url+"/search?q=test")
    print()

if __name__ == "__main__":
    main()
