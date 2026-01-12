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

fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO CIENTÍFICO ---
def generar_textos_robustos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos analizados.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático."
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

# --- ESTADO DE SESIÓN PARA PERSISTENCIA ---
if 'ocr_teoria' not in st.session_state: st.session_state.ocr_teoria = ""
if 'lista_ejercicios_imagenes' not in st.session_state: st.session_state.lista_ejercicios_imagenes = []

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León, Nicaragua"

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_robustos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # SECCIÓN I: TEORÍA + OCR
    texto_teoria_usuario = st.text_area("✍️ Desarrollo Teórico (Escriba aquí):", "Inserte el desarrollo conceptual aquí...", height=100)
    file_ocr = st.file_uploader("🔢 Captura de Ecuación para Teoría", type=["png", "jpg", "jpeg"])
    
    if file_ocr:
        model = cargar_modelo_ocr()
        if model:
            with st.spinner("Transcribiendo ecuación..."):
                st.session_state.ocr_teoria = model(Image.open(file_ocr))
            st.info("Ecuación detectada e integrada al desarrollo.")
            st.latex(st.session_state.ocr_teoria)

    # SECCIÓN II: GRÁFICA
    func_in = st.text_input("📈 Modelo Matemático (Gráfica):", "1/x")
    buf_graf = io.BytesIO()
    try:
        x_v = np.linspace(1, 10, 20); y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(5, 3)); ax.scatter(x_v, y_v, color='#003366'); ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png'); buf_graf.seek(0)
    except: pass

    # SECCIÓN III: EJERCICIOS + IMÁGENES
    texto_ejercicios_usuario = st.text_area("📝 Ejercicios (Texto):", "1. Resolver los siguientes enunciados...")
    imgs_ejercicios = st.file_uploader("🖼️ Capturas de Apoyo para Ejercicios", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    st.session_state.lista_ejercicios_imagenes = [io.BytesIO(f.getvalue()) for f in imgs_ejercicios] if imgs_ejercicios else []

with col_pre:
    st.subheader("👁️ Vista Previa del Cuerpo del Documento")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {textos['intro']}")
        
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria_usuario)
        if st.session_state.ocr_teoria:
            st.latex(st.session_state.ocr_teoria)
            
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf, caption="Representación Visual")
        
        st.markdown("### IV. Ejercicios Propuestos")
        st.write(texto_ejercicios_usuario)
        for img in st.session_state.lista_ejercicios_imagenes:
            st.image(img, width=300)

# --- COMPILACIÓN FINAL SIN PÉRDIDAS ---
if st.button("🚀 Compilar Documentos"):
    doc = Document()
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    
    # Encabezado con imagen circular
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ:
        p = seccion.first_page_header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run().add_picture(f_circ, width=Inches(1))

    # Título y Autor
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Cuerpo del Documento Integrado
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    # Integración de Teoría + OCR
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria_usuario)
    if st.session_state.ocr_teoria:
        doc.add_paragraph(f"Análisis Analítico: {st.session_state.ocr_teoria}")

    if buf_graf.getbuffer().nbytes > 0: doc.add_picture(buf_graf, width=Inches(4))
    
    # Integración de Ejercicios + Imágenes
    doc.add_heading('IV. Ejercicios Propuestos', 1)
    doc.add_paragraph(texto_ejercicios_usuario)
    for img_buf in st.session_state.lista_ejercicios_imagenes:
        doc.add_picture(img_buf, width=Inches(3.5))

    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    # Bibliografía
    doc.add_page_break()
    doc.add_heading('Bibliografía (APA)', 1)
    doc.add_paragraph("Recurso educativo original, UNAN-León (2026).", style='List Bullet')

    # Guardar Word
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # Generar LaTeX con la misma estructura
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx}}
\\begin{{document}}
\\title{{{titulo}}} \\author{{{firma_oficial}}} \\date{{{fecha_actual}}} \\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Teoría}} {texto_teoria_usuario} \\\\ $$ {st.session_state.ocr_teoria} $$
\\section{{Ejercicios}} {texto_ejercicios_usuario}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Documentos integrados correctamente!")
