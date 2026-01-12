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
from datetime import datetime

# Configuración de entorno
os.environ['PIX2TEX_MODEL_DIR'] = '/tmp/pix2tex'

st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")

# Fecha automatizada
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE GENERACIÓN DE TEXTO CIENTÍFICO (ROBUSTO) ---
def generar_textos_robustos(titulo, firma):
    return {
        "intro": (
            f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los "
            f"fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento "
            f"articula la abstracción algebraica con la fenomenología visual, garantizando un rigor deductivo "
            f"en la transición de los modelos teóricos a la representación digital a fecha de {fecha_actual}."
        ),
        "conclu": (
            f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico "
            f"y la visualización paramétrica permite una comprensión holística de los comportamientos funcionales. "
            f"La integración técnica presentada eleva los estándares del análisis pedagógico en la UNAN-León, "
            f"consolidando la abstracción como base del pensamiento lógico-formal."
        ),
        "recom": (
            f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica manual y la "
            f"verificación computacional presentada en este análisis de '{titulo}'. Se recomienda la exploración "
            f"de casos límite y el rigor en la práctica de los ejercicios propuestos para la consolidación del "
            f"pensamiento matemático avanzado en Nicaragua."
        )
    }

@st.cache_resource
def cargar_modelo_ocr():
    try: return LatexOCR()
    except: return None

def hacer_circulo(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        min_dim = min(img.size)
        img = img.crop(((img.width - min_dim) // 2, (img.height - min_dim) // 2, (img.width + min_dim) // 2, (img.height + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        ImageDraw.Draw(mascara).ellipse((0, 0, min_dim, min_dim), fill=255)
        img.putalpha(mascara)
        buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
        return buf
    except: return None

def detectar_bibliografia(texto):
    db = {
        "stewart": "Stewart, J. (2020). Cálculo de una variable (9na ed.). Cengage.",
        "larson": "Larson, R. (2022). Cálculo (12va ed.). Cengage Learning.",
        "leithold": "Leithold, L. (1998). El Cálculo (7ma ed.). Oxford."
    }
    encontradas = [v for k, v in db.items() if k in texto.lower()]
    return encontradas if encontradas else ["Recurso educativo original, UNAN-León (2026)."]

# --- ESTADO DE SESIÓN ---
if 'latex_transcrito' not in st.session_state: st.session_state.latex_transcrito = ""

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    st.write(f"📅 **Fecha:** {fecha_actual}")

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_robustos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    texto_teoria = st.text_area("✍️ Fundamentación Teórica:", "Inserte el desarrollo conceptual aquí...", height=150)
    
    file_ocr = st.file_uploader("🔢 Captura de Ecuación (OCR)", type=["png", "jpg", "jpeg"])
    if file_ocr:
        model = cargar_modelo_ocr()
        if model:
            with st.spinner("Analizando captura..."):
                st.session_state.latex_transcrito = model(Image.open(file_ocr))
            st.latex(st.session_state.latex_transcrito)

    func_in = st.text_input("📈 Función/Sucesión (ej: 1/x):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(1, 10, 20)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter(x_v, y_v, color='#003366')
        ax.grid(True, linestyle=':', alpha=0.6)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    texto_ejercicios = st.text_area("📝 Ejercicios Propuestos:", "1. Resolver...", height=100)

with col_pre:
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        st.markdown(f"<p style='text-align:right;'><b>{firma_oficial}</b><br>{fecha_actual}</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"**I. Introducción:** {textos['intro']}")
        st.markdown(f"**II. Teoría:** {texto_teoria}")
        if st.session_state.latex_transcrito:
            st.markdown("**III. Análisis Analítico:**")
            st.latex(st.session_state.latex_transcrito)
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)
        st.markdown(f"**IV. Ejercicios:** {texto_ejercicios}")
        st.markdown(f"**V. Conclusiones:** {textos['conclu']}")
        st.markdown(f"**VI. Recomendaciones:** {textos['recom']}")

# --- COMPILACIÓN ---
if st.button("🚀 Compilar Archivos Finales"):
    bibliografia = detectar_bibliografia(texto_teoria + " " + texto_ejercicios)
    
    # --- GENERACIÓN WORD ---
    doc = Document()
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ:
        header = seccion.first_page_header
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run().add_picture(f_circ, width=Inches(1.1))
        p.add_run(f"\n{fecha_actual}").font.size = Pt(9)

    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Fundamentación Teórica', 1); doc.add_paragraph(texto_teoria)
    if st.session_state.latex_transcrito:
        doc.add_heading('III. Análisis Analítico', 1); doc.add_paragraph(st.session_state.latex_transcrito)
    if buf_graf.getbuffer().nbytes > 0: doc.add_picture(buf_graf, width=Inches(4.5))
    doc.add_heading('IV. Ejercicios Propuestos', 1); doc.add_paragraph(texto_ejercicios)
    doc.add_heading('V. Conclusiones Académicas', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones Metodológicas', 1); doc.add_paragraph(textos['recom'])
    
    doc.add_page_break()
    doc.add_heading('Bibliografía (APA)', 1)
    for bib in bibliografia: doc.add_paragraph(bib, style='List Bullet')

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- GENERACIÓN LATEX ---
    bib_latex = "\n".join([f"\\item {b}" for b in bibliografia])
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, pgfplots, amssymb}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} \\author{{{firma_oficial}}} \\date{{{fecha_actual}}} \\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Teoría}} {texto_teoria}
\\section{{Análisis}} $$ {st.session_state.latex_transcrito} $$
\\section{{Ejercicios}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\section{{Bibliografía}} \\begin{{itemize}} {bib_latex} \\end{{itemize}}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX Científico", latex_str, f"{titulo}.tex")
    st.success("¡Formatos restaurados y listos para descarga!")
