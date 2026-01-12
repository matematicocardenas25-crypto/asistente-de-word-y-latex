import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")

# Fecha automatizada
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE GENERACIÓN DE TEXTO CIENTÍFICO ---
def generar_textos_robustos(titulo, firma):
    textos = {
        "intro": (
            f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los "
            f"fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento "
            f"articula la abstracción algebraica con la fenomenología visual, garantizando un rigor deductivo "
            f"en la transición de los modelos teóricos a la representación digital. Se aborda la materia no solo "
            f"como una herramienta de cálculo, sino como un lenguaje estructural para la resolución de problemas complejos."
        ),
        "conclu": (
            f"Tras el estudio exhaustivo de las propiedades inherentes a '{titulo}', se establece que la convergencia "
            f"entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los "
            f"comportamientos funcionales. La evidencia analítica presentada demuestra que la formalización de estos "
            f"conceptos es fundamental para el desarrollo de un pensamiento lógico-formal robusto, permitiendo "
            f"interpretar la realidad a través del lente de la precisión matemática."
        ),
        "recom": (
            f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica manual y la "
            f"verificación computacional presentada en este análisis de '{titulo}'. Para optimizar el aprendizaje "
            f"pedagógico, se recomienda la implementación de modelos iterativos y la exploración de casos límite, "
            f"asegurando que el rigor metodológico de la UNAN-León prevalezca en cada etapa de la investigación "
            f"y la práctica docente."
        )
    }
    return textos

# --- FUNCIÓN DE PERFIL CIRCULAR ---
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
    db = {
        "stewart": "Stewart, J. (2020). Cálculo de una variable (9na ed.). Cengage.",
        "larson": "Larson, R. (2022). Cálculo (12va ed.). Cengage Learning.",
        "leithold": "Leithold, L. (1998). El Cálculo (7ma ed.). Oxford."
    }
    encontradas = [v for k, v in db.items() if k in texto.lower()]
    return encontradas if encontradas else ["Recurso educativo original, UNAN-León (2026)."]

# --- SIDEBAR ---
with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    st.write(f"📅 **Fecha:** {fecha_actual}")

st.title("🎓 Sistema Superior de Producción Científica")

# Generar textos automáticos
textos = generar_textos_robustos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    texto_teoria = st.text_area("✍️ Teoría (Desarrollo Conceptual):", "Inserte el fundamento teórico aquí...")
    
    file_ocr = st.file_uploader("🔢 Captura de Ecuación (OCR)", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if file_ocr:
        model = LatexOCR()
        latex_res = model(Image.open(file_ocr))
        st.latex(latex_res)

    st.markdown("---")
    func_in = st.text_input("📈 Función (ej: x**3 - 2*x):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(-10, 10, 400)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x_v, y_v, color='#003366', lw=2)
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    texto_ejercicios = st.text_area("📝 Ejercicios Propuestos:", "1. Determine la derivada...")
    imgs_ejercicios = st.file_uploader("🖼️ Apoyo Visual", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = [io.BytesIO(f.getvalue()) for f in imgs_ejercicios] if imgs_ejercicios else []

with col_pre:
    st.subheader("👁️ Vista Previa de Alta Gama")
    with st.container(border=True):
        st.markdown(f"<p style='text-align:right;'><b>{firma_oficial}</b><br>{fecha_actual}</p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {textos['intro'][:180]}...")
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)
        if latex_res: st.latex(latex_res)
        st.markdown("---")
        st.write("**Resumen de Conclusiones:** El análisis converge en la precisión simbólica...")

# --- COMPILACIÓN ---
if st.button("🚀 Compilar Documentos Profesionales"):
    bibliografia = detectar_bibliografia(texto_teoria + " " + texto_ejercicios)
    
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
    p_autor = doc.add_paragraph(f"Autor: {firma_oficial}")
    p_autor.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_autor.add_run(f"\nLeón, Nicaragua | {fecha_actual}").italic = True

    doc.add_heading('I. Introducción Formal', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo Teórico', 1); doc.add_paragraph(texto_teoria)
    if latex_res:
        doc.add_heading('III. Análisis Simbólico', 1); doc.add_paragraph(latex_res)
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('IV. Ejercicios de Consolidación', 1); doc.add_paragraph(texto_ejercicios)
    for b in list_img_buf: doc.add_picture(b, width=Inches(3.5))
    
    doc.add_heading('V. Conclusiones Académicas', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones Metodológicas', 1); doc.add_paragraph(textos['recom'])
    
    doc.add_page_break()
    doc.add_heading('Bibliografía (Normas APA 7ma Ed.)', 1)
    for bib in bibliografia: doc.add_paragraph(bib, style='List Bullet')

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX ---
    bib_latex = "\n".join([f"\\item {b}" for b in bibliografia])
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, pgfplots, amssymb}}
\\pgfplotsset{{compat=1.18}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} \\author{{{firma_oficial}}} \\date{{{fecha_actual}}} \\maketitle
\\section{{Introducción Formal}} {textos['intro']}
\\section{{Fundamentación Teórica}} {texto_teoria}
\\section{{Análisis Técnico}} $$ {latex_res} $$
\\section{{Representación Gráfica}}
\\begin{{center}} \\begin{{tikzpicture}}
\\begin{{axis}}[axis lines=middle, grid=major, xlabel=$x$, ylabel=$y$]
\\addplot[color=blue, thick, samples=100] {{{func_in.replace('np.', '')}}};
\\end{{axis}} \\end{{tikzpicture}} \\end{{center}}
\\section{{Consolidación Práctica}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\section{{Bibliografía}} \\begin{{itemize}} {bib_latex} \\end{{itemize}}
\\end{{document}}"""

    st.download_button("⬇️ Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ LaTeX Científico", latex_str, f"{titulo}.tex")
    st.success("¡Documentos con rigor académico generados!")
