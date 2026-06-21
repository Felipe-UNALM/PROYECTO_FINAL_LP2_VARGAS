# score_ird.py
import json
import os
import pandas as pd
from limpieza import limpiar_texto
import regex_patterns as rx


def calcular_ird(articulo, idx):
    titulo = articulo.get("titulo", "").strip()
    url = articulo.get("url", "").strip()
    autor = articulo.get("autor", "").strip()
    fecha = articulo.get("fecha", "").strip()
    texto_principal = articulo.get("texto_principal", "").strip()
    referencias = articulo.get("referencias", [])
    enlaces_externos = articulo.get("enlaces_externos", 0)

    # Combinamos para un escaneo semántico integral
    cuerpo_analisis = limpiar_texto(f"{titulo} {texto_principal}")

    # Evaluación de ausencias basales de credibilidad
    sin_autor = 1 if not autor or "Anónimo" in autor or autor == "" else 0
    sin_fecha = 1 if not fecha or "Reciente" in fecha or fecha == "" else 0
    sin_referencias = 1 if not referencias or len(referencias) == 0 else 0

    # Evaluación lingüística usando los nombres exactos de regex_patterns.py
    tiene_conspiracion = (
        1 if rx.REGEX_CONSPIRATIVAS.search(cuerpo_analisis) else 0
    )
    tiene_alarmismo = 1 if rx.REGEX_ALARMISTAS.search(cuerpo_analisis) else 0
    tiene_ciencia = 1 if rx.REGEX_CIENTIFICA.search(cuerpo_analisis) else 0

    ref_string = (
        " ".join(referencias)
        if isinstance(referencias, list)
        else str(referencias)
    )

    tiene_doi_pubmed = (
        1
        if (
            rx.REGEX_DOI_PUBMED.search(cuerpo_analisis)
            or rx.REGEX_DOI_PUBMED.search(ref_string)
        )
        else 0
    )

    tiene_organismo_oficial = (
        1
        if (
            rx.REGEX_ORGANISMOS.search(cuerpo_analisis)
            or rx.REGEX_ORGANISMOS.search(url)
        )
        else 0
    )

    # Fórmula del Modelo Aditivo y Sustractivo IRD de la Rúbrica
    score_ird = 0

    if sin_autor:
        score_ird += 2

    if sin_fecha:
        score_ird += 1

    if sin_referencias:
        score_ird += 3

    if tiene_conspiracion:
        score_ird += 3

    if tiene_alarmismo:
        score_ird += 2

    if tiene_ciencia:
        score_ird -= 3

    if tiene_doi_pubmed:
        score_ird -= 2

    if tiene_organismo_oficial:
        score_ird -= 2

    return {
        "id_articulo": idx,
        "titulo": titulo if titulo else "Sin título",
        "fecha": fecha if fecha else "Sin fecha",
        "autor": autor if autor else "Sin autor",
        "url": url if url else "Sin URL",
        "texto_principal": texto_principal,
        "cantidad_enlaces": enlaces_externos,
        "sin_autor": sin_autor,
        "sin_fecha": sin_fecha,
        "sin_referencias": sin_referencias,
        "tiene_conspiracion": tiene_conspiracion,
        "tiene_alarmismo": tiene_alarmismo,
        "score_ird": score_ird,
    }


def ejecutar_pipeline():
    articulos_procesados = []
    idx = 1

    if os.path.exists("datos_raw.json"):
        with open("datos_raw.json", "r", encoding="utf-8") as f:
            for art in json.load(f):
                articulos_procesados.append(calcular_ird(art, idx))
                idx += 1

    if os.path.exists("datos_raw_meneame.json"):
        with open("datos_raw_meneame.json", "r", encoding="utf-8") as f:
            for art in json.load(f):
                articulos_procesados.append(calcular_ird(art, idx))
                idx += 1

    df = pd.DataFrame(articulos_procesados)
    df.to_csv("resultados_analisis.csv", index=False, encoding="utf-8-sig")
    return df


if __name__ == "__main__":
    ejecutar_pipeline()
    