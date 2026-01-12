import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io

# Configuración de página para evitar errores de carga
st.set_page_config(page_title="Generador Académico", layout="centered")

st.title("🎓 Sistema de Proyectos: Word + LaTeX")

# --- ENTRADA DE DATOS ---
with st.sidebar:
    st.header("Configuración")
    titulo = st.text_input("Título del Proyecto", "Mi Proyecto de Cálculo")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.info("Sube 'perfil.png' a GitHub para incluir tu foto.")

# --- PROCESAMIENTO ---
uploaded_file = st.file_uploader("Sube la imagen del libro", type=["png", "jpg", "jpeg"])
latex_code = ""

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Imagen cargada", width=300)
    with st.spinner("IA convirtiendo a LaTeX..."):
        model = LatexOCR()
        latex_code = model(img)
    st.latex(latex_code)

# --- GRÁFICA ---
st.subheader("Gráfica Automática")
func_input = st.text_input("Escribe la función (ej: x**2)", "x**2")
x = np.linspace(-10, 10, 100)
try:
    y = eval(func_input.replace('^', '**'))
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, y, color='blue', label=f"f(x)={func_input}")
    ax.grid(True)
    st.pyplot(fig)
    
    # Guardar gráfica para los archivos
    buf_grafica = io.BytesIO()
    fig.savefig(buf_grafica, format='png')
    buf_grafica.seek(0)
except:
    st.error("Error en la función matemática.")

# --- GENERAR DOCUMENTOS ---
if st.button("🚀 Preparar Descargas (Word y LaTeX)"):
    # Textos automáticos
    intro = f"Este documento sobre {titulo} ha sido generado por {autor}. Integra OCR y gráficas."
    conclu = "Se concluye que la automatización mejora la precisión en documentos técnicos."
    recom = "Se recomienda revisar la sintaxis de las funciones antes de exportar."

    # 1. GENERAR WORD
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {autor}")
    try:
        doc.add_picture('perfil.png', width=Inches(1.5))
    except:
        pass # Si no hay foto, sigue adelante
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Fórmula y Gráfica', 1)
    doc.add_paragraph(f"Fórmula: {latex_code}")
    doc.add_picture(buf_grafica, width=Inches(5))
    doc.add_heading('Conclusiones', 1); doc.add_paragraph(conclu)
    doc.add_heading('Recomendaciones', 1); doc.add_paragraph(recom)

    word_buf = io.BytesIO()
    doc.save(word_buf)
    word_buf.seek(0)

    # 2. GENERAR LATEX
    latex_content = f"\\documentclass{{article}}\n\\title{{{titulo}}}\n\\author{{{autor}}}\n\\begin{{document}}\n\\maketitle\n\\section{{Introducción}}\n{intro}\n\\section{{Fórmula}}\n${latex_code}$\n\\end{{document}}"

    # Botones de descarga
    st.download_button("⬇️ Descargar Word (.docx)", word_buf, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX (.tex)", latex_content, f"{titulo}.tex")
