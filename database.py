import sqlite3
import json
import os

DB_NAME = "desinformacion.db"

def inicializar_db():
    """Crea la base de datos y la tabla si no existen."""
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
    print("¡Base de datos inicializada correctamente!")

def cargar_datos_desde_json(archivo_json, tipo_fuente):
    """Lee el archivo JSON de Felipe e inserta los datos reales en la DB."""
    if not os.path.exists(archivo_json):
        print(f"Aviso: No se encontró el archivo {archivo_json}")
        return

    # Leer el archivo JSON estructurado de Felipe
    with open(archivo_json, 'r', encoding='utf-8') as f:
        articulos_recopilados = json.load(f)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    registros_cargados = 0

    for item in articulos_recopilados:
        titulo = item.get('titulo', 'Sin título')
        autor = item.get('autor', 'Anónimo')
        fecha = item.get('fecha', 'Reciente')
        url = item.get('url', '')
        texto = item.get('texto_principal', '')
        
        # Calculamos cuántas referencias extrajo Felipe en su lista
        referencias_conteo = len(item.get('referencias', []))

        # --- LÓGICA TEMPORAL (Mientras Sergio termina su código) ---
        # Analizamos palabras clave básicas para simular el riesgo en el dashboard
        contenido_completo = (titulo + texto).lower()
        if "peligro" in contenido_completo or "oculto" in contenido_completo or "falsa" in contenido_completo:
            puntaje_ird = 8
            conspiranoico_detectado = 1
        elif tipo_fuente == "Oficial":
            puntaje_ird = -3
            conspiranoico_detectado = 0
        else:
            puntaje_ird = 3
            conspiranoico_detectado = 0
        # -----------------------------------------------------------

        try:
            cursor.execute('''
                INSERT INTO articulos (titulo, autor, fecha, url, texto_principal, tipo_fuente, puntaje_ird, conspiranoico_detectado, referencias_conteo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, autor, fecha, url, texto, tipo_fuente, puntaje_ird, conspiranoico_detectado, referencias_conteo))
            registros_cargados += 1
        except sqlite3.IntegrityError:
            # Si la URL ya existe en la DB, no la duplica
            pass

    conn.commit()
    conn.close()
    print(f"¡Se han cargado {registros_cargados} artículos nuevos desde {archivo_json}!")

if __name__ == "__main__":
    inicializar_db()
    # Procesamos la Fuente 1 (MedlinePlus -> Oficial)
    cargar_datos_desde_json("datos_raw.json", "Oficial")
    # Procesamos la Fuente 2 (Menéame -> Blog/Foro)
    cargar_datos_desde_json("datos_raw_meneame.json", "Blog")