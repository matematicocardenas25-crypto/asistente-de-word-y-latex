import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración Superior
st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

# --- MOTOR DE TEXTO ACADÉMICO ROBUSTO ---
def generar_textos_elite(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. Cárdenas López, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}, buscando cerrar la brecha entre la teoría pura y la aplicación práctica.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos analizados. Los resultados validan la rigurosidad del método aplicado.",
        "recom": "Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado, sugiriendo la extensión de este análisis a modelos dinámicos de mayor complejidad."
    }

# --- PROCESADOR DE IMAGEN PERFIL (CIRCULAR) ---
def preparar_foto_circular(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        min_dim = min(img.size)
        img = img.crop(((img.width - min_dim) // 2, (img.height - min_dim) // 2, (img.width + min_dim) // 2, (img.height + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        img.putalpha(mascara)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except:
        return None

st.title("🎓 Compilador Científico Profesional - UNAN León")

with st.sidebar:
    st.header("📋 Parámetros del Documento")
    titulo = st.text_input("Título del Proyecto", "Análisis de Modelos Matemáticos")
    st.info(f"Autor: {firma_oficial}")

textos = generar_textos_elite(titulo)
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos de Contenido")
    texto_teoria = st.text_area("✍️ Desarrollo Teórico (Contenido de capturas):", height=150, placeholder="Escriba o pegue aquí el desarrollo...")
    
    st.markdown("---")
    st.subheader("📊 Gráfica Universal")
    st.caption("Física, Estadística, Cálculo (Ej: np.sin(x), np.exp(-x), x**2)")
    func_in = st.text_input("Defina f(x):", "np.sin(x) * np.exp(-0.1*x)")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-5, 15, 500)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2, label=f'f(x) = {func_in}')
        ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300)
        buf_graf.seek(0)
        plt.close(fig)
    except:
        st.warning("Ingrese una función válida para visualizar.")

    st.markdown("---")
    texto_ejercicios = st.text_area("📝 Ejercicios Propuestos:", "1. Calcule la derivada...\n2. Analice la convergencia...", height=100)

with col_pre:
    st.subheader("👁️ Vista Previa Completa (No trabaje a ciegas)")
    with st.container(border=True):
        # Simulación de encabezado superior derecho
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color: gray;'>{firma_oficial}</p>", unsafe_allow_html=True)
        
        st.markdown("### I. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### II. Desarrollo Teórico")
        st.write(texto_teoria if texto_teoria else "*Esperando contenido...*")
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Gráfica HD Generada")
            
        st.markdown("### III. Ejercicios Propuestos")
        st.write(texto_ejercicios if texto_ejercicios else "*Esperando ejercicios...*")
        
        st.markdown("### IV. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("### V. Recomendaciones")
        st.write(textos['recom'])

# --- COMPILACIÓN FINAL ---
if st.button("🚀 Generar Word Premium y LaTeX"):
    doc = Document()
    
    # 1. Foto y Fecha (Superior Derecha)
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p_h = header.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto = preparar_foto_circular('perfil.png') # Debe existir perfil.png en tu carpeta
    if foto:
        p_h.add_run().add_picture(foto, width=Inches(0.8))
    p_h.add_run(f"\nFecha: {fecha_actual}").bold = True

    # Título y Firma
    t = doc.add_heading(titulo, 0); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f = doc.add_paragraph(firma_oficial); f.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Estructura de Secciones
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo Teórico', 1); doc.add_paragraph(texto_teoria)
    
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
        
    doc.add_heading('III. Ejercicios Propuestos', 1); doc.add_paragraph(texto_ejercicios)
    doc.add_heading('IV. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('V. Recomendaciones', 1); doc.add_paragraph(textos['recom'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX Sincronizado
    latex_str = f"\\documentclass{{article}}\\usepackage[utf8]{{inputenc}}\\usepackage{{amsmath,graphicx}}\\title{{{titulo}}}\\author{{{firma_oficial}}}\\date{{{fecha_actual}}}\\begin{{document}}\\maketitle\\section{{Introducción}}{textos['intro']}\\section{{Teoría}}{texto_teoria}\\section{{Ejercicios}}{texto_ejercicios}\\section{{Conclusiones}}{textos['conclu']}\\end{{document}}"

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX Pro", latex_str, f"{titulo}.tex")
    st.success("¡Archivos listos para entregar!")
