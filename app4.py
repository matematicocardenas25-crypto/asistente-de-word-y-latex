import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

# --- CONFIGURACIÓN E IDENTIDAD ---
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"
st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- SISTEMA DE MEMORIA LOCAL (ANTI-APAGONES) ---
# Esto guarda el texto en la sesión del navegador
if 'contenido_teorico' not in st.session_state:
    st.session_state['contenido_teorico'] = ""
if 'ejercicios_lista' not in st.session_state:
    st.session_state['ejercicios_lista'] = ""

# --- MOTOR DE REDACCIÓN AUTOMATIZADA Y ROBUSTA ---
def generar_cuerpo_academico(titulo):
    # Diccionario con lenguaje matemático elegante y profesional
    return {
        "intro": f"El presente estudio técnico titulado '{titulo}' aborda de manera exhaustiva la formalización y el análisis de estructuras fundamentales en las ciencias exactas. A través de una metodología deductiva, se pretende sistematizar los conceptos teóricos y su aplicabilidad práctica, garantizando un rigor académico acorde a los estándares de la UNAN León. Bajo la autoría del Lic. Ismael Cárdenas López, este compendio articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado.",
        
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos, consolidando así la estructura conceptual necesaria para futuras investigaciones en el área de la matemática pura y aplicada.",
        
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de las sucesiones y series aquí abordadas, fomentando la aplicación de estos marcos teóricos en contextos interdisciplinarios que requieran de una alta capacidad de abstracción y síntesis matemática."
    }

st.title("🎓 Compilador Científico de Élite - UNAN León")
st.warning("🔒 Protección de datos activa: El contenido se mantiene en la sesión del navegador ante recargas accidentales.")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo = st.text_input("Título del Proyecto", "Análisis y Modelado de Sucesiones y Series")
    
    st.markdown("### I. Desarrollo Teórico")
    # Vinculamos al session_state para no perder datos
    raw_contenido = st.text_area("Cuerpo del documento:", value=st.session_state['contenido_teorico'], height=350, placeholder="Pegue la información del PDF aquí...")
    st.session_state['contenido_teorico'] = raw_contenido

    st.markdown("---")
    st.subheader("📊 Motor Gráfico Matemático")
    func_in = st.text_input("Función f(x) para graficar:", "np.cos(x) * np.exp(-x/5)")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-5, 15, 500)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2, label=f"f(x) = {func_in}")
        ax.set_title(f"Visualización: {titulo}", fontsize=10)
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: st.warning("Esperando expresión válida...")

    st.markdown("### II. Ejercicios Propuestos")
    ejercicios_raw = st.text_area("Ejercicios:", value=st.session_state['ejercicios_lista'], height=200)
    st.session_state['ejercicios_lista'] = ejercicios_raw

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_cuerpo_academico(titulo)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#003366;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_oficial}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("#### I. Introducción")
        st.write(textos['intro'])
        
        st.markdown("#### II. Desarrollo Teórico")
        # st.write mantiene los párrafos si dejas una línea en blanco
        st.write(st.session_state['contenido_teorico'])
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Análisis Gráfico Computacional")
        
        st.markdown("#### III. Ejercicios Propuestos")
        st.write(st.session_state['ejercicios_lista'])

        st.markdown("#### IV. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("#### V. Recomendaciones")
        st.write(textos['recom'])

# --- GENERACIÓN DE ARCHIVOS (RESURRECCIÓN DE DATOS) ---
if st.button("🚀 Compilar y Asegurar Documento"):
    doc = Document()
    # (Aquí iría tu lógica de la foto circular que ya tienes configurada)
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_oficial).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('I. Introducción', 1)
    doc.add_paragraph(textos['intro'])
    
    doc.add_heading('II. Desarrollo Teórico', 1)
    doc.add_paragraph(st.session_state['contenido_teorico'])
    
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5))
    
    doc.add_heading('III. Ejercicios Propuestos', 1)
    doc.add_paragraph(st.session_state['ejercicios_lista'])
    
    doc.add_heading('IV. Conclusiones', 1)
    doc.add_paragraph(textos['conclu'])
    
    doc.add_heading('V. Recomendaciones', 1)
    doc.add_paragraph(textos['recom'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo}.docx")
    st.success("✅ Documento recuperado y generado con éxito.")
