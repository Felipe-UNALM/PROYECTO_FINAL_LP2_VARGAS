import sqlite3
import pandas as pd
import os
import subprocess

# Nombre exacto del flujo oficial acordado por el grupo
DB_NAME = "monitor_desinformacion.db"
CSV_ANALISIS = "resultados_analisis.csv"

def inicializar_db():
    """Crea la base de datos relacional y la tabla estructurada limpia."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            fecha TEXT,
            url TEXT UNIQUE,
            texto_principal TEXT,
            tipo_fuente TEXT,
            puntaje_ird INTEGER,
            conspiranoico_detectado INTEGER,
            referencias_conteo INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("¡Base de datos SQLite inicializada de forma limpia!")

def integrar_datos_desde_csv():
    """Toma el CSV generado por Sergio y lo mete a la DB (Paso 3 del flujo)."""
    if not os.path.exists(CSV_ANALISIS):
        print(f"❌ Error Crítico: No se encontró el archivo '{CSV_ANALISIS}'.")
        return

    print(f"📥 Leyendo '{CSV_ANALISIS}' generado por Sergio...")
    df_analizado = pd.read_csv(CSV_ANALISIS)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    registros_insertados = 0

    for _, row in df_analizado.iterrows():
        url = str(row['url'])
        
        # Clasificación automática según el dominio de la URL de origen
        if "medlineplus.gov" in url.lower():
            tipo_fuente = "Oficial"
        else:
            tipo_fuente = "Blog"

        # Mapeamos los datos calculados por las expresiones regulares de Sergio
        titulo = row['titulo']
        autor = row['autor']
        fecha = row['fecha']
        texto_principal = row['texto_principal']
        puntaje_ird = int(row['score_ird'])
        
        # Consideramos riesgo crítico si tiene conspiración activa o puntaje alto (>= 4)
        conspiranoico_detectado = 1 if row['tiene_conspiracion'] == 1 or puntaje_ird >= 4 else 0
        referencias_conteo = 0 if row['sin_referencias'] == 1 else 1

        try:
            cursor.execute('''
                INSERT INTO articulos (titulo, autor, fecha, url, texto_principal, tipo_fuente, puntaje_ird, conspiranoico_detectado, referencias_conteo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, autor, fecha, url, texto_principal, tipo_fuente, puntaje_ird, conspiranoico_detectado, referencias_conteo))
            registros_insertados += 1
        except sqlite3.IntegrityError:
            # Evita duplicar registros si corren el script varias veces en la misma DB
            pass

    conn.commit()
    conn.close()
    print(f"✅ ¡Éxito! Se han cargado {registros_insertados} artículos analizados en '{DB_NAME}'.")

if __name__ == "__main__":
    # PASO 2 DEL FLUJO: Forzamos la ejecución automática del script de Sergio para generar el CSV fresco
    print("🚀 Ejecutando el analizador de Sergio (score_ird.py)...")
    try:
        subprocess.run(["python", "score_ird.py"], check=True)
        print("✨ CSV 'resultados_analisis.csv' generado con éxito por el módulo de Sergio.")
    except Exception as e:
        print("⚠️ Nota: Verifica que score_ird.py corra sin problemas de dependencias.")

    # PASO 3 DEL FLUJO: Inicializamos tu DB e insertamos la data extraída del CSV de Sergio
    inicializar_db()
    integrar_datos_desde_csv()