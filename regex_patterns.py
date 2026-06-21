""" regex_patterns.py: Centraliza todas las expresiones regulares requeridas
para rastrear patrones lingüísticos, adjetivos alarmistas, frases conspirativas,
y los elementos mitigadores (como citas a universidades, registradas DOI o PubMed.)"""

import re
# Para remover caracteres corruptos de transferencia de HTML web.
PARCHE_LIMPIEZA_TEXTO = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s.,;:!?¿¡\-()\"\']'
# 1. FACTORES DE RIESGO LINGUISTICO (+2 puntos en el IRD)
PALABRAS_CLAVE_ALARMISTAS = [
    r'alarmante', r'peligro oculto', r'estragos masivos', r'mortal', r'destrucción',
    r'pánico', r'terror', r'amenaza silenciosa', r'efectos desvatadores', r'veneno cotidiano'
]
REGEX_ALARMISTAS = re.compile("|".join(PALABRAS_CLAVE_ALARMISTAS), re.IGNORECASE)

# 2. Frases de toerias cospirativas (+3 puntos en el IRD)
PALABRAS_CLAVE_CONSPIRATIVAS = [
    r'la ciencia ignora', r'silencio isntitucional', r'lo que no quieren que sepas', 
    r'estudio alternativo', r'ocultan', r'control mundial', r'el gobierno miente',
    r'plan secreto', r'experimento humano']
REGEX_CONSPIRATIVAS = re.compile("|".join(PALABRAS_CLAVE_CONSPIRATIVAS), re.IGNORECASE)

#3. Mitigación: Respaldo de comunidad cientifica (-3 puntos en el IRD)

PALABRAS_CLAVE_CIENTIFICAS = [
    r'científicos', r'investigadores', r'estudio clínico', r'universidad de',
    r'revista científica', r'ensayo controlado', r'evidencia médica'
]
REGEX_CIENTIFICA = re.compile("|".join(PALABRAS_CLAVE_CIENTIFICAS), re.IGNORECASE)

#4. Mitigación: Ligas DOI o PubMed (-2 puntos en el IRD)
PALABRAS_CLAVE_DOI_PUBMED = [r'doi\.org', r'pubmed\.ncbi\.nlm\.nih\.gov']
REGEX_DOI_PUBMED = re.compile("|".join(PALABRAS_CLAVE_DOI_PUBMED), re.IGNORECASE)

#5. Mitigación: Organismos gubernamentales o de salud reconocidos (-2 puntos en el IRD)
PALABRAS_CLAVE_ORGANISMOS = [r'oms', r'cdc',r'medlineplus', r'minsa', r'fda', r'\.gov', r'\.gob']
REGEX_ORGANISMOS = re.compile("|".join(PALABRAS_CLAVE_ORGANISMOS), re.IGNORECASE)
