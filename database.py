import sqlite3
import pandas as pd
import os
import subprocess

# Nombre de la base de datos oficial del flujo
DB_NAME = "monitor_desinformacion.db"
CSV_ANALISIS = "resultados_analisis.csv"

def inicializar_db():
    """Crea la base de datos relacional con las columnas exactas pedidas por Sergio."""
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
            frases_alarmistas INTEGER,
            referencias_cientificas INTEGER,
            puntaje_ird INTEGER,
            clasificacion TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("¡Base de datos SQLite inicializada con el nuevo esquema de Sergio!")

def integrar_datos_desde_csv():
    """Toma el CSV de Sergio y lo estructura bajo el nuevo formato relacional."""
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
        puntaje_ird = int(row['score_ird'])
        
        # Clasificación automática de la fuente
        if "medlineplus.gov" in url.lower():
            tipo_fuente = "Oficial"
            referencias_cientificas = 1  # Cuenta como mitigación científica válida
        else:
            tipo_fuente = "Blog"
            referencias_cientificas = 0

        titulo = row['titulo']
        autor = row['autor']
        fecha = row['fecha']
        texto_principal = row['texto_principal']
        
        # Variables numéricas y semánticas solicitadas por Sergio
        frases_alarmistas = int(row['tiene_alarmismo'])
        
        # Lógica estricta de clasificación para la exposición
        if puntaje_ird >= 4 or int(row['tiene_conspiracion']) == 1:
            clasificacion = "ALTO RIESGO"
        else:
            clasificacion = "CONFIABLE"

        try:
            cursor.execute('''
                INSERT INTO articulos (titulo, autor, fecha, url, texto_principal, tipo_fuente, frases_alarmistas, referencias_cientificas, puntaje_ird, clasificacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, autor, fecha, url, texto_principal, tipo_fuente, frases_alarmistas, referencias_cientificas, puntaje_ird, clasificacion))
            registros_insertados += 1
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f"✅ ¡Éxito! Se han indexado {registros_insertados} registros limpios en '{DB_NAME}'.")

if __name__ == "__main__":
    print("🚀 Iniciando motor analítico de expresiones regulares (Sergio)...")
    try:
        subprocess.run(["python", "score_ird.py"], check=True)
        print("✨ CSV 'resultados_analisis.csv' generado con éxito.")
    except Exception as e:
        print("⚠️ Nota: Verifica que score_ird.py corra sin problemas.")

    inicializar_db()
    integrar_datos_desde_csv()