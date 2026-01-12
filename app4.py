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

st.set_page_config(page_title="Calculo Pro: Generador Universal", layout="wide")

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

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    autor_predeterminado = "Ismael Antonio Cárdenas, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    autor = st.text_input("Autor del Proyecto", autor_predeterminado)
    st.info("Sube 'perfil.jpeg' a tu GitHub.")

st.title("🎓 Sistema Educativo: Generación de Guías Premium")

# --- SECCIÓN PRINCIPAL: OCR Y GRÁFICA ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Ejercicio Resuelto (OCR)")
    uploaded_file = st.file_uploader("Sube el ejercicio resuelto", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=300)
        model = LatexOCR()
        latex_res = model(img)
        st.latex(latex_res)

with col2:
    st.header("2. Visualización Matemática")
    func_input = st.text_input("Función para la gráfica:", "np.cos(x)")
    try:
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = eval(func_input.replace('^', '**'), {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(x_vals, y_vals, color='blue', linewidth=2)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig)
        buf_graf = io.BytesIO(); fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except:
        st.error("Error en la función.")

# --- SECCIÓN: EJERCICIOS PROPUESTOS ---
st.divider()
st.header("📝 3. Sección de Ejercicios Propuestos")
col_text, col_img = st.columns(2)

with col_text:
    texto_ejercicios = st.text_area("Escribe los enunciados de los ejercicios (uno por línea):", 
                                    "1. Calcule la derivada de la función anterior.\n2. Determine los puntos críticos.\n3. Evalúe el límite cuando x tiende a cero.")

with col_img:
    img_ejercicios = st.file_uploader("O sube capturas de ejercicios propuestos", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = []
    if img_ejercicios:
        for file in img_ejercicios:
            img_p = Image.open(file)
            st.image(img_p, width=200)
            b = io.BytesIO(); img_p.save(b, format="PNG"); b.seek(0)
            list_img_buf.append(b)

# --- BOTÓN DE GENERACIÓN ---
if st.button("🚀 Generar Material Educativo Completo"):
    # LÓGICA DE TEXTOS AUTOMATIZADOS Y ELEGANTES
    intro = f"El presente compendio académico, titulado '{titulo}', representa una síntesis técnica y pedagógica diseñada rigurosamente por el {autor}. En este documento se explora la intersección entre la teoría abstracta y la representación computacional, proporcionando al estudiante un marco conceptual sólido para el dominio del tema en cuestión."
    conclu = f"Tras el análisis exhaustivo de '{titulo}', se concluye que la integración de herramientas de visualización dinámica y digitalización de sintaxis matemática no solo optimiza el tiempo de estudio, sino que refuerza la intuición geométrica necesaria para la resolución de problemas complejos en el ámbito de las ciencias exactas."
    recom = f"Para un aprovechamiento integral de esta guía de '{titulo}', se recomienda al lector realizar un contraste analítico entre los resultados obtenidos manualmente y las gráficas generadas. Asimismo, se insta a abordar los ejercicios propuestos como un desafío intelectual para consolidar el pensamiento lógico-matemático."

    # --- WORD ---
    doc = Document()
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    header = seccion.first_page_header
    p_h = header.paragraphs[0]; p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ: p_h.add_run().add_picture(f_circ, width=Inches(1.2))
    
    doc.add_heading(titulo, 0)
    p_aut = doc.add_paragraph(f"Elaborado por: {autor}")
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Ejercicio de Aplicación', 1)
    doc.add_paragraph(f"Modelado Matemático (OCR):").bold = True
    doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(5))
    
    doc.add_heading('Ejercicios de Consolidación', 1)
    doc.add_paragraph(texto_ejercicios)
    for b_img in list_img_buf:
        doc.add_picture(b_img, width=Inches(4))
    
    doc.add_heading('Conclusiones Académicas', 1); doc.add_paragraph(conclu)
    doc.add_heading('Recomendaciones de Estudio', 1); doc.add_paragraph(recom)
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX ---
    latex_file = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[remember picture,overlay]
\\node[anchor=north east, xshift=-1cm, yshift=-1.5cm] at (current page.north east) {{
    \\begin{{tikzpicture}} \\clip [circle] (0,0) circle (1.5cm); \\node at (0,0) {{\\includegraphics[width=3cm]{{perfil.jpeg}}}}; \\end{{tikzpicture}}
}};
\\end{{tikzpicture}}
\\title{{\\textbf{{{titulo}}}}} \\author{{Elaborado por: \\\\ {autor}}} \\date{{\\today}} \\maketitle
\\section{{Introducción}} {intro}
\\section{{Desarrollo Técnico}} \\noindent Expresión analizada: \\\\ \\centering $ {latex_res} $ \\\\
\\section{{Ejercicios Propuestos}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {conclu}
\\section{{Recomendaciones}} {recom}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, f"{titulo}.tex")
