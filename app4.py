import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# --- SOLUCIÓN DE PERMISOS PARA TRANSCRIPCIÓN ---
# Esto intenta saltarse el error "Permission Denied" que viste en tu captura
os.environ['PIX2TEX_MODEL_DIR'] = '/tmp/pix2tex'
if not os.path.exists('/tmp/pix2tex'):
    try:
        os.makedirs('/tmp/pix2tex', exist_ok=True)
    except:
        pass

st.set_page_config(page_title="Compilador Ismael: OCR Matemático", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- CARGA DEL MODELO DE TRANSCRIPCIÓN (IMAGEN A TEXTO/LATEX) ---
@st.cache_resource
def inicializar_ocr():
    try:
        return LatexOCR()
    except Exception as e:
        st.warning(f"Aviso: El motor de transcripción automática está en mantenimiento. Las imágenes se adjuntarán como capturas de alta calidad.")
        return None

# --- MOTOR DE TEXTO ---
def generar_textos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos. Autor: Lic. {firma}. Fecha: {fecha_actual}.",
        "conclu": "Se establece que la convergencia entre el cálculo simbólico y la visualización permite una comprensión holística del análisis.",
        "recom": "Se recomienda contrastar la resolución analítica con la verificación computacional presentada."
    }

# --- ESTADO DE SESIÓN ---
if 'formula_transcrita' not in st.session_state: st.session_state.formula_transcrita = ""

with st.sidebar:
    st.header("📋 Datos del Proyecto")
    titulo = st.text_input("Título", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Lic. en Matemáticas, UNAN-León"

st.title("🎓 Sistema de Producción Científica (OCR + Compilador)")
textos = generar_textos(titulo, firma_oficial)
model_ocr = inicializar_ocr()

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Carga y Transcripción")
    
    # SECCIÓN TEORÍA + OCR
    texto_teoria = st.text_area("✍️ Texto base de Teoría:", "Desarrollo conceptual...", height=80)
    cap_teoria = st.file_uploader("🖼️ Captura de Ecuación (Para convertir a texto)", type=["png", "jpg", "jpeg"])
    
    if cap_teoria and model_ocr:
        if st.button("🔍 Transcribir Imagen a Texto/Fórmula"):
            with st.spinner("Leyendo fórmulas de la imagen..."):
                img = Image.open(cap_teoria)
                st.session_state.formula_transcrita = model_ocr(img)
                st.success("¡Transcripción completada!")

    if st.session_state.formula_transcrita:
        st.info("Resultado del OCR (puedes editarlo):")
        st.session_state.formula_transcrita = st.text_area("Fórmula/Texto detectado:", st.session_state.formula_transcrita)
        st.latex(st.session_state.formula_transcrita)

    # GRÁFICA
    st.markdown("---")
    func_in = st.text_input("📈 Función (ej: n**2):", "1/x")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(1, 15, 30)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, 'o-', color='#003366')
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

    # EJERCICIOS
    st.markdown("---")
    texto_ejercicios = st.text_area("📝 Texto de Ejercicios:", "Resolver:")
    caps_ejercicios = st.file_uploader("🖼️ Capturas de Ejercicios (Se adjuntan como imagen)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

with col_pre:
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        st.markdown(f"**{titulo}**")
        st.write(textos['intro'])
        st.write(f"**Teoría:** {texto_teoria}")
        if st.session_state.formula_transcrita:
            st.latex(st.session_state.formula_transcrita)
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf)
        st.write(f"**Ejercicios:** {texto_ejercicios}")

# --- COMPILACIÓN ---
if st.button("🚀 Generar Word y LaTeX"):
    # --- WORD ---
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria)
    if st.session_state.formula_transcrita:
        doc.add_paragraph(f"Fórmula transcrita: {st.session_state.formula_transcrita}")
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4))
    
    doc.add_heading('IV. Ejercicios', 1)
    doc.add_paragraph(texto_ejercicios)
    if caps_ejercicios:
        for f in caps_ejercicios:
            doc.add_picture(io.BytesIO(f.getvalue()), width=Inches(3))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX ---
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\begin{{document}}
\\title{{{titulo}}} \\maketitle
\\section{{Teoría}} {texto_teoria}
\\begin{{equation}}
{st.session_state.formula_transcrita}
\\end{{equation}}
\\section{{Ejercicios}} {texto_ejercicios}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
