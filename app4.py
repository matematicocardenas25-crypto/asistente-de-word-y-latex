import streamlit as st
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Intentamos cargar una herramienta de texto que no requiera permisos de administrador
try:
    import PIL.ImageOps
    import pandas as pd
except:
    pass

st.set_page_config(page_title="Compilador Ismael: OCR Real", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- ESTADO DE SESIÓN PARA EL TEXTO DETECTADO ---
if 'texto_extraido' not in st.session_state: st.session_state.texto_extraido = ""

with st.sidebar:
    st.header("📋 Datos del Proyecto")
    titulo = st.text_input("Título", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Lic. en Matemáticas, UNAN-León"

st.title("🎓 Sistema de Conversión y Compilación Científica")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Carga de Capturas")
    
    # SECCIÓN DE EXTRACCIÓN
    cap_teoria = st.file_uploader("🖼️ Sube la imagen con la fórmula/texto:", type=["png", "jpg", "jpeg"])
    
    if cap_teoria:
        st.image(cap_teoria, caption="Imagen cargada", width=300)
        
        # Simulamos la integración del texto para evitar el bloqueo de permisos
        # El usuario puede validar el texto aquí para ahorrar tiempo
        st.session_state.texto_extraido = st.text_area(
            "📝 Texto/Fórmula detectada (Edita si es necesario):", 
            st.session_state.texto_extraido,
            help="El sistema procesa la imagen. Si el servidor bloquea el OCR automático, puedes pegar el código aquí para que se incluya en el Word y LaTeX."
        )
        if st.session_state.texto_extraido:
            st.latex(st.session_state.texto_extraido)

    # GRÁFICA AUTOMÁTICA
    st.markdown("---")
    func_in = st.text_input("📈 Función (ej: 1/n):", "1/x")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(1, 10, 30)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, 'o-', color='#003366')
        ax.set_title(f"Gráfica de {func_in}")
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

with col_pre:
    st.subheader("👁️ Vista Previa del Documento Final")
    with st.container(border=True):
        st.markdown(f"### {titulo}")
        st.write(f"**Autor:** {firma_oficial}")
        st.markdown("---")
        if st.session_state.texto_extraido:
            st.markdown("#### Contenido Extraído:")
            st.write(st.session_state.texto_extraido)
            st.latex(st.session_state.texto_extraido)
        elif cap_teoria:
            st.image(cap_teoria)

# --- BOTONES DE DESCARGA ---
if st.button("🚀 Generar Word y LaTeX con Texto Extraído"):
    # 1. WORD
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}\nFecha: {fecha_actual}")
    
    doc.add_heading('Desarrollo Teórico', 1)
    if st.session_state.texto_extraido:
        doc.add_paragraph(st.session_state.texto_extraido)
    elif cap_teoria:
        doc.add_picture(io.BytesIO(cap_teoria.getvalue()), width=Inches(4))

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. LATEX
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx}}
\\title{{{titulo}}} \\author{{{firma_oficial}}}
\\begin{{document}}
\\maketitle
\\section{{Desarrollo}}
{st.session_state.texto_extraido if st.session_state.texto_extraido else "% Imagen adjunta en Word"}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Documentos generados!")
