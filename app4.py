import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# --- BLOQUE DE DESBLOQUEO DE PERMISOS (SOLUCIÓN AL ERROR ROJO) ---
# Forzamos al modelo a instalarse en la carpeta temporal con permisos totales
os.environ['PIX2TEX_MODEL_DIR'] = '/tmp/pix2tex'
if not os.path.exists('/tmp/pix2tex'):
    os.makedirs('/tmp/pix2tex', exist_ok=True)

st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")

fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO CIENTÍFICO ---
def generar_textos_robustos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos analizados.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado en Nicaragua."
    }

@st.cache_resource
def cargar_modelo_ocr():
    try:
        # Iniciamos el motor en la zona segura desbloqueada
        return LatexOCR()
    except Exception as e:
        st.error(f"Error técnico de permisos: {e}. Intente refrescar la página.")
        return None

# --- ESTADO DE SESIÓN (PARA QUE NO SE BORRE NADA) ---
if 'ocr_resultado' not in st.session_state: st.session_state.ocr_resultado = ""
if 'imagenes_ejercicios' not in st.session_state: st.session_state.imagenes_ejercicios = []

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León"

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_robustos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # TEORÍA + INTEGRACIÓN DE CAPTURA
    texto_teoria = st.text_area("✍️ Desarrollo Teórico (Texto):", "Inserte el desarrollo conceptual aquí...", height=100)
    file_ocr = st.file_uploader("🔢 Captura de Ecuación (Integración Automática)", type=["png", "jpg", "jpeg"])
    
    if file_ocr:
        model = cargar_modelo_ocr()
        if model:
            with st.spinner("Desbloqueando motor y procesando imagen..."):
                # Se guarda la transcripción en el cerebro del programa
                st.session_state.ocr_resultado = model(Image.open(file_ocr))
            st.success("¡Contenido de la captura integrado!")
            st.latex(st.session_state.ocr_resultado)

    # GRÁFICA HD (REVISADA PARA EVITAR SYNTAX ERROR)
    func_in = st.text_input("📈 Modelo para Gráfica HD:", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_v = np.linspace(1, 15, 40)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_v, y_v, 'o-', color='#003366', label=f'a_n = {func_in}')
        ax.set_title("Análisis Gráfico de la Sucesión", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300)
        buf_graf.seek(0)
    except:
        pass

    # EJERCICIOS + CAPTURAS
    st.markdown("---")
    texto_ejercicios = st.text_area("📝 Ejercicios Propuestos (Texto):", "Resolver los siguientes casos...")
    imgs_ejercicios = st.file_uploader("🖼️ Capturas de Guías de Ejercicios", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if imgs_ejercicios:
        st.session_state.imagenes_ejercicios = [io.BytesIO(f.getvalue()) for f in imgs_ejercicios]

with col_pre:
    st.subheader("👁️ Vista Previa Sincronizada")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**I. Introducción:** {textos['intro']}")
        
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria)
        if st.session_state.ocr_resultado:
            st.markdown("**Fórmula extraída de la imagen:**")
            st.latex(st.session_state.ocr_resultado)
            
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización Analítica")
            
        st.markdown("### IV. Ejercicios Propuestos")
        st.write(texto_ejercicios)
        for img_data in st.session_state.imagenes_ejercicios:
            st.image(img_data, width=350)

# --- COMPILACIÓN FINAL ---
if st.button("🚀 Compilar y Sincronizar Documentos"):
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    # INTEGRACIÓN DE CAPTURA EN EL WORD
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria)
    if st.session_state.ocr_resultado:
        doc.add_paragraph(f"Expresión Matemática Detectada: {st.session_state.ocr_resultado}")

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('IV. Ejercicios Propuestos', 1)
    doc.add_paragraph(texto_ejercicios)
    for img_buf in st.session_state.imagenes_ejercicios:
        doc.add_picture(img_buf, width=Inches(3.5))

    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX Sincronizado
    latex_str = f"\\documentclass{{article}}\\usepackage[utf8]{{inputenc}}\\usepackage{{amsmath,graphicx}}\\begin{{document}}\\title{{{titulo}}}\\author{{{firma_oficial}}}\\maketitle\\section{{Introducción}}{textos['intro']}\\section{{Teoría}}{texto_teoria} $$ {st.session_state.ocr_resultado} $$ \\section{{Ejercicios}}{texto_ejercicios}\\section{{Conclusiones}}{textos['conclu']}\\section{{Recomendaciones}}{textos['recom']}\\end{{document}}"

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Permisos desbloqueados y archivos listos!")
