# Reconocimiento Web

El reconocimiento mapea la superficie de ataque antes de explotar nada.

## 1. Fingerprinting de tecnologias

```bash
whatweb http://objetivo.com -v
curl -sI http://objetivo.com

# Cabeceras reveladoras:
# Server: Apache/2.4.49     -> version del servidor
# X-Powered-By: PHP/7.4     -> lenguaje backend
# Set-Cookie: PHPSESSID     -> PHP | JSESSIONID -> Java/Spring
# X-Generator: WordPress    -> CMS
```

## 2. Deteccion de WAF

```bash
wafw00f http://objetivo.com
# Resultados: Cloudflare, ModSecurity, AWS WAF, Sucuri, Imperva...
# Si hay WAF -> necesitamos tecnicas de bypass en los payloads
```

## 3. Enumeracion de subdominios

```bash
sublist3r -d objetivo.com -o subdominios.txt
ffuf -u http://FUZZ.objetivo.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fc 302,404
gobuster dns -d objetivo.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

## 4. Fuzzing de directorios y archivos

```bash
# ffuf -- el mas rapido
ffuf -u http://objetivo.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fc 404

# Con extensiones
ffuf -u http://objetivo.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -e .php,.html,.txt,.bak,.zip,.sql -fc 404

# gobuster
gobuster dir -u http://objetivo.com -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -x php,html,txt -b 404

# nikto -- escaner automatico basico
nikto -h http://objetivo.com
```

## 5. Archivos sensibles criticos

```
/.git/HEAD          -> Repositorio Git expuesto -> codigo fuente completo
/.env               -> Credenciales y claves API en texto plano
/robots.txt         -> Rutas excluidas de indexacion (pueden ser jugosas)
/phpinfo.php        -> Informacion detallada del servidor PHP
/backup.zip         -> Backups de la aplicacion
/admin/ /wp-admin/  -> Paneles de administracion
/api/               -> Endpoints de API sin documentar
/config.php         -> Archivos de configuracion
/.htaccess          -> Configuracion Apache
/web.config         -> Configuracion IIS (Windows)
```

## 6. Script propio

```bash
python3 scripts/web_recon.py --url http://localhost:8080 --full
python3 scripts/web_recon.py --url http://objetivo.com --sensitive
```

## Checklist

```
[ ] Tecnologias identificadas (server, lenguaje, CMS, framework, versiones)
[ ] WAF detectado y tipo identificado
[ ] Subdominios enumerados
[ ] Directorios y archivos mapeados con ffuf/gobuster
[ ] Archivos sensibles buscados (.env, .git, backup...)
[ ] Parametros de entrada identificados
[ ] Formularios de login localizados
[ ] APIs descubiertas
[ ] Versiones identificadas para buscar CVEs
```
