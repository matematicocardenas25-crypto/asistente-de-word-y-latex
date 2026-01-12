import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io

# Configuración profesional
st.set_page_config(page_title="Editor Académico Pro", layout="wide")
st.title("🚀 Generador Automático: Word + LaTeX")

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.header("📋 Datos del Documento")
    titulo = st.text_input("Título del Proyecto", "Estudio de Cálculo Integral")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.info("Asegúrate de tener el archivo 'perfil.png' en tu GitHub para la foto.")

# --- ENTRADA DE DATOS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Escaneo de Imagen")
    foto_libro = st.file_uploader("Sube la fórmula del libro", type=["png", "jpg", "jpeg"])
    latex_resultado = ""
    if foto_libro:
        img = Image.open(foto_libro)
        st.image(img, caption="Imagen detectada", width=300)
        modelo = LatexOCR()
        latex_resultado = modelo(img)
        st.code(latex_resultado, language='latex')

with col2:
    st.subheader("2. Gráfica Automática")
    func_input = st.text_input("Función a graficar (ej: x**2)", "x**2")
    x = np.linspace(-10, 10, 400)
    y = eval(func_input.replace('^', '**'))
    fig, ax = plt.subplots()
    ax.plot(x, y, color='blue', label=f"f(x)={func_input}")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    # Guardar gráfica para los archivos
    buf_graf = io.BytesIO()
    fig.savefig(buf_graf, format='png')
    buf_graf.seek(0)

# --- TEXTOS AUTOMÁTICOS ---
intro = f"Este proyecto, desarrollado por {autor}, presenta un análisis detallado sobre {titulo}, integrando herramientas digitales para la transcripción de fórmulas y visualización matemática avanzada."
conclu = "Se determina que el uso de tecnologías OCR y generación dinámica de gráficas optimiza el tiempo de creación de reportes técnicos y reduce el error humano en la transcripción de datos complejos."
recomen = "Se recomienda ampliar este modelo para incluir cálculo multivariable y asegurar que las capturas de imagen tengan iluminación óptima para mejorar la precisión del reconocimiento de caracteres."

# --- GENERACIÓN DE ARCHIVOS ---
st.divider()
st.header("📥 Descargar Resultados")
c1, c2 = st.columns(2)

# GENERAR WORD
with c1:
    if st.button("📦 Crear Documento Word"):
        doc = Document()
        doc.add_heading(titulo, 0)
        doc.add_paragraph(f"Autor: {autor}")
        
        # Insertar tu foto perfil.png
        try:
            doc.add_picture('perfil.png', width=Inches(1.5))
        except:
            doc.add_paragraph("[Error: No se encontró el archivo perfil.png en GitHub]")

        doc.add_heading('Introducción', level=1)
        doc.add_paragraph(intro)
        
        doc.add_heading('Desarrollo y Gráficas', level=1)
        doc.add_paragraph(f"Fórmula detectada: {latex_resultado}")
        doc.add_picture(buf_graf, width=Inches(5))
        
        doc.add_heading('Conclusiones', level=1)
        doc.add_paragraph(conclu)
        
        doc.add_heading('Recomendaciones', level=1)
        doc.add_paragraph(recomen)
        
        target_word = io.BytesIO()
        doc.save(target_word)
        target_word.seek(0)
        st.download_button("Descargar Word (.docx)", target_word, f"{titulo}.docx")

# GENERAR LATEX
with c2:
    if st.button("⚛️ Crear Código LaTeX"):
        tex_code = f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}

\\title{{{titulo}}}
\\author{{{autor}}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{intro}

\\section{{Análisis Matemático}}
La fórmula procesada es:
\\[ {latex_resultado} \\]

\\section{{Conclusiones}}
{conclu}

\\section{{Recomendaciones}}
{recomen}

\\end{{document}}
        """
        st.download_button("Descargar LaTeX (.tex)", tex_code, f"{titulo}.tex")
