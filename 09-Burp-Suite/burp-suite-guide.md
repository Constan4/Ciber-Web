# Burp Suite -- Guia de Uso

Burp Suite es el proxy/scanner estandar para pentesting web.
Intercepta todo el trafico entre el navegador y el servidor.

## Configuracion inicial

```bash
# Lanzar
burpsuite &

# Configurar proxy en Firefox:
# about:preferences -> Network Settings -> Manual Proxy
# HTTP: 127.0.0.1 Puerto: 8080

# Instalar certificado para HTTPS:
# 1. Con Firefox -> http://burpsuite
# 2. "CA Certificate" -> guardar como burp.cer
# 3. Firefox -> about:preferences -> Certificates -> Import
```

## Modulos principales

### Proxy -- Interceptar peticiones

```
Proxy -> Intercept -> Turn Intercept ON
Navegar en Firefox -> Burp captura cada peticion
-> Forward: dejar pasar
-> Drop: cancelar
-> Action -> Send to Repeater / Intruder / Scanner
```

### Repeater -- Modificar y reenviar peticiones

```
1. En Proxy -> HTTP History -> clic derecho -> Send to Repeater
2. Modificar cualquier parte de la peticion
3. Click Send -> ver respuesta
4. Ideal para: probar SQLi, XSS, cambiar parametros
```

### Intruder -- Ataques automatizados

```
1. Send to Intruder desde cualquier peticion
2. Marcar los parametros a atacar con *payload*
3. Payloads tab -> cargar wordlist
4. Tipos de ataque:
   - Sniper: un parametro, una wordlist
   - Cluster Bomb: varios parametros, varias wordlists

Uso tipico:
- Brute force de login (usuario y contrasena)
- Fuzzing de parametros
- Enumeracion de IDs (IDOR)
```

### Scanner -- Escaneo automatico (Pro)

```
# En la version Community, escaneo limitado
# Pro: escanea toda la app automaticamente
# Target -> Site Map -> clic derecho -> Active Scan
```

### Decoder -- Codificar/decodificar

```
# URL encode/decode, Base64, HTML entities, hex...
Decoder tab -> pegar texto -> elegir transformacion
```

### Comparer -- Comparar respuestas

```
# Util para detectar diferencias en Blind SQLi o enumeracion de usuarios
Send to Comparer desde dos respuestas -> Compare
```

## Tips practicos

```
1. Siempre mirar: HTTP History en Proxy
2. Buscar tokens JWT en cabeceras Authorization
3. Buscar claves API en respuestas JSON
4. Usar Search (Ctrl+F) en cualquier respuesta

# Wordlists integradas de Burp:
/usr/share/burp/wordlists/

# Extensiones utiles (BApp Store):
- JWT Editor: manipular tokens JWT
- Logger++: logging avanzado
- Param Miner: descubrir parametros ocultos
- ActiveScan++: mejorar el scanner
```
