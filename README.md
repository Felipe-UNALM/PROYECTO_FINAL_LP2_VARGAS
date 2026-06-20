# 📊 Sistema de Monitoreo de Indicadores de Desinformación Científica

Prototipo funcional desarrollado para la evaluación del **Taller 2** en el curso de **Lenguaje de Programación 2 (Semestre 2026-1)**. El sistema recopila contenido web relacionado con temas de salud y ciencia mediante técnicas de Web Scraping, procesa los textos mediante expresiones regulares (Regex) y calcula un **Índice de Riesgo de Desinformación (IRD)** automatizado, visualizando los resultados en un panel interactivo.

---

## 👥 Integrantes y Roles

* **Felipe** ([@Felipe-UNALM](https://github.com/Felipe-UNALM))  
    *Rol:* Encargado del Web Scraping.
* **Sergio** 
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
* **Control de Versiones:** Git & GitHub

---

## 📦 Estructura del Proyecto

```text
📦 PROYECTO_FINAL_LP2_VARGAS
 ┣ 📜 app.py                   # Código principal de la interfaz en Streamlit
 ┣ 📜 database.py              # Script de creación e integración de la Base de Datos SQLite
 ┣ 📜 desinformacion.db        # Archivo de base de datos relacional (Generado automáticamente)
 ┣ 📜 requerimientos.txt       # Listado de librerías y dependencias del proyecto
 ┗ 📜 resultados_simulados.csv # Datos estructurados base para la simulación del pipeline
