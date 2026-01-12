import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io

# Configuración inicial para evitar errores de renderizado
st.set_page_config(page_title="Generador Académico", layout="centered")

st.title("🎓 Sistema de Proyectos de Cálculo")
st.markdown("Genera documentos Word y LaTeX con IA y gráficas.")

# --- DATOS DEL PROYECTO ---
with st.sidebar:
    st.header("Configuración")
    titulo = st.text_input("Título del Proyecto", "Análisis Matemático")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.info("Sube 'perfil.png' a tu GitHub para que aparezca tu foto.")

# --- PROCESAMIENTO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Imagen a LaTeX")
    uploaded_file = st.file_uploader("Sube tu fórmula", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=250)
        with st.spinner("Leyendo..."):
            model = LatexOCR()
            latex_res = model(img)
        st.latex(latex_res)

with col2:
    st.subheader("2. Gráfica")
    func_input = st.text_input("Función (ej: x**2)", "x**2")
    x = np.linspace(-10, 10, 100)
    try:
        y = eval(func_input.replace('^', '**'))
        fig, ax = plt.subplots(figsize=(5,3))
        ax.plot(x, y, color='red')
        ax.grid(True)
        st.pyplot(fig)
        
        # Buffer para imágenes
        buf_graf = io.BytesIO()
        fig.savefig(buf_graf, format='png')
        buf_graf.seek(0)
    except:
        st.error("Revisa la función")

# --- GENERADOR DE ARCHIVOS ---
if st.button("🚀 Generar Todo (Word y LaTeX)"):
    # Lógica de textos automáticos
    intro = f"Este trabajo presenta un análisis sobre {titulo}, elaborado por {autor}."
    conclu = "Se concluye que el uso de IA facilita la transcripción de fórmulas complejas."
    recom = "Se recomienda verificar los resultados gráficos con métodos analíticos."

    # CREAR WORD
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {autor}")
    try:
        doc.add_picture('perfil.png', width=Inches(1.5))
    except:
        pass
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Fórmula', 1); doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(4))
    doc.add_heading('Conclusión', 1); doc.add_paragraph(conclu)
    doc.add_heading('Recomendación', 1); doc.add_paragraph(recom)

    word_io = io.BytesIO()
    doc.save(word_io)
    word_io.seek(0)
    
    # CREAR LATEX
    latex_file = f"\\documentclass{{article}}\n\\title{{{titulo}}}\n\\author{{{autor}}}\n\\begin{{document}}\n\\maketitle\n\\section{{Intro}}\n{intro}\n\\section{{Formula}}\n${latex_res}$\n\\end{{document}}"

    st.download_button("⬇️ Descargar Word", word_io, "proyecto.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, "proyecto.tex")
