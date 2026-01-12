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

st.set_page_config(page_title="Calculo Pro: Formato Académico", layout="wide")

def hacer_circulo(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        ancho, alto = img.size
        min_dim = min(ancho, alto)
        img = img.crop(((ancho - min_dim) // 2, (alto - min_dim) // 2, (ancho + min_dim) // 2, (alto + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        dibujo = ImageDraw.Draw(mascara)
        dibujo.ellipse((0, 0, min_dim, min_dim), fill=255)
        resultado = ImageOps.fit(img, mascara.size, centering=(0.5, 0.5))
        resultado.putalpha(mascara)
        buf = io.BytesIO()
        resultado.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except:
        return None

with st.sidebar:
    st.header("📋 Configuración")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.info("Asegúrate de que 'perfil.jpeg' esté en tu GitHub.")

st.title("🎓 Generador Académico: Word + LaTeX (Premium)")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Reconocimiento de Imagen")
    uploaded_file = st.file_uploader("Sube tu captura", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=300)
        model = LatexOCR()
        latex_res = model(img)
        st.latex(latex_res)

with col2:
    st.header("2. Gráfica Centrada (0,0)")
    func_input = st.text_input("Función matemática:", "np.sin(x)")
    try:
        x = np.linspace(-10, 10, 1000)
        y = eval(func_input.replace('^', '**'), {"x": x, "np": np})
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(x, y, color='blue', linewidth=2)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        buf_graf = io.BytesIO(); fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except:
        st.error("Error en la función.")

st.divider()
if st.button("🚀 Generar Todo con Formato Elegante"):
    # TEXTOS ELEGANTES
    intro = f"El presente estudio, titulado '{titulo}', constituye un análisis riguroso de los principios fundamentales del cálculo. A través de la integración de herramientas de visión computacional para la digitalización de expresiones matemáticas y la representación gráfica de alta precisión, se busca profundizar en el comportamiento asintótico y estructural de las funciones analizadas por {autor}."
    conclu = "Se concluye que la convergencia entre el análisis analítico y la representación visual computarizada permite una comprensión holística de las propiedades de la función. La precisión en la transcripción de caracteres matemáticos y el centrado riguroso de los ejes coordenados son esenciales para una interpretación académica correcta."
    recom = "Se recomienda emplear este marco metodológico para la documentación de procesos de ingeniería y ciencias exactas, asegurando siempre la calibración de los parámetros de visualización para capturar la esencia de las discontinuidades y puntos críticos de las funciones."

    # --- WORD: FOTO SOLO EN PRIMERA HOJA ---
    doc = Document()
    # Usamos secciones para que la foto solo esté en la primera página
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    header = seccion.first_page_header
    p_header = header.paragraphs[0]
    p_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto_circular = hacer_circulo('perfil.jpeg')
    if foto_circular:
        run = p_header.add_run()
        run.add_picture(foto_circular, width=Inches(1.2))
    
    doc.add_heading(titulo, 0)
    p_autor = doc.add_paragraph(f"Por: {autor}")
    p_autor.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Desarrollo Matemático', 1)
    doc.add_paragraph(f"Expresión identificada mediante OCR:").bold = True
    doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(5))
    doc.add_heading('Conclusiones', 1); doc.add_paragraph(conclu)
    doc.add_heading('Recomendaciones', 1); doc.add_paragraph(recom)

    word_io = io.BytesIO(); doc.save(word_io); word_io.seek(0)
    
    # --- LATEX: FOTO SOLO EN PRIMERA HOJA ---
    latex_file = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, tikz}}

\\begin{{document}}

% Foto circular solo en la portada (esquina superior derecha)
\\begin{{tikzpicture}}[remember picture,overlay]
\\node[anchor=north east, xshift=-1cm, yshift=-1.5cm] at (current page.north east) {{
    \\begin{{tikzpicture}}
        \\clip [circle] (0,0) circle (1.5cm);
        \\node at (0,0) {{\\includegraphics[width=3cm]{{perfil.jpeg}}}};
    \\end{{tikzpicture}}
}};
\\end{{tikzpicture}}

\\title{{\\textbf{{{titulo}}}}}
\\author{{{autor}}}
\\date{{\\today}}
\\maketitle

\\section{{Introducción}}
{intro}

\\section{{Análisis y Resultados}}
La expresión matemática analizada se define como:
\\[ {latex_res} \\]

\\section{{Conclusiones}}
{conclu}

\\section{{Recomendaciones}}
{recom}

\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", word_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, f"{titulo}.tex")
