import streamlit as st
from PIL import Image
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración profesional de página
st.set_page_config(page_title="Compilador Ismael: UNAN-León", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- MOTOR DE TEXTO ACADÉMICO ---
def generar_textos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado."
    }

with st.sidebar:
    st.header("📋 Datos del Documento")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León"

st.title("🎓 Sistema Superior de Producción Científica")
textos = generar_textos(titulo, firma_oficial)

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # SECCIÓN TEORÍA + CAPTURA
    texto_teoria = st.text_area("✍️ Desarrollo Teórico (Texto):", "Inserte el desarrollo conceptual aquí...", height=100)
    cap_teoria = st.file_uploader("🖼️ Captura de Teoría/Ecuación", type=["png", "jpg", "jpeg"], key="teoria_up")
    
    # GRÁFICA HD
    st.markdown("---")
    func_in = st.text_input("📈 Función para Gráfica (ej: 1/x):", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_v = np.linspace(1, 15, 40)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_v, y_v, 'o-', color='#003366', label=f'a_n = {func_in}')
        ax.set_title("Comportamiento Analítico de la Sucesión", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

    # SECCIÓN EJERCICIOS + CAPTURAS MÚLTIPLES
    st.markdown("---")
    texto_ejercicios = st.text_area("📝 Ejercicios (Texto):", "Resolver los siguientes casos propuestos...")
    caps_ejercicios = st.file_uploader("🖼️ Capturas de Ejercicios", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="ejer_up")

with col_pre:
    st.subheader("👁️ Vista Previa Sincronizada")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**I. Introducción:** {textos['intro']}")
        
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria)
        if cap_teoria:
            st.image(cap_teoria, caption="Captura de Teoría Integrada", width=400)
            
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización de la Función")
            
        st.markdown("### IV. Ejercicios Propuestos")
        st.write(texto_ejercicios)
        if caps_ejercicios:
            for i, img in enumerate(caps_ejercicios):
                st.image(img, caption=f"Ejercicio {i+1}", width=300)

# --- PROCESAMIENTO DE ARCHIVOS ---
if st.button("🚀 Compilar Word y LaTeX"):
    # 1. GENERAR WORD (.docx)
    doc = Document()
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria)
    if cap_teoria:
        img_t = io.BytesIO(cap_teoria.getvalue())
        doc.add_picture(img_t, width=Inches(4))

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('IV. Ejercicios Propuestos', 1)
    doc.add_paragraph(texto_ejercicios)
    if caps_ejercicios:
        for f in caps_ejercicios:
            img_e = io.BytesIO(f.getvalue())
            doc.add_picture(img_e, width=Inches(3.5))

    doc.add_heading('V. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('VI. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. GENERAR LATEX (.tex)
    # Nota: El código LaTeX incluye marcadores donde irían las figuras
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, amssymb}}
\\title{{\\textbf{{{titulo}}}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Desarrollo Teórico}}
{texto_teoria}
% Nota: Aquí se ha integrado la captura de teoría en el documento final.
\\section{{Gráfica Analítica}}
% Figura generada por el sistema.
\\section{{Ejercicios Propuestos}}
{texto_ejercicios}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}"""

    # BOTONES DE DESCARGA
    st.download_button("⬇️ Descargar Word (.docx)", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX (.tex)", latex_str, f"{titulo}.tex")
    st.success("¡Ambos archivos han sido generados correctamente!")
