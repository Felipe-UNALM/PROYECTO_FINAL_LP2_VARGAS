import sqlite3
import pandas as pd
import os

DB_NAME = "desinformacion.db"
CSV_NAME = "resultados_simulados.csv"

def inicializar_db():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Creamos la tabla con las columnas exactas de nuestro CSV
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
    print("¡Base de datos y tabla 'articulos' inicializadas con éxito!")

def cargar_datos_desde_csv():
    """Lee el CSV e inserta los datos en SQLite evitando duplicados por URL."""
    if not os.path.exists(CSV_NAME):
        print(f"Error: No se encontró el archivo {CSV_NAME}")
        return

    # Leemos el CSV usando la librería Pandas
    df = pd.read_csv(CSV_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    
    # Cargamos los datos. if_exists='append' significa que agrega los datos nuevos
    try:
        df.to_sql('articulos', conn, if_exists='append', index=False)
        print(f"¡Se han cargado {len(df)} artículos correctamente a la base de datos!")
    except sqlite3.IntegrityError:
        print("Nota: Algunos artículos no se duplicaron porque sus URLs ya existían en la DB.")
    
    conn.close()

if __name__ == "__main__":
    inicializar_db()
    cargar_datos_desde_csv()