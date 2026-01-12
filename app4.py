import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import re
from datetime import datetime

# --- DATOS DE IDENTIDAD ---
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- PROCESADOR DE TEXTO (FIX PARA PÁRRAFOS) ---
def procesar_parrafos(texto):
    # Divide el texto si hay demasiados espacios o si viene de Mathpix con saltos extraños
    lineas = texto.split('\n')
    texto_limpio = ""
    for linea in lineas:
        if linea.strip():
            texto_limpio += linea.strip() + "\n\n" # Asegura doble espacio entre párrafos
    return texto_limpio

# --- PROCESADOR DE IMAGEN (FOTO CIRCULAR) ---
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
    except: return None

# --- GENERADOR DE CONTENIDO MATEMÁTICO ROBUSTO ---
def generar_textos_profesionales(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. Cárdenas López, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos.",
        "recom": "Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado."
    }

st.title("🎓 Compilador Científico de Élite - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático Avanzado")
    
    st.markdown("### I. Desarrollo Teórico")
    raw_contenido = st.text_area("Pegue el contenido de Mathpix aquí:", height=250, 
                                 placeholder="Al pegar, el sistema organizará los párrafos automáticamente...")
    
    # Procesamos el contenido pegado para que no sea una sola línea
    contenido = procesar_parrafos(raw_contenido)

    st.markdown("---")
    st.subheader("📊 Motor Gráfico")
    func_in = st.text_input("Función f(x):", "np.cos(x) * np.exp(-x/5)")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-5, 15, 500)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2)
        ax.set_title(f"Representación Gráfica: {titulo}", fontsize=10)
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: st.warning("Ingrese una expresión matemática válida.")

    ejercicios = st.text_area("📝 Guía de Ejercicios:", "1. Demuestre la convergencia...")

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_profesionales(titulo)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>{firma_oficial}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. Introducción"); st.write(textos['intro'])
        
        st.markdown("### II. Desarrollo Teórico")
        if contenido:
            # Dividimos para mostrar LaTeX correctamente por bloques
            partes = contenido.split('\n\n')
            for p in partes:
                if '$' in p or '\\' in p: st.latex(p.replace('$', ''))
                else: st.write(p)
        else: st.info("El desarrollo aparecerá aquí.")
        
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)
        st.markdown("### III. Ejercicios Propuestos"); st.write(ejercicios)
        st.markdown("### IV. Conclusiones"); st.write(textos['conclu'])
        st.markdown("### V. Recomendaciones"); st.write(textos['recom'])

# --- GENERACIÓN DE DOCUMENTACIÓN ---
if st.button("🚀 Compilar Word y LaTeX"):
    doc = Document()
    
    # 1. Foto Circular y Fecha
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p_h = header.paragraphs[0]; p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto = preparar_foto_circular('perfil.png')
    if foto: p_h.add_run().add_picture(foto, width=Inches(0.8))
    p_h.add_run(f"\nFecha: {fecha_actual}").bold = True

    # 2. Título y Firma
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_oficial).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 3. Secciones con Párrafos Correctos
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    
    doc.add_heading('II. Desarrollo Teórico', 1)
    # Insertamos párrafo por párrafo para evitar la línea única en Word
    for p in contenido.split('\n\n'):
        if p.strip():
            doc.add_paragraph(p.strip())
    
    if buf_graf.getbuffer().nbytes > 0: doc.add_picture(buf_graf, width=Inches(4.5))
        
    doc.add_heading('III. Ejercicios Propuestos', 1); doc.add_paragraph(ejercicios)
    doc.add_heading('IV. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('V. Recomendaciones', 1); doc.add_paragraph(textos['recom'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.success("¡Documento procesado con párrafos correctos!")
