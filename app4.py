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
    st.info("El sistema está optimizado para generar ingresos mediante contenido educativo premium.")

st.title("🎓 Sistema de Producción Científica Avanzada")

# Textos con rigor académico (Preservando tildes)
intro_formal = f"El presente compendio técnico, enfocado en '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del {autor}, este documento articula la abstracción algebraica con la fenomenología visual."
conclu_formal = f"Tras el estudio exhaustivo, se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de las estructuras matemáticas analizadas en '{titulo}'."

# --- INTERFAZ DE ENTRADA ---
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # 1. Área de Texto Libre (Copiar/Pegar)
    texto_libre = st.text_area("✍️ Pegar texto descriptivo o teoría:", "Inserte aquí el cuerpo teórico del ejercicio...")
    
    # 2. OCR Matemático
    file_ocr = st.file_uploader("🔢 Captura de Ecuación (OCR)", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if file_ocr:
        model = LatexOCR()
        latex_res = model(Image.open(file_ocr))
        st.latex(latex_res)

    # 3. Detector de Gráficas (Entrada de función)
    st.markdown("---")
    st.subheader("📈 Representación Gráfica Profesional")
    func_in = st.text_input("Función detectada en captura (ej: x**3 - 2*x):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(-5, 5, 400)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, color='#1f77b4', lw=2)
        ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    # 4. Galería de Capturas
    imgs_subidas = st.file_uploader("🖼️ Subir capturas de apoyo (Ejercicios/Gráficas)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = [io.BytesIO(f.getvalue()) for f in imgs_subidas] if imgs_subidas else []

with col_pre:
    st.subheader("👁️ Vista Previa de Alta Gama")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {intro_formal}")
        st.write(f"**Teoría:** {texto_libre}")
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf, caption="Gráfica Vectorizada")
        if latex_res: st.latex(latex_res)

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
    doc.add_paragraph(intro_formal)
    doc.add_heading('Desarrollo Teórico', 1); doc.add_paragraph(texto_libre)
    doc.add_heading('Análisis Simbólico', 1); doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(4.5))
    doc.add_heading('Anexos Visuales', 1)
    for b in list_img_buf: doc.add_picture(b, width=Inches(3))
    doc.add_heading('Conclusiones', 1); doc.add_paragraph(conclu_formal)
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX PROFESIONAL (PGFPLOTS) ---
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, pgfplots}}
\\pgfplotsset{{compat=1.18}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} \\author{{{autor}}} \\maketitle
\\section{{Introducción}} {intro_formal}
\\section{{Cuerpo Teórico}} {texto_libre}
\\section{{Análisis Matemático}} $ {latex_res} $
\\section{{Representación Gráfica}}
\\begin{{center}}
\\begin{{tikzpicture}}
\\begin{{axis}}[axis lines=middle, grid=major, xlabel=$x$, ylabel=$y$, title={{Gráfica de $f(x) = {func_in}$}}]
\\addplot[color=blue, thick, samples=100] {{{func_in.replace('np.', '')}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{center}}
\\section{{Conclusiones}} {conclu_formal}
\\end{{document}}"""

    st.download_button("⬇️ Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ LaTeX Profesional", latex_str, f"{titulo}.tex")
