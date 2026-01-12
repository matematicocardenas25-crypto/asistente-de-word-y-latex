import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")

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
    except: return None

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    autor = st.text_input("Autor", "Ismael Antonio Cárdenas, Lic. en Matemáticas, UNAN-León")
    st.info("Sistema diseñado para la producción de contenidos educativos de alta rentabilidad.")

st.title("🎓 Sistema de Producción Científica Avanzada")

# --- LÓGICA DE TEXTOS CIENTÍFICOS (Automatización Elegante) ---
intro_formal = f"El presente compendio técnico, enfocado en '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del {autor}, este documento articula la abstracción algebraica con la fenomenología visual, garantizando un rigor deductivo en la transición de la abstracción analítica a la representación digital."
conclu_formal = f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los puntos críticos y el comportamiento de las funciones. Esta integración técnica eleva la calidad del análisis pedagógico contemporáneo."
recom_formal = f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada en este análisis de '{titulo}'. Para optimizar el aprendizaje, se recomienda un contraste dialéctico entre los algoritmos computacionales y los métodos de demostración clásica."

# --- INTERFAZ DE ENTRADA ---
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # 1. Cuerpo Teórico
    texto_teoria = st.text_area("✍️ Texto para Teoría (Copiar/Pegar):", "Inserte aquí el fundamento teórico o descripción del tema...")
    
    # 2. OCR Matemático
    file_ocr = st.file_uploader("🔢 Captura de Ejercicio Resuelto (OCR)", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if file_ocr:
        model = LatexOCR()
        latex_res = model(Image.open(file_ocr))
        st.latex(latex_res)

    # 3. Gráfica Vectorizada
    st.markdown("---")
    st.subheader("📈 Gráfica Profesional")
    func_in = st.text_input("Función detectada (ej: np.cos(x)):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(-7, 7, 500)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, color='#1f77b4', lw=2)
        ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
        ax.grid(True, linestyle='--', alpha=0.6)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    # 4. Sección de Ejercicios Propuestos (NUEVA MEJORA)
    st.markdown("---")
    st.subheader("📝 Sección de Ejercicios")
    texto_ejercicios = st.text_area("✍️ Enunciados de Ejercicios (Copiar/Pegar):", "1. Calcule la derivada... \n2. Encuentre el área...")
    imgs_ejercicios = st.file_uploader("🖼️ Capturas de Ejercicios/Apoyo", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = [io.BytesIO(f.getvalue()) for f in imgs_ejercicios] if imgs_ejercicios else []

with col_pre:
    st.subheader("👁️ Vista Previa de Alta Gama")
    with st.container(border=True):
        st.markdown(f"<p style='text-align:right;'><b>{autor}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {intro_formal[:150]}...")
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf, caption="Gráfica Vectorizada")
        if latex_res: st.latex(latex_res)
        st.markdown("---")
        st.write(f"**Propuestos:** {texto_ejercicios}")

# --- COMPILACIÓN FINAL ---
if st.button("🚀 Compilar Documentos Profesionales"):
    # --- WORD ---
    doc = Document()
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ:
        header = doc.sections[0].first_page_header
        header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        header.paragraphs[0].add_run().add_picture(f_circ, width=Inches(1.1))
    
    doc.add_heading(titulo, 0)
    doc.add_heading('Introducción Formal', 1); doc.add_paragraph(intro_formal)
    doc.add_heading('Desarrollo Teórico', 1); doc.add_paragraph(texto_teoria)
    doc.add_heading('Análisis Simbólico', 1); doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('Ejercicios de Consolidación', 1)
    doc.add_paragraph(texto_ejercicios)
    for b in list_img_buf: doc.add_picture(b, width=Inches(3.5))
    
    doc.add_heading('Conclusiones Académicas', 1); doc.add_paragraph(conclu_formal)
    doc.add_heading('Recomendaciones Metodológicas', 1); doc.add_paragraph(recom_formal)
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX PROFESIONAL ---
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, pgfplots, amssymb}}
\\pgfplotsset{{compat=1.18}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} \\author{{{autor}}} \\maketitle
\\section{{Introducción Formal}} {intro_formal}
\\section{{Fundamentación Teórica}} {texto_teoria}
\\section{{Análisis Técnico}} $ {latex_res} $
\\section{{Representación Gráfica}}
\\begin{{center}}
\\begin{{tikzpicture}}
\\begin{{axis}}[axis lines=middle, grid=major, xlabel=$x$, ylabel=$y$]
\\addplot[color=blue, thick, samples=100] {{{func_in.replace('np.', '')}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{center}}
\\section{{Consolidación Práctica}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {conclu_formal}
\\section{{Recomendaciones}} {recom_formal}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX Científico", latex_str, f"{titulo}.tex")
    st.success("¡Documentos de alta calidad generados!")
