import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io

# Configuración de página
st.set_page_config(page_title="Generador Académico Pro", layout="wide")

st.title("🎓 Sistema Automatizado de Proyectos de Cálculo")
st.markdown("Generación de documentos Word y LaTeX con IA.")

# --- DATOS DEL AUTOR ---
with st.sidebar:
    st.header("👤 Información del Autor")
    nombre_proyecto = st.text_input("Título del Proyecto", "Análisis de Funciones Complejas")
    autor = st.text_input("Nombre Completo", "Tu Nombre Aquí")
    fecha = st.date_input("Fecha de Entrega")

# --- PROCESAMIENTO DE IMAGEN (OCR) ---
st.header("1. Captura y Reconocimiento de Fórmulas")
archivo_imagen = st.file_uploader("Sube la foto del libro o ejercicio", type=["png", "jpg", "jpeg"])

latex_extraido = ""
if archivo_imagen:
    img = Image.open(archivo_imagen)
    st.image(img, caption="Imagen cargada", width=400)
    with st.spinner("IA analizando fórmula..."):
        modelo = LatexOCR()
        latex_extraido = modelo(img)
    st.success("Fórmula detectada:")
    st.latex(latex_extraido)

# --- GENERACIÓN DE GRÁFICA ---
st.header("2. Visualización Matemática")
funcion_str = st.text_input("Escribe la función para la gráfica (ej: x**3 - 2*x)", "x**2")

fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(-10, 10, 500)
try:
    y = eval(funcion_str.replace('^', '**'))
    ax.plot(x, y, label=f"f(x) = {funcion_str}", color='darkorange', linewidth=2)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.grid(True, linestyle='--')
    ax.legend()
    st.pyplot(fig)
    
    # Guardar gráfica para los archivos
    buf_grafica = io.BytesIO()
    fig.savefig(buf_grafica, format='png')
    buf_grafica.seek(0)
except:
    st.error("Error en la sintaxis de la función.")

# --- GENERACIÓN DE TEXTOS AUTOMÁTICOS ---
introduccion = f"El presente trabajo académico titulado '{nombre_proyecto}' ha sido elaborado por {autor}. Se centra en la digitalización de expresiones matemáticas y el análisis gráfico computacional para fortalecer el aprendizaje del cálculo."
conclusiones = "Se concluye que la integración de herramientas de OCR permite una transición eficiente entre el material impreso y el digital, reduciendo errores de transcripción en fórmulas complejas."
recomendaciones = "Se recomienda el uso de este sistema para la creación de portafolios digitales, asegurando que las gráficas mantengan una escala adecuada para la interpretación de límites y derivadas."

# --- BOTONES DE DESCARGA ---
st.header("3. Exportar Documentos")
col_word, col_latex = st.columns(2)

# --- LÓGICA WORD ---
with col_word:
    if st.button("📝 Generar Word"):
        doc = Document()
        doc.add_heading(nombre_proyecto, 0)
        doc.add_paragraph(f"Autor: {autor}\nFecha: {fecha}")
        
        # Insertar Foto de Perfil
        try:
            doc.add_picture('perfil.png', width=Inches(1.2))
        except:
            doc.add_paragraph("[Foto de perfil no encontrada en el repositorio]")

        doc.add_heading('Introducción', level=1)
        doc.add_paragraph(introduccion)
        
        doc.add_heading('Desarrollo Matemático', level=1)
        doc.add_paragraph(f"Fórmula identificada: {latex_extraido}")
        doc.add_picture(buf_grafica, width=Inches(5))
        
        doc.add_heading('Conclusiones', level=1)
        doc.add_paragraph(conclusiones)
        
        doc.add_heading('Recomendaciones', level=1)
        doc.add_paragraph(recomendaciones)
        
        buf_word = io.BytesIO()
        doc.save(buf_word)
        buf_word.seek(0)
        
        st.download_button("Descargar .DOCX", buf_word, f"{nombre_proyecto}.docx")

# --- LÓGICA LATEX ---
with col_latex:
    if st.button("⚛️ Generar Código LaTeX"):
        codigo_tex = f"""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath}}

\\title{{{nombre_proyecto}}}
\\author{{{autor}}}
\\date{{{fecha}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{introduccion}

\\section{{Desarrollo}}
La expresión analizada es:
\\begin{{equation}}
{latex_extraido}
\\end{{equation}}

\\section{{Conclusiones}}
{conclusiones}

\\section{{Recomendaciones}}
{recomendaciones}

\\end{{document}}
        """
        st.download_button("Descargar .TEX", codigo_tex, f"{nombre_proyecto}.tex")
