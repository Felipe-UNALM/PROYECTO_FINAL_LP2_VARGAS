import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página web
st.set_page_config(page_title="Monitoreo de Desinformación", layout="wide", page_icon="📊")

# Título principal del Dashboard
st.title("📊 Sistema de Monitoreo de Indicadores de Desinformación Científica")
st.markdown("### Prototipo de detección de señales de riesgo en artículos de salud")
st.write("Este sistema analiza textos web mediante heurísticas lógicas para calcular el Índice de Riesgo de Desinformación (IRD).")

st.divider()

# Función para conectar a la DB y jalar los datos
def cargar_datos_db():
    conn = sqlite3.connect("monitor_desinformacion.db")
    # Traemos todos los artículos guardados en la tabla
    df = pd.read_sql_query("SELECT * FROM articulos", conn)
    conn.close()
    return df

df_articulos = cargar_datos_db()

if not df_articulos.empty:
    # --- SECCIÓN 1: MÉTRICAS GLOBALES ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Artículos Analizados", value=len(df_articulos))
        
    with col2:
        promedio_ird = df_articulos['puntaje_ird'].mean()
        st.metric(label="Índice IRD Promedio Global", value=f"{promedio_ird:.1f} pts")
        
    with col3:
        # Consideramos alto riesgo si el score es mayor o igual a 4
        alto_riesgo = len(df_articulos[df_articulos['puntaje_ird'] >= 4])
        st.metric(label="Artículos de Alto Riesgo Detectados", value=alto_riesgo, delta="Alerta", delta_color="inverse")

    st.divider()

    # --- SECCIÓN 2: GRÁFICOS INTERACTIVOS ---
    st.subheader("📈 Distribución del Nivel de Riesgo (IRD)")
    st.write("A mayor puntaje en el gráfico, el artículo presenta más indicadores sospechosos (falta de autor, lenguaje alarmista, etc.).")
    
    # Gráfico de barras interactivo usando Streamlit
    st.bar_chart(data=df_articulos, x='titulo', y='puntaje_ird', color='#ff4b4b')

    st.divider()

    # --- SECCIÓN 3: TABLA DE DATOS Y FILTROS ---
    st.subheader("🔍 Explorador de Artículos Analizados")
    
    # Filtro por tipo de fuente
    tipo_filtro = st.selectbox("Filtrar por tipo de fuente:", ["Todos", "Oficial", "Blog"])
    
    if tipo_filtro != "Todos":
        df_filtrado = df_articulos[df_articulos['tipo_fuente'] == tipo_filtro]
    else:
        df_filtrado = df_articulos

    # Mostrar la tabla limpia en el dashboard
    st.dataframe(
        df_filtrado[['titulo', 'autor', 'fecha', 'tipo_fuente', 'puntaje_ird', 'url']], 
        use_container_width=True
    )

else:
    st.error("No se encontraron datos en la base de datos. Asegúrate de ejecutar 'database.py' primero.")