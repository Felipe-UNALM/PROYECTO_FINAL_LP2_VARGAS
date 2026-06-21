import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configuración profesional de la página web
st.set_page_config(page_title="Sistema de Monitoreo de Desinformación", layout="wide")

st.title("📊 Sistema de Monitoreo de Indicadores de Desinformación Científica")
st.markdown("### Prototipo de detección de señales de riesgo en artículos de salud")
st.markdown("---")

# Conexión directa a la base de datos unificada
conn = sqlite3.connect("monitor_desinformacion.db")
df = pd.read_sql_query("SELECT * FROM articulos", conn)
conn.close()

total_articulos = len(df)
alertas_criticas = len(df[df['clasificacion'] == "ALTO RIESGO"])
promedio_ird = df['puntaje_ird'].mean() if total_articulos > 0 else 0.0

# 1. COMPONENTE: Tarjetas de KPIs (Indicadores Clave)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Artículos Analizados", value=total_articulos)
with col2:
    st.metric(label="Índice IRD Promedio Global", value=f"{promedio_ird:.1f} pts")
with col3:
    st.metric(label="Artículos de Alto Riesgo Detectados", value=alertas_criticas, delta="¡Alerta!" if alertas_criticas > 0 else "Estable", delta_color="inverse")

st.markdown("---")

# Distribución de pantallas para los dos gráficos solicitados por Sergio
col_graf1, col_graf2 = st.columns([2, 1])

with col_graf1:
    st.markdown("#### 📈 Distribución del Nivel de Riesgo (IRD)")
    if total_articulos > 0:
        # IMPLEMENTACIÓN: Rojo para alto riesgo y Verde para confiable
        fig_bar = px.bar(
            df, 
            x='titulo', 
            y='puntaje_ird',
            color='clasificacion',
            color_discrete_map={'ALTO RIESGO': '#FF4B4B', 'CONFIABLE': '#00B074'},
            labels={'titulo': 'Artículo', 'puntaje_ird': 'Puntaje IRD', 'clasificacion': 'Evaluación'},
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sin datos para graficar.")

with col_graf2:
    st.markdown("#### 🍰 Porcentaje de Información Confiable")
    if total_articulos > 0:
        # COMPONENTE NUEVO: Gráfico de Torta/Pastel exigido en la guía
        fig_pie = px.pie(
            df, 
            names='clasificacion',
            color='clasificacion',
            color_discrete_map={'ALTO RIESGO': '#FF4B4B', 'CONFIABLE': '#00B074'},
            hole=0.2,
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sin datos para gráfico circular.")

st.markdown("---")

# 2. COMPONENTE: Tabla de Control con Semáforo
st.markdown("#### 🔍 Explorador de Artículos Analizados (Tabla de Control)")

opciones_fuente = ["Todos"] + list(df['tipo_fuente'].unique()) if total_articulos > 0 else ["Todos"]
filtro_fuente = st.selectbox("Filtrar por tipo de fuente:", opciones_fuente)

if total_articulos > 0:
    if filtro_fuente != "Todos":
        df_filtrado = df[df['tipo_fuente'] == filtro_fuente]
    else:
        df_filtrado = df.copy()

    # Columnas organizadas idéntico al libreto de exposición
    df_mostrar = df_filtrado[['titulo', 'autor', 'fecha', 'tipo_fuente', 'frases_alarmistas', 'referencias_cientificas', 'puntaje_ird', 'clasificacion', 'url']]
    
    # IMPLEMENTACIÓN: Efecto Semáforo condicional avanzado
    def estilo_celda_alerta(val):
        color = '#FFD2D2' if val == "ALTO RIESGO" else '#D2F8D2'
        text_color = '#990000' if val == "ALTO RIESGO" else '#006600'
        return f'background-color: {color}; color: {text_color}; font-weight: bold;'

    # Aplica gradiente naranja al puntaje IRD e iluminación roja/verde a la clasificación
    styled_df = df_mostrar.style.background_gradient(
        subset=['puntaje_ird'], 
        cmap='Oranges'
    ).map(
        estilo_celda_alerta, 
        subset=['clasificacion']
    )
    
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("La base de datos relacional está vacía.")