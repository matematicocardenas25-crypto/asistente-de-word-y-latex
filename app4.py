import streamlit as st
from PIL import Image, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

# --- DATOS DE IDENTIDAD ---
fecha_actual = datetime.now().strftime("%d de %B, %Y")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

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
    except:
        return None

# --- GENERADOR DE CONTENIDO MATEMÁTICO ROBUSTO ---
def generar_textos_profesionales(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Bajo la autoría del Lic. Cárdenas López, este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}, buscando establecer un nexo entre la teoría pura y la modelación aplicada.",
        "conclu": f"Tras el estudio exhaustivo de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos. Se confirma que la rigurosidad en la formulación es el pilar fundamental para la interpretación de resultados en el campo de las matemáticas superiores.",
        "recom": "Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado. Asimismo, se sugiere la extensión de este análisis a modelos dinámicos de mayor complejidad para validar las tendencias observadas en este estudio."
    }

st.title("🎓 Compilador Científico de Élite - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático Avanzado")
    
    st.markdown("### I. Desarrollo Teórico")
    contenido = st.text_area("Contenido (Texto o LaTeX):", height=150, 
                             placeholder="Escriba el desarrollo o pegue el código de Mathpix...")
    
    st.markdown("---")
    st.subheader("📊 Motor Gráfico Universal")
    func_in = st.text_input("Función f(x) (Ej: np.sin(x)*np.exp(-0.1*x)):", "np.cos(x) * np.exp(-x/5)")
    
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x_vals = np.linspace(-5, 15, 500)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y_vals, color='#003366', linewidth=2, label=f"f(x)={func_in}")
        ax.set_title(f"Representación Gráfica: {titulo}", fontsize=10)
        ax.axhline(0, color='black', lw=1); ax.axvline(0, color='black', lw=1)
        ax.grid(True, alpha=0.3); ax.legend()
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig); buf_graf.seek(0)
    except:
        st.warning("Ingrese una expresión matemática válida.")

    st.markdown("---")
    ejercicios = st.text_area("📝 Guía de Ejercicios:", "1. Demuestre la convergencia de la serie...\n2. Evalúe la integral de contorno...")

with col_pre:
    st.subheader("👁️ Vista Previa del Manuscrito")
    textos = generar_textos_profesionales(titulo)
    with st.container(border=True):
        # Encabezado con fecha
        st.markdown(f"<div style='text-align: right;'><b>León, Nicaragua</b><br>{fecha_actual}</div>", unsafe_allow_html=True)
        
        # Título y Firma
        st.markdown(f"<h1 style='text-align:center;'>{titulo}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color: #555;'>{firma_oficial}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Secciones completas
        st.markdown("### I. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### II. Desarrollo Teórico")
        if contenido:
            try: st.latex(contenido)
            except: st.write(contenido)
        else: st.info("El desarrollo aparecerá aquí.")
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Figura 1: Análisis visual del modelo.")
            
        st.markdown("### III. Ejercicios Propuestos")
        st.write(ejercicios)
        
        st.markdown("### IV. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("### V. Recomendaciones")
        st.write(textos['recom'])

# --- GENERACIÓN DE DOCUMENTACIÓN ---
if st.button("🚀 Compilar Word y LaTeX"):
    doc = Document()
    
    # Encabezado (Foto y Fecha)
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    p_h = header.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    foto = preparar_foto_circular('perfil.png')
    if foto:
        p_h.add_run().add_picture(foto, width=Inches(0.8))
    p_h.add_run(f"\nFecha: {fecha_actual}").bold = True

    # Título y Firma Oficial
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    firma_para = doc.add_paragraph(firma_oficial)
    firma_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    firma_para.runs[0].font.size = Pt(12)

    # Cuerpo del documento con lenguaje robusto
    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo Teórico', 1); doc.add_paragraph(contenido)
    
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))
        
    doc.add_heading('III. Ejercicios Propuestos', 1); doc.add_paragraph(ejercicios)
    doc.add_heading('IV. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('V. Recomendaciones', 1); doc.add_paragraph(textos['recom'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX Sincronizado
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath,graphicx,amssymb}}
\\title{{\\textbf{{{titulo}}}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Desarrollo Teórico}} {contenido}
\\section{{Ejercicios}} {ejercicios}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX Pro", latex_str, f"{titulo}.tex")
    st.success("¡Documentación técnica generada con éxito!")
