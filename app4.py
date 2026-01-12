import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración de entorno y permisos
os.environ['PIX2TEX_MODEL_DIR'] = '/tmp/pix2tex'

st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")

# Estilo CSS para simular una hoja de papel (PDF/Latex View)
st.markdown("""
    <style>
    .document-page {
        background-color: white;
        color: black;
        padding: 50px;
        margin: auto;
        width: 100%;
        min-height: 800px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-family: 'Times New Roman', Times, serif;
        border: 1px solid #ddd;
    }
    .latex-header { text-align: right; font-size: 12px; }
    .latex-title { text-align: center; font-weight: bold; font-size: 24px; margin-top: 20px; }
    .latex-author { text-align: center; font-size: 16px; margin-bottom: 30px; }
    .latex-section { font-weight: bold; font-size: 18px; margin-top: 20px; border-bottom: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO ---
def generar_textos_robustos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual, garantizando un rigor deductivo en la transición de los modelos teóricos a la representación digital a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos funcionales. La integración técnica presentada eleva los estándares del análisis pedagógico en la UNAN-León, consolidando la abstracción como base del pensamiento lógico-formal.",
        "recom": f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada en este análisis de '{titulo}'. Se recomienda la exploración de casos límite y el rigor en la práctica de los ejercicios propuestos para la consolidación del pensamiento matemático avanzado en Nicaragua."
    }

@st.cache_resource
def cargar_modelo_ocr():
    try: return LatexOCR()
    except: return None

def hacer_circulo(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        min_dim = min(img.size)
        img = img.crop(((img.width - min_dim) // 2, (img.height - min_dim) // 2, (img.width + min_dim) // 2, (img.height + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        ImageDraw.Draw(mascara).ellipse((0, 0, min_dim, min_dim), fill=255)
        img.putalpha(mascara)
        buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
        return buf
    except: return None

# --- ESTADO DE SESIÓN ---
if 'latex_transcrito' not in st.session_state: st.session_state.latex_transcrito = ""

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    st.write(f"📅 **Fecha:** {fecha_actual}")

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_robustos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    texto_teoria = st.text_area("✍️ Teoría:", "Inserte el fundamento teórico aquí...", height=150)
    
    file_ocr = st.file_uploader("🔢 Captura de Ecuación (OCR)", type=["png", "jpg", "jpeg"])
    if file_ocr:
        model = cargar_modelo_ocr()
        if model:
            with st.spinner("Transcribiendo..."):
                st.session_state.latex_transcrito = model(Image.open(file_ocr))
            st.latex(st.session_state.latex_transcrito)

    func_in = st.text_input("📈 Función/Sucesión:", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(1, 10, 20)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter(x_v, y_v, color='#003366')
        ax.grid(True, linestyle=':', alpha=0.6)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    texto_ejercicios = st.text_area("📝 Ejercicios:", "1. Analice...", height=100)

with col_pre:
    st.subheader("👁️ Vista Previa Realista (Estilo LaTeX/PDF)")
    # --- CONTENEDOR DE HOJA TIPO PDF ---
    st.markdown(f"""
    <div class="document-page">
        <div class="latex-header">
            <b>{firma_oficial}</b><br>{fecha_actual}
        </div>
        <div class="latex-title">{titulo.upper()}</div>
        <div class="latex-author">Autor: {firma_oficial}</div>
        
        <div class="latex-section">I. Introducción</div>
        <p>{textos['intro']}</p>
        
        <div class="latex-section">II. Fundamentación Teórica</div>
        <p>{texto_teoria}</p>
        
        <div class="latex-section">III. Desarrollo Analítico</div>
        <p>A continuación se presenta la transcripción de la captura procesada:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Renderizado de elementos vivos dentro de la vista previa
    if st.session_state.latex_transcrito:
        st.latex(st.session_state.latex_transcrito)
    
    if buf_graf.getbuffer().nbytes > 0:
        st.image(buf_graf, caption="Representación Gráfica del Modelo")

    st.markdown(f"""
    <div class="document-page" style="margin-top:-50px; box-shadow:none; border-top:none;">
        <div class="latex-section">IV. Ejercicios Propuestos</div>
        <p>{texto_ejercicios}</p>
        <div class="latex-section">V. Conclusiones</div>
        <p>{textos['conclu']}</p>
        <div class="latex-section">VI. Recomendaciones</div>
        <p>{textos['recom']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- BOTONES DE DESCARGA ---
if st.button("🚀 Finalizar y Compilar"):
    # Lógica de Word
    doc = Document()
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ:
        header = seccion.first_page_header
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run().add_picture(f_circ, width=Inches(1.1))
    
    doc.add_heading(titulo, 0)
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Teoría', 1); doc.add_paragraph(texto_teoria)
    if st.session_state.latex_transcrito:
        doc.add_heading('III. Análisis Analítico', 1); doc.add_paragraph(st.session_state.latex_transcrito)
    if buf_graf.getbuffer().nbytes > 0: doc.add_picture(buf_graf, width=Inches(4.5))
    doc.add_heading('IV. Ejercicios', 1); doc.add_paragraph(texto_ejercicios)
    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # Lógica LaTeX
    latex_str = f"\\documentclass{{article}}\\usepackage[utf8]{{inputenc}}\\usepackage{{amsmath,amssymb,graphicx}}\\begin{{document}}\\title{{{titulo}}}\\author{{{firma_oficial}}}\\maketitle\\section{{Introducción}}{textos['intro']}\\section{{Teoría}}{texto_teoria}\\section{{Análisis}}$${st.session_state.latex_transcrito}$$\\section{{Ejercicios}}{texto_ejercicios}\\section{{Conclusiones}}{textos['conclu']}\\section{{Recomendaciones}}{textos['recom']}\\end{{document}}"

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
