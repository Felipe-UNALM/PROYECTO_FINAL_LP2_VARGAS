""" limpieza.py: Filtra y limpia de manera determinante los strings,
aplicando un parche mediante expresiones regualares para eliminar caracteres 
de codificación corrupta heredados por la web."""

import re

from regex_patterns import PARCHE_LIMPIEZA_TEXTO

def limpiar_texto(texto):
    if not texto:
        return ""
    # Normaliza multiples espacios y saltos de línea a espacios simples
    texto_limpio = re.sub(r'\s+', ' ', texto)
    # Ejecuta el parche de depuración sintática
    texto_limpio = re.sub(PARCHE_LIMPIEZA_TEXTO, '', texto_limpio)
    return texto_limpio.strip()
