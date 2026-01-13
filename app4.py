import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import json
from datetime import datetime

# --- IDENTIDAD Y CONFIGURACIÓN ---
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"
st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA (PROFESIONAL Y ELEGANTE) ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos y la estabilidad de los marcos conceptuales analizados.",
        
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios que requieran una alta capacidad de abstracción y síntesis matemática."
    }

# --- PERSISTENCIA DE DATOS (ANTI-REFRESCO) ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

# --- PANEL LATERAL DE RESPALDO ---
with st.sidebar:
    st.header("💾 Respaldo de Seguridad")
    if st.button("📥 Crear Punto de Restauración"):
        data_respaldo = {"titulo": "Proyecto", "contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo (.json)", json.dumps(data_respaldo), "respaldo_ismael.json")
    st.info("Si se va la luz, el archivo de respaldo te permitirá recuperar todo instantáneamente.")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    
    st.markdown("### I. Desarrollo Teórico")
    cont_input = st.text_area("Cuerpo del Contenido:", value=st.session_state.contenido, height=350, key="area_cont")
    st.session_state.contenido = cont_input

    st.markdown("---")
    st.subheader("📊 Motor Gráfico Matemático")
    func_in = st.text_input("Función f(x):", "np.sin(x) * np.exp(-x/10)")
    
    buf_graf = io.BytesIO()
    try:
        x_vals = np.linspace(-10, 20, 1000)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x_vals, y_vals, color='#1A5276', linewidth=2, label=f"f(x)={func_in}")
        ax.set_title(f"Análisis Paramétrico: {titulo_proy}")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: st.warning("Esperando función válida...")

    st.markdown("### II. Ejercicios Propuestos")
    ejer_input = st.text_area("Lista de Ejercicios:", value=st.session_state.ejercicios, height=200, key="area_ejer")
    st.session_state.ejercicios = ejer_input

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><i>{firma_oficial}</i></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 1. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### 2. Desarrollo Teórico")
        st.markdown(st.session_state.contenido)
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Representación Gráfica del Comportamiento Analítico")
        
        st.markdown("### 3. Ejercicios Propuestos")
        st.markdown(st.session_state.ejercicios)
        
        st.markdown("### 4. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("### 5. Recomendaciones")
        st.write(textos['recom'])

# --- GENERACIÓN DE DOCUMENTOS (WORD Y LATEX) ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    
    # 1. GENERACIÓN WORD
    doc = Document()
    doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_oficial).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    secciones_doc = [("I. Introducción", textos['intro']), 
                     ("II. Desarrollo Teórico", st.session_state.contenido),
                     ("III. Ejercicios Propuestos", st.session_state.ejercicios),
                     ("IV. Conclusiones", textos['conclu']),
                     ("V. Recomendaciones", textos['recom'])]
    
    for tit, cont in secciones_doc:
        doc.add_heading(tit, 1)
        for parrafo in cont.split('\n\n'):
            if parrafo.strip(): doc.add_paragraph(parrafo.strip())

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # 2. GENERACIÓN LATEX (RESTAURADO)
    latex_code = f"""
\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, graphicx}}
\\title{{{titulo_proy}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{I. Introducción}} {textos['intro']}
\\section{{II. Desarrollo Teórico}} 
{st.session_state.contenido}
\\section{{III. Ejercicios Propuestos}}
{st.session_state.ejercicios}
\\section{{IV. Conclusiones}} {textos['conclu']}
\\section{{V. Recomendaciones}} {textos['recom']}
\\end{{document}}
"""
    l_io = io.StringIO(latex_code)

    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar Código LaTeX (.tex)", l_io.getvalue(), f"{titulo_proy}.tex")
    st.success("¡Documentación técnica compilada con éxito!")
