# Configuracion del Laboratorio Web

## Opcion A -- Docker (recomendado)

```bash
sudo apt install docker.io -y && sudo systemctl start docker

# DVWA -- Damn Vulnerable Web Application
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
# Acceder: http://localhost:8080  |  admin / password  |  Security: Low

# WebGoat
docker run -d --name webgoat -p 9090:8080 webgoat/webgoat
# Acceder: http://localhost:9090/WebGoat

# Juice Shop (el mas moderno, mas parecido a una app real)
docker run -d --name juiceshop -p 3000:3000 bkimminich/juice-shop
# Acceder: http://localhost:3000

docker ps  # ver todos activos
```

## Opcion B -- Plataformas online

- PortSwigger Web Security Academy: https://portswigger.net/web-security
  Labs gratuitos de SQLi, XSS, CSRF, SSRF, IDOR, JWT...
- HackTheBox: https://hackthebox.com
- TryHackMe: https://tryhackme.com

## Configurar Burp Suite

```bash
burpsuite &
# Firefox: Preferencias -> Red -> Proxy Manual
# HTTP: 127.0.0.1 Puerto: 8080
# Instalar CA: http://burpsuite -> Download CA Certificate -> importar en Firefox
```

## Wordlists

```bash
sudo apt install seclists -y
ls /usr/share/seclists/Discovery/Web-Content/
ls /usr/share/seclists/Fuzzing/
```
