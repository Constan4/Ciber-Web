# 🕷️ Ciber-Web — Web Application Penetration Testing

<p align="center">
  <img src="https://img.shields.io/badge/Enfoque-Web%20Security%20%2F%20Ofensivo-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OWASP-Top%2010%202021-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Tools-Burp%20Suite%20%7C%20sqlmap%20%7C%20ffuf-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  <b>Guía completa de pentesting de aplicaciones web.</b><br/>
  Desde el reconocimiento hasta la explotación de las vulnerabilidades más críticas.
</p>

---

## Kill Chain Web

```
  [Objetivo web]
        │
        ▼
  01 Reconocimiento ──► Subdominios · Directorios · Tecnologías · WAF
        │
        ▼
  02 SQL Injection ──► Detección · Extracción · Bypass · sqlmap
        │
        ▼
  03 XSS ──────────► Reflected · Stored · DOM · Cookie Stealing
        │
        ▼
  04 LFI / RFI ────► Path Traversal · Log Poisoning · PHP Wrappers
        │
        ▼
  05 SSRF ─────────► Metadata Cloud · Port Scan Interno · Bypass
        │
        ▼
  06 Autenticación ► Brute Force · JWT · OAuth · Session Fixation
        │
        ▼
  07 File Upload ──► Bypass · Webshell · RCE
        │
        ▼
  08 API Security ─► REST · GraphQL · IDOR · Rate Limiting
```

---

## Módulos

| # | Módulo | Vulnerabilidades | Script |
|---|--------|-----------------|--------|
| 01 | [Reconocimiento](01-Reconocimiento/) | Subdominios, directorios, WAF, fingerprint | `web_recon.py` |
| 02 | [SQL Injection](02-SQL-Injection/) | Error, Blind, Time, Out-of-Band, sqlmap | `sqli_scanner.py` |
| 03 | [XSS](03-XSS/) | Reflected, Stored, DOM, CSP bypass | `xss_scanner.py` |
| 04 | [LFI / RFI](04-LFI-RFI/) | Path traversal, log poisoning, wrappers | `lfi_scanner.py` |
| 05 | [SSRF](05-SSRF/) | Internal network, cloud metadata, bypass | `ssrf_scanner.py` |
| 06 | [Autenticación](06-Autenticacion/) | Brute force, JWT, OAuth, MFA bypass | `auth_attack.py` |
| 07 | [File Upload](07-File-Upload/) | Extensión bypass, webshell, RCE | `upload_bypass.py` |
| 08 | [API Security](08-API-Security/) | IDOR, mass assignment, GraphQL, rate limit | `api_scanner.py` |
| 09 | [Burp Suite](09-Burp-Suite/) | Guía completa de uso profesional | — |
| 10 | [OWASP Top 10](10-OWASP-Top10/) | Los 10 riesgos web más críticos 2021 | — |

---

## Laboratorio

```
┌─────────────────────────────────────────────────────┐
│  Kali Linux (atacante)    192.168.1.35               │
│       │                                              │
│       ▼                                              │
│  DVWA  (Docker)           http://localhost:8080      │
│  WebGoat (Docker)         http://localhost:9090      │
│  HackTheBox / TryHackMe   Máquinas online            │
│  PortSwigger Labs         https://portswigger.net    │
└─────────────────────────────────────────────────────┘
```

Ver [lab/setup-laboratorio.md](lab/setup-laboratorio.md)

---

## Herramientas esenciales

| Herramienta | Uso | Instalación |
|-------------|-----|-------------|
| **Burp Suite** | Proxy + scanner + intruder | `apt install burpsuite` |
| **sqlmap** | SQL Injection automatizado | `apt install sqlmap` |
| **ffuf** | Fuzzing de rutas, parámetros | `apt install ffuf` |
| **gobuster** | Directory/subdomain enum | `apt install gobuster` |
| **nikto** | Escaner web básico | `apt install nikto` |
| **wafw00f** | Detección de WAF | `pip install wafw00f` |
| **whatweb** | Fingerprinting de tecnologías | `apt install whatweb` |
| **wfuzz** | Fuzzing avanzado | `apt install wfuzz` |
| **sublist3r** | Enumeración de subdominios | `pip install sublist3r` |

---

## Inicio rápido

```bash
# Instalar todo lo necesario
sudo apt update && sudo apt install -y burpsuite sqlmap ffuf gobuster nikto whatweb wfuzz

# Levantar el laboratorio local con Docker
docker run -d -p 8080:80 vulnerables/web-dvwa
docker run -d -p 9090:8080 webgoat/webgoat

# Primer reconocimiento
python3 01-Reconocimiento/scripts/web_recon.py --url http://localhost:8080

# OWASP Top 10 — empezar por aquí
cat 10-OWASP-Top10/owasp-top10-2021.md
```

---

## ⚠️ Aviso Legal

> Exclusivamente para uso educativo en entornos propios o con autorización expresa.
> El acceso no autorizado a sistemas informáticos es un delito penal.

---

*Constan4 — Web Application Security*
