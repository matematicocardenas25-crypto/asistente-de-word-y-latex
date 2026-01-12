import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="Calculo Pro: Generador Universal", layout="wide")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración")
    titulo = st.text_input("Título del Proyecto", "Proyecto de Cálculo General")
    autor = st.text_input("Nombre del Autor", "Tu Nombre")
    st.markdown("---")
    st.write("**Guía de Funciones:**")
    st.write("- **Polinomial:** `x**3 - 2*x + 1` ")
    st.write("- **Trigonométrica:** `np.sin(x)`, `np.cos(x)`")
    st.write("- **Exponencial:** `np.exp(x)`")
    st.write("- **Logarítmica:** `np.log(x)`")
    st.write("- **Hiperbólica:** `np.sinh(x)`, `np.cosh(x)`")

st.title("🎓 Sistema de Proyectos Matemáticos")

col1, col2 = st.columns(2)

# --- 1. IMAGEN A LATEX (Sin cambios) ---
with col1:
    st.header("1. Reconocimiento de Imagen")
    uploaded_file = st.file_uploader("Sube tu captura", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=300)
        with st.spinner("Analizando fórmula..."):
            model = LatexOCR()
            latex_res = model(img)
        st.latex(latex_res)

# --- 2. GRÁFICA PROFESIONAL CENTRADA ---
with col2:
    st.header("2. Gráfica Centrada (0,0)")
    func_input = st.text_input("Escribe la función matemática:", "np.sin(x)")
    
    try:
        x = np.linspace(-10, 10, 1000)
        # Diccionario para permitir funciones de numpy directamente
        y = eval(func_input.replace('^', '**'), {"x": x, "np": np})
        
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.plot(x, y, color='blue', linewidth=2, label=f"f(x) = {func_input}")
        
        # --- AJUSTE DE EJES AL CENTRO (0,0) ---
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')
        
        # Ajustar límites para que se vea bien
        plt.ylim(min(y)-1, max(y)+1) if not np.isinf(y).any() else plt.ylim(-10, 10)
        
        st.pyplot(fig)
        
        buf_graf = io.BytesIO()
        fig.savefig(buf_graf, format='png')
        buf_graf.seek(0)
    except Exception as e:
        st.error(f"Error: {e}. Recuerda usar 'np.' para funciones especiales.")

# --- 3. GENERACIÓN DE DOCUMENTOS ---
st.divider()
if st.button("🚀 Generar Todo (Word y LaTeX)"):
    # Textos automáticos enriquecidos
    intro = f"El presente trabajo, titulado '{titulo}', es una investigación elaborada por {autor}. Se enfoca en la resolución y visualización de funciones complejas."
    conclu = "Se concluye que la representación gráfica con ejes centrados facilita la identificación de raíces, asíntotas y el comportamiento asintótico de las funciones analizadas."
    recom = "Se recomienda el uso de notación NumPy para funciones exponenciales y logarítmicas para garantizar la precisión decimal en los documentos finales."

    # CREAR WORD
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {autor}")
    try:
        doc.add_picture('perfil.png', width=Inches(1.2))
    except:
        pass
    
    doc.add_heading('Introducción', 1); doc.add_paragraph(intro)
    doc.add_heading('Análisis Matemático', 1)
    doc.add_paragraph(f"Fórmula detectada: {latex_res}")
    doc.add_picture(buf_graf, width=Inches(5))
    doc.add_heading('Conclusiones', 1); doc.add_paragraph(conclu)
    doc.add_heading('Recomendaciones', 1); doc.add_paragraph(recom)

    word_io = io.BytesIO()
    doc.save(word_io)
    word_io.seek(0)
    
    # CREAR LATEX
    latex_file = f"\\documentclass{{article}}\n\\usepackage{{amsmath}}\n\\title{{{titulo}}}\n\\author{{{autor}}}\n\\begin{{document}}\n\\maketitle\n{intro}\n\\[ {latex_res} \\]\n{conclu}\n\\end{{document}}"

    st.download_button("⬇️ Descargar Word", word_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, f"{titulo}.tex")
