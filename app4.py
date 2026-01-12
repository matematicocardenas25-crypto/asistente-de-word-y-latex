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

# Configuración de página de alta calidad
st.set_page_config(page_title="Compilador Científico - Ismael Cárdenas", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- GENERADOR DE TEXTOS ROBUSTOS (Academia de Élite) ---
def generar_textos_robustos(titulo, firma):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. {firma}, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}, buscando cerrar la brecha entre la teoría pura y la aplicación práctica.",
        "conclu": f"Tras el estudio exhaustivo de los modelos presentados en '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos. Se confirma que la rigurosidad en la formulación es el pilar de la interpretación científica moderna.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado. Asimismo, se sugiere la extensión de este análisis a modelos de mayor complejidad para validar las tendencias observadas."
    }

# --- ESTADO DE SESIÓN ---
if 'texto_pegado' not in st.session_state: st.session_state.texto_pegado = ""

with st.sidebar:
    st.header("📋 Configuración del Documento")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    firma_oficial = "Ismael Antonio Cárdenas López, Licenciado en Matemáticas, UNAN-León"

st.title("🎓 Sistema Superior de Producción Científica")
st.info("Sistema optimizado: Pegue el contenido de sus capturas abajo para integrarlo automáticamente.")

textos = generar_textos_robustos(titulo, firma_oficial)
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    
    # SECCIÓN I: DESARROLLO TEÓRICO (Aquí pegas lo que copies de tus imágenes)
    st.markdown("### I. Contenido Analítico")
    texto_teoria = st.text_area("✍️ Pegue aquí el texto/fórmulas de sus capturas:", 
                                value=st.session_state.texto_pegado, 
                                height=200,
                                help="Copie el texto de su imagen y péguelo aquí. Se incluirá como texto real en el Word y LaTeX.")
    
    # SECCIÓN II: GRÁFICA HD
    st.markdown("---")
    st.markdown("### II. Visualización de Alta Definición")
    func_in = st.text_input("📈 Modelo Matemático (ej: n/(n+1)):", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_v = np.linspace(1, 15, 50)
        y_v = eval(func_in.replace('^', '**'), {"x": x_v, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_v, y_v, 'o-', color='#003366', linewidth=2, markersize=6, label=f'f(n) = {func_in}')
        ax.set_title(f"Comportamiento Analítico: {titulo}", fontsize=12, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300) # Máxima calidad para impresión
        plt.close(fig)
        buf_graf.seek(0)
    except:
        st.warning("Ingrese una función válida para generar la gráfica.")

    # SECCIÓN III: EJERCICIOS
    st.markdown("---")
    st.markdown("### III. Guía de Ejercicios")
    enunciado_ejercicios = st.text_area("📝 Enunciados de la Guía:", "Determine la convergencia o divergencia de...")

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.write(f"**Introducción:** {textos['intro']}")
        
        st.markdown("#### II. Desarrollo")
        st.write(texto_teoria)
        if texto_teoria:
            try: st.latex(texto_teoria)
            except: pass
            
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Gráfica Científica Generada en 300 DPI")
            
        st.markdown("#### IV. Conclusiones")
        st.write(textos['conclu'])

# --- COMPILACIÓN FINAL (Word + LaTeX) ---
if st.button("🚀 Compilar Documentos de Élite"):
    # 1. GENERACIÓN DE WORD
    doc = Document()
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"Autor: {firma_oficial}\nLeón, Nicaragua | {fecha_actual}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(texto_teoria)

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    
    doc.add_heading('III. Ejercicios Propuestos', 1)
    doc.add_paragraph(enunciado_ejercicios)

    doc.add_heading('IV. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('V. Recomendaciones', 1); doc.add_paragraph(textos['recom'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. GENERACIÓN DE LATEX
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
\\section{{Ejercicios Propuestos}} {enunciado_ejercicios}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium (.docx)", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX (.tex)", latex_str, f"{titulo}.tex")
    st.success("¡Documentos sincronizados con éxito!")
