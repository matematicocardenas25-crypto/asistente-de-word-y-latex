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

# --- FUNCIÓN PARA HACER LA FOTO CIRCULAR ---
def hacer_circulo(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        # Hacerla cuadrada
        ancho, alto = img.size
        min_dim = min(ancho, alto)
        img = img.crop(((ancho - min_dim) // 2, (alto - min_dim) // 2, (ancho + min_dim) // 2, (alto + min_dim) // 2))
        
        # Crear máscara circular
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

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración")
    titulo = st.text_input("Título del Proyecto", "Proyecto de Cálculo")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.info("Sube 'perfil.png' a GitHub para activar la foto circular.")

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

# --- GENERACIÓN DE ARCHIVOS ---
st.divider()
if st.button("🚀 Generar Todo con Foto Circular"):
    intro = f"Este proyecto sobre {titulo} ha sido elaborado por {autor}..."
    conclu = "Se concluye que el análisis gráfico y digital optimiza los resultados..."
    recom = "Se recomienda el uso de este formato para presentaciones académicas de alto nivel."

    # --- WORD CON FOTO CIRCULAR A LA DERECHA ---
    doc = Document()
    
    # Encabezado con foto
    header_section = doc.sections[0].header
    p = header_section.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    foto_circular = hacer_circulo('perfil.jpeg')
    if foto_circular:
        run.add_picture(foto_circular, width=Inches(1))
    
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {autor}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Análisis', 1); doc.add_paragraph(f"Fórmula: {latex_res}")
    doc.add_picture(buf_graf, width=Inches(5))
    doc.add_heading('Conclusiones', 1); doc.add_paragraph(conclu)

    word_io = io.BytesIO(); doc.save(word_io); word_io.seek(0)
    
    # --- LATEX CON FOTO CIRCULAR ---
    latex_file = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\usepackage{{tikz}}

\\begin{{document}}

% Foto circular arriba a la derecha
\\begin{{tikzpicture}}[remember picture,overlay]
\\node[anchor=north east, xshift=-1cm, yshift=-1cm] at (current page.north east) {{
    \\begin{{tikzpicture}}
        \\clip [circle] (0,0) circle (1.2cm);
        \\node at (0,0) {{\\includegraphics[width=2.4cm]{{perfil.jpeg}}}};
    \\end{{tikzpicture}}
}};
\\end{{tikzpicture}}

\\title{{{titulo}}}
\\author{{{autor}}}
\\date{{\\today}}
\\maketitle

\\section{{Introducción}}
{intro}

\\section{{Desarrollo}}
\\[ {latex_res} \\]

\\section{{Conclusiones}}
{conclu}

\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", word_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, f"{titulo}.tex")
