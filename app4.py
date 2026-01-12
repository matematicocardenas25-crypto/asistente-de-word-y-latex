import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import re

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

def detectar_bibliografia(texto):
    # Base de datos de referencias APA 7ma Edición
    db = {
        "stewart": "Stewart, J. (2020). Cálculo de una variable: Trascendentes tempranas (9na ed.). Cengage Learning.",
        "larson": "Larson, R., & Edwards, B. H. (2022). Cálculo (12va ed.). Cengage Learning.",
        "leithold": "Leithold, L. (1998). El Cálculo (7ma ed.). Oxford University Press.",
        "spivak": "Spivak, M. (2018). Cálculo Infinitesimal (4ta ed.). Reverté.",
        "apostol": "Apostol, T. M. (2002). Calculus (Vol. 1). Reverté."
    }
    encontradas = [v for k, v in db.items() if k in texto.lower()]
    if not encontradas:
        encontradas = ["Recurso educativo original desarrollado bajo rigor académico, UNAN-León (2026)."]
    return encontradas

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración de Élite")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    st.info(f"Autor: {firma_oficial}")

st.title("🎓 Sistema Superior de Producción Científica")

# --- TEXTOS CIENTÍFICOS ROBUSTOS ---
intro_formal = f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma_oficial}, este documento articula la abstracción algebraica con la fenomenología visual, garantizando la precisión en la modelación matemática."
conclu_formal = f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos asintóticos. La integración técnica presentada eleva los estándares del análisis pedagógico en Nicaragua."
recom_formal = f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica y la verificación computacional. El rigor en la práctica de los ejercicios propuestos es imperativo para la consolidación del pensamiento lógico-matemático avanzado."

# --- INTERFAZ ---
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Carga de Material")
    texto_teoria = st.text_area("✍️ Fundamentación Teórica (Copiar/Pegar):", "Inserte aquí el desarrollo conceptual...")
    
    file_ocr = st.file_uploader("🔢 Captura de Ejercicio (OCR)", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if file_ocr:
        model = LatexOCR()
        latex_res = model(Image.open(file_ocr))
        st.latex(latex_res)

    st.markdown("---")
    func_in = st.text_input("📈 Función detectada en captura (ej: x**3):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(-10, 10, 500)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, color='#003366', lw=2)
        ax.axhline(0, color='black', lw=0.8); ax.axvline(0, color='black', lw=0.8)
        ax.grid(True, linestyle=':', alpha=0.6)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    st.subheader("📝 Sección de Ejercicios")
    texto_ejercicios = st.text_area("✍️ Enunciados (Copiar/Pegar):", "1. Calcule el límite...")
    imgs_ejercicios = st.file_uploader("🖼️ Capturas de Apoyo", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = [io.BytesIO(f.getvalue()) for f in imgs_ejercicios] if imgs_ejercicios else []

# --- COMPILACIÓN ---
if st.button("🚀 Compilar Material Profesional"):
    bibliografia = detectar_bibliografia(texto_teoria + " " + texto_ejercicios)
    
    # --- WORD (PRIMERA HOJA CON PERFIL) ---
    doc = Document()
    f_circ = hacer_circulo('perfil.jpeg')
    
    # Configurar Encabezado solo primera página (vía sección)
    if f_circ:
        header = doc.sections[0].header
        header.is_linked_to_previous = False
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run().add_picture(f_circ, width=Inches(1.1))

    doc.add_heading(titulo, 0)
    p_firma = doc.add_paragraph()
    run_f = p_firma.add_run(f"Autor: {firma_oficial}")
    run_f.italic = True
    run_f.font.size = Pt(10)
    p_firma.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(intro_formal)
    doc.add_heading('II. Fundamento Teórico', 1); doc.add_paragraph(texto_teoria)
    doc.add_heading('III. Desarrollo Analítico', 1); doc.add_paragraph(latex_res)
    if buf_graf.getbuffer().nbytes > 0: doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('IV. Ejercicios Propuestos', 1); doc.add_paragraph(texto_ejercicios)
    for b in list_img_buf: doc.add_picture(b, width=Inches(3.5))
    
    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(conclu_formal)
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(recom_formal)
    
    doc.add_page_break()
    doc.add_heading('Referencias Bibliográficas (APA)', 1)
    for bib in bibliografia: doc.add_paragraph(bib, style='List Bullet')
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX (AJUSTE PGFPLOTS PROFESIONAL) ---
    bib_latex = "\\begin{itemize}\n" + "\n".join([f"\\item {b}" for b in bibliografia]) + "\n\\end{itemize}"
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, pgfplots, amssymb, geometry}}
\\geometry{{a4paper, margin=1in}}
\\pgfplotsset{{compat=1.18}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} 
\\author{{{firma_oficial}}}
\\date{{\\today}}
\\maketitle

\\section{{Introducción}} {intro_formal}
\\section{{Teoría}} {texto_teoria}
\\section{{Análisis Matemático}} $$ {latex_res} $$

\\section{{Gráfica de la Función}}
\\begin{{center}}
\\begin{{tikzpicture}}
\\begin{{axis}}[
    axis lines=middle, grid=major, 
    xlabel=$x$, ylabel=$y$,
    title={{$f(x) = {func_in}$}},
    domain=-5:5, samples=100,
    ]
    \\addplot[blue, ultra thick] {{{func_in.replace('np.', '')}}};
\\end{{axis}}
\\end{{tikzpicture}}
\\end{{center}}

\\section{{Ejercicios Propuestos}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {conclu_formal}
\\section{{Bibliografía (APA)}} {bib_latex}
\\end{{document}}"""

    st.download_button("⬇️ Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ LaTeX Científico", latex_str, f"{titulo}.tex")
    st.success("¡Documento de alta jerarquía generado!")
