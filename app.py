import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configuración profesional de la página web con tema visual
st.set_page_config(page_title="Monitor de Desinformación", layout="wide")

# Estilos CSS personalizados para limpiar bordes y tipografía de la tabla
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; }
    div.stDataFrame div[data-testid="stTable"] { font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Encabezado Premium
st.subheader("🔮 PROYECTO INTEGRADOR")
st.title("📊 Sistema Inteligente de Monitoreo de Desinformación Científica")
st.markdown("Análisis automatizado de señales de riesgo en artículos de salud mediante el modelo matemático **IRD**.")
st.markdown("---")

# Conexión directa a la base de datos unificada
conn = sqlite3.connect("monitor_desinformacion.db")
df = pd.read_sql_query("SELECT * FROM articulos", conn)
conn.close()

total_articulos = len(df)
alertas_criticas = len(df[df['clasificacion'] == "ALTO RIESGO"])
promedio_ird = df['puntaje_ird'].mean() if total_articulos > 0 else 0.0

# 1. COMPONENTE: Tarjetas de KPIs estilizadas en contenedores independientes
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("<p style='color: #888; margin-bottom: 0px;'>📚 Total Analizados</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin-top: 0px;'>{total_articulos} <span style='font-size: 16px; color: #888;'>artículos</span></h2>", unsafe_allow_html=True)
with col2:
    with st.container(border=True):
        st.markdown("<p style='color: #888; margin-bottom: 0px;'>📈 Riesgo Promedio Global</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin-top: 0px; color: #E67E22;'>{promedio_ird:.1f} <span style='font-size: 16px; color: #888;'>pts</span></h2>", unsafe_allow_html=True)
with col3:
    with st.container(border=True):
        st.markdown("<p style='color: #888; margin-bottom: 0px;'>🚨 Alertas Críticas</p>", unsafe_allow_html=True)
        color_alert = "#E74C3C" if alertas_criticas > 0 else "#2ECC71"
        st.markdown(f"<h2 style='margin-top: 0px; color: {color_alert};'>{alertas_criticas} <span style='font-size: 16px; color: #888;'>detectadas</span></h2>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. COMPONENTE: Sección de Gráficos Distribuidos
col_graf1, col_graf2 = st.columns([1.8, 1.2], gap="large")

with col_graf1:
    with st.container(border=True):
        st.markdown("#### 🎯 Índice de Riesgo por Artículo (Métrica IRD)")
        if total_articulos > 0:
            fig_bar = px.bar(
                df, 
                x='titulo', 
                y='puntaje_ird',
                color='clasificacion',
                color_discrete_map={'ALTO RIESGO': '#E74C3C', 'CONFIABLE': '#2ECC71'},
                labels={'titulo': 'Artículo', 'puntaje_ird': 'Puntaje IRD', 'clasificacion': 'Resultado'},
                template="plotly_white"
            )
            fig_bar.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350, showlegend=True)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sin datos.")

with col_graf2:
    with st.container(border=True):
        st.markdown("#### 🍰 Balance Sanitario Global")
        if total_articulos > 0:
            fig_pie = px.pie(
                df, 
                names='clasificacion',
                color='clasificacion',
                color_discrete_map={'ALTO RIESGO': '#E74C3C', 'CONFIABLE': '#2ECC71'},
                hole=0.4
            )
            fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Sin datos.")

st.markdown("<br>", unsafe_allow_html=True)

# 3. COMPONENTE: Tabla de Control Avanzada y Filtro Profesional
with st.container(border=True):
    col_title, col_filter = st.columns([2, 1])
    with col_title:
        st.markdown("#### 🔍 Explorador y Central de Control Relacional")
        st.markdown("<p style='font-size: 13px; color: #777;'>Visualización en tiempo real del almacenamiento estructurado en SQLite</p>", unsafe_allow_html=True)
    with col_filter:
        opciones_fuente = ["Todos los orígenes"] + list(df['tipo_fuente'].unique()) if total_articulos > 0 else ["Todos"]
        filtro_fuente = st.selectbox("", opciones_fuente)

    if total_articulos > 0:
        if filtro_fuente != "Todos los orígenes":
            df_filtrado = df[df['tipo_fuente'] == filtro_fuente]
        else:
            df_filtrado = df.copy()

        # Reordenamos y renombramos columnas para la presentación formal
        df_mostrar = df_filtrado[['titulo', 'autor', 'fecha', 'tipo_fuente', 'frases_alarmistas', 'referencias_cientificas', 'puntaje_ird', 'clasificacion', 'url']].copy()
        df_mostrar.columns = ['Título del Artículo', 'Autor Detectado', 'Fecha Publicación', 'Tipo Fuente', 'Frases Alarmistas 🚨', 'Referencias Científicas 🔬', 'Puntaje IRD', 'Evaluación Final', 'Enlace URL']
        
        # Funciones de estilo semáforo pulidas (tonos pastel suaves)
        def estilo_celda_alerta(val):
            if val == "ALTO RIESGO":
                return 'background-color: #FADBD8; color: #78281F; font-weight: bold; text-align: center;'
            return 'background-color: #D5F5E3; color: #1E8449; font-weight: bold; text-align: center;'

        # Función para resaltar los números en negrita sin alterar el fondo de la celda
        def estilo_puntaje_negrita(val):
            return 'font-weight: bold; text-align: center;'

        # Renderizar la tabla con estilos semáforo en Evaluación y negritas en Puntaje IRD
        styled_df = df_mostrar.style.map(
            estilo_celda_alerta, 
            subset=['Evaluación Final']
        ).map(
            estilo_puntaje_negrita,
            subset=['Puntaje IRD']
        )
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("La base de datos relacional está vacía.")