import streamlit as st
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración Superior
st.set_page_config(page_title="Calculo Pro: Compilador de Élite", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO CIENTÍFICO (RECUPERADO) ---
def generar_textos_pro(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado."
    }

# --- ESTADO DE SESIÓN ---
if 'ocr_resultado' not in st.session_state: st.session_state.ocr_resultado = ""

with st.sidebar:
    st.header("📋 Configuración Profesional")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León"

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos_pro(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # SECCIÓN I: TEORÍA Y OCR
    st.markdown("### I. Desarrollo Teórico")
    texto_teoria = st.text_area("✍️ Texto base de la teoría:", "Inserte el desarrollo conceptual aquí...", height=100)
    
    cap_teoria = st.file_uploader("🔢 Captura de Ecuación (Para convertir a texto)", type=["png", "jpg", "jpeg"])
    if cap_teoria:
        st.image(cap_teoria, caption="Captura cargada para procesamiento", width=400)
        # Espacio para que el OCR o el usuario pongan el código y ahorren tiempo
        st.session_state.ocr_resultado = st.text_area("📝 Texto/LaTeX detectado de la imagen:", 
                                                   st.session_state.ocr_resultado,
                                                   help="El texto que pongas aquí se integrará automáticamente como fórmulas en los documentos.")
        if st.session_state.ocr_resultado:
            st.latex(st.session_state.ocr_resultado)

    # SECCIÓN II: GRÁFICA DE ALTA CALIDAD (RECUPERADA)
    st.markdown("---")
    st.markdown("### II. Visualización HD")
    func_in = st.text_input("📈 Modelo Matemático (ej: 1/x):", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_v = np.linspace(1, 15, 40)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_v, y_v, 'o-', color='#003366', linewidth=2, label=f'a_n = {func_in}')
        ax.set_title("Análisis Gráfico de la Sucesión", fontsize=12, fontweight='bold')
        ax.set_xlabel("Término (n)"); ax.set_ylabel("Valor (a_n)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300) # Calidad de impresión
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

    # SECCIÓN III: EJERCICIOS
    st.markdown("---")
    st.markdown("### III. Ejercicios y Guías")
    texto_ejercicios = st.text_area("📝 Enunciados de Ejercicios:", "Resolver los siguientes casos...")
    imgs_ejercicios = st.file_uploader("🖼️ Capturas de Guías de Ejercicios", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

with col_pre:
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {textos['intro']}")
        
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria)
        if st.session_state.ocr_resultado:
            st.latex(st.session_state.ocr_resultado)
            
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización Analítica HD")
            
        st.markdown("### IV. Ejercicios Propuestos")
        st.write(texto_ejercicios)
        if imgs_ejercicios:
            for img in imgs_ejercicios:
                st.image(img, width=350)

# --- COMPILACIÓN INTEGRAL (WORD + LATEX) ---
if st.button("🚀 Compilar Word y LaTeX de Alta Calidad"):
    # 1. WORD PROFESIONAL
    doc = Document()
    # Estilo de título
    header = doc.add_heading(titulo, 0)
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria)
    if st.session_state.ocr_resultado:
        doc.add_paragraph(f"Expresión Matemática Detectada: {st.session_state.ocr_resultado}")

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('IV. Ejercicios Propuestos', 1)
    doc.add_paragraph(texto_ejercicios)
    if imgs_ejercicios:
        for img_f in imgs_ejercicios:
            doc.add_picture(io.BytesIO(img_f.getvalue()), width=Inches(3.5))

    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. LATEX PROFESIONAL
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, amssymb, xcolor}}
\\title{{\\textbf{{{titulo}}}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Desarrollo Teórico}}
{texto_teoria}
\\begin{{equation}}
{st.session_state.ocr_resultado if st.session_state.ocr_resultado else "% No se detectó fórmula"}
\\end{{equation}}
\\section{{Ejercicios}} {texto_ejercicios}
\\section{{Conclusiones}} {textos['conclu']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium (.docx)", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX Pro (.tex)", latex_str, f"{titulo}.tex")
    st.success("¡Documentos de alta calidad generados!")
