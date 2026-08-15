# OWASP Top 10 -- 2021

Los 10 riesgos de seguridad mas criticos en aplicaciones web.

---

## A01 -- Broken Access Control

Usuarios acceden a recursos o funciones para los que no tienen permiso.

```
IDOR: /api/users/1234 -> cambiar a /api/users/1235
Path traversal: ../../../../etc/passwd
Forzar URLs de admin: /admin/users sin estar autenticado
```

---

## A02 -- Cryptographic Failures

Datos sensibles sin cifrar o con cifrado debil.

```
HTTP en vez de HTTPS (datos en texto plano)
Contrasenas en MD5 sin salt (crackeable con rainbow tables)
Claves hardcodeadas en el codigo fuente
Certificados SSL caducados o autofirmados
```

---

## A03 -- Injection

SQL, XSS, Command Injection, LDAP, etc.

```sql
-- SQLi: ' OR 1=1--
-- XSS: <script>alert(1)</script>
-- Command: ; cat /etc/passwd
-- LDAP: *)(uid=*))(|(uid=*
```

---

## A04 -- Insecure Design

Errores en el diseno de la logica de negocio.

```
Reseteo de contrasena sin verificacion
Flujos de pago sin validacion del lado del servidor
Funciones que dependen solo de validacion del cliente (JavaScript)
```

---

## A05 -- Security Misconfiguration

Configuraciones por defecto inseguras.

```
Credenciales por defecto: admin/admin
Puertos y servicios innecesarios abiertos
Stack traces detallados en produccion
CORS permisivo: Access-Control-Allow-Origin: *
Directorio listing habilitado
```

---

## A06 -- Vulnerable and Outdated Components

Usar librerias o frameworks con vulnerabilidades conocidas.

```bash
# Detectar versiones
whatweb http://objetivo.com
# Buscar CVEs para las versiones encontradas
# https://nvd.nist.gov/ o searchsploit
searchsploit apache 2.4.49
```

---

## A07 -- Identification and Authentication Failures

Fallos en autenticacion y gestion de sesiones.

```
Contrasenas debiles permitidas
Sin limitacion de intentos de login (brute force posible)
Tokens de sesion predecibles
JWT con algoritmo "none"
```

---

## A08 -- Software and Data Integrity Failures

Usar codigo o datos sin verificar integridad.

```
Deserializacion insegura -> RCE
CI/CD sin verificacion de paquetes (supply chain attacks)
npm packages maliciosos
```

---

## A09 -- Security Logging and Monitoring Failures

No registrar o monitorizar eventos de seguridad.

```
Sin logs de intentos de login fallidos
Sin alertas de comportamiento anomalo
Logs sin proteccion -> borrados por el atacante
```

---

## A10 -- Server-Side Request Forgery (SSRF)

El servidor hace peticiones a URLs controladas por el atacante.

```
?url=http://169.254.169.254/metadata  -> AWS metadata
?url=http://localhost:6379            -> Redis interno
?url=http://192.168.1.1/admin        -> red interna
```
