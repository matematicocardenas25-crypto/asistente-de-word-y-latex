import streamlit as st
from PIL import Image
import pytesseract # Motor de texto
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración de Élite
st.set_page_config(page_title="Calculo Pro: Compilador UNAN-León", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO ACADÉMICO ---
def generar_textos_pro(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": "Tras el estudio exhaustivo, se establece que la convergencia entre el cálculo simbólico y la visualización permite una comprensión holística.",
        "recom": "Se recomienda contrastar la resolución analítica manual con la verificación computacional presentada."
    }

# --- ESTADO DE SESIÓN ---
if 'texto_ocr' not in st.session_state: st.session_state.texto_ocr = ""

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León"

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_pro(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # SECCIÓN I: TEORÍA CON EXTRACCIÓN DE TEXTO
    st.markdown("### I. Desarrollo Teórico")
    texto_teoria_manual = st.text_area("✍️ Texto introductorio:", "Desarrollo conceptual...", height=70)
    
    cap_teoria = st.file_uploader("🔢 Sube la imagen para extraer el texto/fórmulas:", type=["png", "jpg", "jpeg"])
    
    if cap_teoria:
        img = Image.open(cap_teoria)
        st.image(img, caption="Imagen cargada para procesar", width=400)
        
        if st.button("🔍 Extraer Texto de la Imagen"):
            with st.spinner("La IA está leyendo tu captura..."):
                try:
                    # Intento de lectura directa para ahorrar tiempo
                    st.session_state.texto_ocr = pytesseract.image_to_string(img, lang='spa+eng')
                    st.success("¡Texto extraído con éxito!")
                except:
                    st.error("El servidor requiere configuración adicional para OCR automático. Por favor, valida el texto manualmente abajo.")

        st.session_state.texto_ocr = st.text_area("📝 Texto/LaTeX extraído (Edita si es necesario):", 
                                               st.session_state.texto_ocr, height=150)
        if st.session_state.texto_ocr:
            st.info("Vista previa de fórmulas detectadas:")
            st.write(st.session_state.texto_ocr)

    # SECCIÓN II: GRÁFICA HD RECUPERADA
    st.markdown("---")
    st.markdown("### II. Visualización HD")
    func_in = st.text_input("📈 Modelo Matemático (ej: 1/x):", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_v = np.linspace(1, 15, 45)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_v, y_v, 'o-', color='#003366', linewidth=2, label=f'a_n = {func_in}')
        ax.set_title("Análisis Gráfico de la Sucesión", fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

with col_pre:
    st.subheader("👁️ Vista Previa Sincronizada")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {textos['intro']}")
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria_manual)
        if st.session_state.texto_ocr:
            st.markdown(st.session_state.texto_ocr)
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Gráfica de Alta Definición")

# --- GENERACIÓN DE ARCHIVOS ---
if st.button("🚀 Compilar Word y LaTeX"):
    # 1. WORD
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria_manual)
    if st.session_state.texto_ocr:
        doc.add_paragraph(st.session_state.texto_ocr)
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. LATEX
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx}}
\\begin{{document}}
\\title{{{titulo}}} \\author{{{firma_oficial}}} \\maketitle
\\section{{Teoría}}
{texto_teoria_manual}
{st.session_state.texto_ocr}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
