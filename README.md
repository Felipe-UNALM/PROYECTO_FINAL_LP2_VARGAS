# 📊 Sistema de Monitoreo de Indicadores de Desinformación Científica

Prototipo funcional desarrollado para la evaluación del **Taller 2** en el curso de **Lenguaje de Programación 2 (Semestre 2026-1)**. El sistema recopila contenido web relacionado con temas de salud y ciencia mediante técnicas de Web Scraping, procesa los textos mediante expresiones regulares (Regex) y calcula un **Índice de Riesgo de Desinformación (IRD)** automatizado, visualizando los resultados en un panel interactivo conectado a una base de datos relacional.

---

## 👥 Integrantes y Roles

* **Felipe** ([@Felipe-UNALM](https://github.com/Felipe-UNALM))  
    *Rol:* Encargado del Web Scraping.
* **Sergio** ([@sergiomendoza290803-wq](https://github.com/sergiomendoza290803-wq))  
    *Rol:* Encargado de procesamiento de texto, Regex y diseño del modelo heurístico IRD.
* **Isaac** ([@IsaacAlvarezCaja2026](https://github.com/IsaacAlvarezCaja2026))  
    *Rol:* Encargado de arquitectura de datos (SQLite), integración y visualización (Streamlit).

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.12+
* **Web Scraping:** Requests, BeautifulSoup4
* **Análisis Textual:** Expresiones Regulares (Librería nativa `re`)
* **Base de Datos:** SQLite3 (Persistencia local relacional)
* **Dashboard:** Streamlit (Interfaz de usuario interactiva)
* **Visualización:** Plotly Express & Matplotlib
* **Control de Versiones:** Git & GitHub

---

## 📦 Estructura del Proyecto

```text
📦 PROYECTO_FINAL_LP2_VARGAS
 ┣ 📜 app.py                    # Código principal del Dashboard interactivo en Streamlit
 ┣ 📜 database.py               # Script de arquitectura de datos unificada e inyección a SQLite
 ┣ 📜 monitor_desinformacion.db # Base de datos relacional SQLite (Persistencia estructurada)
 ┣ 📜 limpieza.py               # Funciones de limpieza de cadenas de texto
 ┣ 📜 regex_patterns.py         # Diccionario de patrones y expresiones regulares
 ┣ 📜 robots_checker.py         # Validador de permisos de acceso web (robots.txt)
 ┣ 📜 score_ird.py              # Algoritmo matemático del Índice de Riesgo de Desinformación
 ┣ 📜 scraper_fuente1.py        # Extractor automatizado para MedlinePlus
 ┣ 📜 scraper_fuente2.py        # Extractor automatizado para Menéame
 ┗ 📜 requerimientos.txt        # Listado estandarizado de dependencias del proyecto
```
