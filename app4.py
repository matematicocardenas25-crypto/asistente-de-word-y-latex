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
    except:
        return None

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    autor = st.text_input("Autor del Proyecto", "Ismael Antonio Cárdenas, Licenciado en Matemáticas, UNAN-León")
    st.info("Sube 'perfil.jpeg' a tu repositorio para personalizar la portada.")

st.title("🎓 Sistema de Producción de Contenidos Científicos")

# --- LÓGICA DE TEXTOS CIENTÍFICOS (Preservando rigor y tildes) ---
intro_formal = f"El presente compendio técnico, enfocado en '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la supervisión del {autor}, este documento articula la abstracción algebraica con la fenomenología visual, proporcionando un entorno de aprendizaje basado en la precisión deductiva."
conclu_formal = f"Tras el estudio exhaustivo de '{titulo}', se establece que la modelación matemática digital permite una comprensión unificada de las estructuras asintóticas y el comportamiento de las funciones. La integración de estas herramientas eleva la calidad del análisis pedagógico contemporáneo."
recom_formal = f"Se insta al investigador a realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada en este análisis de '{titulo}'. La práctica constante de los ejercicios propuestos es imperativa para la consolidación del pensamiento lógico-matemático."

# --- INTERFAZ DE USUARIO ---
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Carga de Material")
    
    # 1. OCR para el ejercicio resuelto
    file_ocr = st.file_uploader("1. Sube la imagen del Ejercicio Resuelto (OCR)", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if file_ocr:
        img = Image.open(file_ocr)
        with st.spinner("Analizando sintaxis matemática..."):
            model = LatexOCR()
            latex_res = model(img)
        st.latex(latex_res)

    # 2. Generación de Gráfica
    func_in = st.text_input("2. Función para graficar (ej: np.sin(x)/x):", "x**2")
    buf_graf = io.BytesIO()
    try:
        x = np.linspace(-10, 10, 1000)
        y = eval(func_in.replace('^', '**'), {"x": x, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(x, y, color='darkblue', linewidth=1.5)
        ax.axhline(0, color='black', lw=0.8); ax.axvline(0, color='black', lw=0.8)
        ax.grid(True, linestyle=':', alpha=0.6)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except:
        st.warning("Escriba una función válida para generar la gráfica.")

    # 3. Sección de Ejercicios y Capturas
    st.markdown("---")
    st.subheader("📝 Sección de Ejercicios")
    texto_props = st.text_area("Enunciados de los ejercicios:", "Determine el dominio y rango de la función analizada.")
    
    # Nuevo cargador múltiple para reemplazar el error de pegado
    st.write("📸 **Carga de capturas de pantalla:**")
    imgs_subidas = st.file_uploader("Sube todas las capturas de ejercicios aquí:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    list_img_buf = []
    if imgs_subidas:
        for f in imgs_subidas:
            img_p = Image.open(f)
            b = io.BytesIO()
            img_p.save(b, format="PNG")
            b.seek(0)
            list_img_buf.append(b)
        st.success(f"Se han cargado {len(list_img_buf)} capturas.")

with col_pre:
    st.subheader("👁️ Pre-compilación del Documento")
    with st.container(border=True):
        st.markdown(f"<p style='text-align:right;'><b>{autor}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"**Introducción:**\n{intro_formal}")
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización Analítica")
        if latex_res:
            st.latex(latex_res)
        st.markdown(f"**Ejercicios Propuestos:**\n{texto_props}")

# --- GENERACIÓN DE ARCHIVOS ---
st.divider()
if st.button("🚀 Generar Guía Científica Final"):
    # Bibliografía APA automática
    f_db = {"stewart": "Stewart, J. (2015). Cálculo. Cengage.", "larson": "Larson, R. (2017). Cálculo. Cengage."}
    bibs = [v for k, v in f_db.items() if k in (texto_props + " " + titulo).lower()]
    if not bibs: bibs = ["Recurso educativo original diseñado bajo rigor académico."]

    # --- WORD ---
    doc = Document()
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ: 
        header = doc.sections[0].first_page_header
        header.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        header.paragraphs[0].add_run().add_picture(f_circ, width=Inches(1.1))
    
    doc.add_heading(titulo, 0)
    doc.add_heading('Introducción Formal', 1); doc.add_paragraph(intro_formal)
    doc.add_heading('Análisis Matemático', 1); doc.add_paragraph(latex_res)
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5))
    
    doc.add_heading('Ejercicios de Consolidación', 1); doc.add_paragraph(texto_props)
    for b in list_img_buf:
        doc.add_picture(b, width=Inches(4))
            
    doc.add_heading('Conclusiones Académicas', 1); doc.add_paragraph(conclu_formal)
    doc.add_heading('Recomendaciones Metodológicas', 1); doc.add_paragraph(recom_formal)
    doc.add_page_break(); doc.add_heading('Referencias Bibliográficas (APA)', 1)
    for b in bibs: doc.add_paragraph(b)
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- LATEX ---
    c_lat = "\\begin{itemize}\n" + "\n".join([f"\\item {c}" for c in bibs]) + "\n\\end{itemize}"
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, amssymb}}
\\begin{{document}}
\\title{{\\textbf{{{titulo}}}}} \\author{{{autor}}} \\maketitle
\\section{{Introducción Formal}} {intro_formal}
\\section{{Análisis Técnico}} \\\\ $ {latex_res} $ 
\\section{{Ejercicios Propuestos}} {texto_props.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {conclu_formal}
\\section{{Bibliografía}} {c_lat}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Material generado correctamente!")
