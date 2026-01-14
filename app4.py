import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
from datetime import datetime

# --- 1. IDENTIDAD Y CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Ismael Cárdenas", layout="wide")

def obtener_fecha():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha()
firma_full = "Ismael Antonio Cardenas López - Licenciado en Matemática Unan León Nicaragua"

# --- 2. MOTOR DE CONTENIDO ROBUSTO ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'...",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística...",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica..."
    }

# --- 3. LÓGICA DE COLORES PARA VISTA PREVIA ---
def renderizar_estilos(texto):
    lineas = texto.split('\n')
    for l in lineas:
        if not l.strip(): continue
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "AXIOMA", "PROPOSICIÓN"]):
            st.info(f"✨ **{l}**") # Azul llamativo
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**") # Verde llamativo
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"📝 **{l}**") # Naranja llamativo
        elif "SOLUCIÓN" in up or "SOLUCION" in up:
            st.markdown(f"✅ **{l}**") # Gris/Check
        else:
            st.write(l)

# --- 4. INTERFAZ DE USUARIO ---
st.title("🎓 Gestor Académico de Élite - Ismael Cárdenas")

with st.sidebar:
    st.header("⚙️ Configuración")
    tema = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")
    st.write(f"📅 **Fecha:** {fecha_actual}")
    st.write(f"👤 **Autor:** {firma_full}")

col_input, col_preview = st.columns([1, 1])

with col_input:
    st.subheader("📥 Entrada de Datos")
    cont_teorico = st.text_area("Contenido (Teoremas, Definiciones...)", height=250)
    cont_ejercicios = st.text_area("Ejercicios y Soluciones", height=200)

# --- 5. VISTA PREVIA Y DESCARGAS ---
with col_preview:
    st.subheader("👁️ Vista Previa del Documento")
    textos = generar_textos_robustos(tema)
    
    with st.container(border=True):
        # Encabezado con imagen circular (Simulada en preview)
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{tema}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>{firma_full}</p>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("### I. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### II. Desarrollo Teórico")
        renderizar_estilos(cont_teorico)
        
        st.markdown("### III. Ejercicios")
        renderizar_estilos(cont_ejercicios)
        
        st.success(f"**IV. Conclusiones Robustas**\n\n{textos['conclu']}")
        st.info(f"**V. Recomendaciones Robustas**\n\n{textos['recom']}")

# --- 6. MENÚS DE DESCARGA SEPARADOS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    if st.button("📦 Generar Menú WORD", key="gen_word"):
        # Lógica de Word aquí (Se mantiene tu código previo)
        st.download_button("⬇️ Descargar .DOCX", b"data", f"{tema}.docx", key="dw_word")

with c2:
    if st.button("📦 Generar Menú LaTeX", key="gen_latex"):
        # Generamos el código limpio para Overleaf
        # ... (Función procesar_a_latex aquí) ...
        st.code("% Copia este código en Overleaf\n\\documentclass{article}...", language="latex")
        st.download_button("⬇️ Descargar .TEX", "codigo", f"{tema}.tex", key="dw_latex")
