import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

# --- CONFIGURACIÓN DE IDENTIDAD ---
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# Función para procesar tu foto de perfil de forma circular
def preparar_foto_circular(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        min_dim = min(img.size)
        img = img.crop(((img.width - min_dim) // 2, (img.height - min_dim) // 2, (img.width + min_dim) // 2, (img.height + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        ImageDraw.Draw(mascara).ellipse((0, 0, min_dim, min_dim), fill=255)
        img.putalpha(mascara)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except:
        return None

# Textos Académicos Robustos
def generar_textos(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. Cárdenas López, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos.",
        "recom": "Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado."
    }

st.title("🎓 Compilador Científico Profesional")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Entrada de Datos")
    titulo = st.text_input("Título del Proyecto", "Análisis de Modelos Matemáticos")
    
    st.markdown("### I. Desarrollo Teórico")
    contenido = st.text_area("Pegue aquí el texto o código LaTeX de su captura:", height=150, 
                             placeholder="Ejemplo: \\frac{d}{dx} e^x = e^x")
    
    st.markdown("---")
    st.subheader("📊 Gráfica Universal (Física/Estadística)")
    func_in = st.text_input("Defina f(x) (Use np. para funciones):", "np.sin(x) / x")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-10, 10, 400)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2)
        ax.set_title(f"Gráfica de {titulo}")
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except:
        st.caption("Esperando función válida...")

    st.markdown("---")
    ejercicios = st.text_area("📝 Ejercicios Propuestos:", "1. Resuelva la integral definida...")

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos(titulo)
    with st.container(border=True):
        # Encabezado simulado
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>{firma_oficial}</p>", unsafe_allow_html=True)
        
        st.markdown("#### Introducción")
        st.write(textos['intro'])
        
        st.markdown("#### Desarrollo y Fórmulas")
        if contenido:
            try:
                st.latex(contenido) # Intenta dibujar la matemática
            except:
                st.write(contenido)
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Visualización Analítica HD")

# --- GENERACIÓN DE ARCHIVOS ---
if st.button("🚀 Compilar Word y LaTeX"):
    doc = Document()
    
    # Encabezado: Foto Circular y Fecha
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p_h = header.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto = preparar_foto_circular('perfil.png')
    if foto:
        p_h.add_run().add_picture(foto, width=Inches(0.8))
    p_h.add_run(f"\nFecha: {fecha_actual}").bold = True

    # Título y Firma
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f = doc.add_paragraph(firma_oficial)
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f.runs[0].font.size = Pt(12)

    # Secciones
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo Teórico', 1); doc.add_paragraph(contenido)
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
    doc.add_heading('III. Ejercicios Propuestos', 1); doc.add_paragraph(ejercicios)
    doc.add_heading('IV. Conclusiones', 1); doc.add_paragraph(textos['conclu'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX
    latex_str = f"\\documentclass{{article}}\\usepackage[utf8]{{inputenc}}\\usepackage{{amsmath,graphicx}}\\title{{{titulo}}}\\author{{{firma_oficial}}}\\date{{{fecha_actual}}}\\begin{{document}}\\maketitle\\section{{Introducción}}{textos['intro']}\\section{{Teoría}}{contenido}\\section{{Ejercicios}}{ejercicios}\\section{{Conclusiones}}{textos['conclu']}\\end{{document}}"

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Prueba superada! Archivos generados.")
