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

# --- PROCESADOR DE TEXTO CORREGIDO (MANTIENE PÁRRAFOS SEPARADOS) ---
def procesar_parrafos_fiel(texto):
    if not texto: return ""
    # Esta versión respeta los saltos de línea dobles que separan párrafos
    parrafos = texto.split('\n')
    texto_final = ""
    for linea in parrafos:
        if linea.strip() == "":
            texto_final += "\n\n" # Mantiene el espacio entre párrafos
        else:
            texto_final += linea + " "
    return texto_final

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

# --- GENERADOR DE CONTENIDO PROFESIONAL ---
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
    raw_contenido = st.text_area("Contenido (Texto y LaTeX):", height=300, 
                                 placeholder="Pegue aquí el contenido. Use doble intro para separar párrafos.")
    
    # Aplicamos la nueva función que sí respeta párrafos
    contenido_listo = procesar_parrafos_fiel(raw_contenido)

    st.markdown("---")
    st.subheader("📊 Motor Gráfico Avanzado")
    func_in = st.text_input("Defina la función f(x) o código matemático:", "np.cos(x) * np.exp(-x/5)")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-5, 15, 500)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2, label=f"f(x) = {func_in}")
        ax.set_title(f"Análisis Gráfico: {titulo}", fontsize=10)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: st.warning("Esperando expresión matemática válida para graficar...")

    st.markdown("### II. Ejercicios Propuestos")
    ejercicios_raw = st.text_area("Lista de Ejercicios:", height=200, placeholder="Ejercicio 1...\n\nEjercicio 2...")
    ejercicios_listos = procesar_parrafos_fiel(ejercicios_raw)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_profesionales(titulo)
    with st.container(border=True):
        # Encabezado corregido
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#003366;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><i>{firma_oficial}</i></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Introducción
        st.markdown("### I. Introducción")
        st.write(textos['intro'])
        
        # Desarrollo Teórico con separación real
        st.markdown("### II. Desarrollo Teórico")
        if contenido_listo:
            # Usamos markdown directo para que reconozca los saltos de línea \n\n
            st.markdown(contenido_listo)
        else:
            st.info("El desarrollo se visualizará aquí con sus párrafos separados.")
        
        # Espacio para Gráfica
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización Generada por el Motor Matemático")
        
        # Ejercicios con separación real
        st.markdown("### III. Ejercicios Propuestos")
        if ejercicios_listos:
            st.markdown(ejercicios_listos)
        
        # Cierre
        st.markdown("---")
        st.markdown("#### IV. Conclusiones")
        st.write(textos['conclu'])
        st.markdown("#### V. Recomendaciones")
        st.write(textos['recom'])

# --- GENERACIÓN DE DOCUMENTOS (WORD Y LATEX) ---
if st.button("🚀 Compilar Documentación Final"):
    # --- WORD ---
    doc = Document()
    # Configuración de página y encabezado (Mantiene tu foto circular)
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p_h = header.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto = preparar_foto_circular('perfil.png')
    if foto: p_h.add_run().add_picture(foto, width=Inches(0.8))
    p_h.add_run(f"\nFecha: {fecha_actual}").bold = True

    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_oficial).alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('I. Introducción', 1)
    doc.add_paragraph(textos['intro'])

    doc.add_heading('II. Desarrollo Teórico', 1)
    # El Word ahora también recibe los párrafos separados
    for p in raw_contenido.split('\n\n'):
        if p.strip(): doc.add_paragraph(p.strip())
    
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5))
        
    doc.add_heading('III. Ejercicios Propuestos', 1)
    for p in ejercicios_raw.split('\n\n'):
        if p.strip(): doc.add_paragraph(p.strip())

    w_io = io.BytesIO()
    doc.save(w_io)
    w_io.seek(0)
    
    # --- LATEX ---
    latex_code = f"""
\\documentclass[12pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, graphicx}}
\\title{{{titulo}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{I. Introducción}} {textos['intro']}
\\section{{II. Desarrollo Teórico}} 
{raw_contenido}
\\section{{III. Ejercicios Propuestos}}
{ejercicios_raw}
\\end{{document}}
"""
    l_io = io.StringIO(latex_code)

    st.download_button("⬇️ Descargar Word (.docx)", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar Código LaTeX (.tex)", l_io.getvalue(), f"{titulo}.tex")
    st.success("¡Documentos generados con éxito!")
