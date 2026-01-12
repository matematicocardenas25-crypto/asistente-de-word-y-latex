import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Compilador Ismael - UNAN León", layout="wide")
fecha_actual = datetime.now().strftime("%d de %B, %Y")

# --- TEXTOS ACADÉMICOS ROBUSTOS ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de las ciencias exactas. Este documento articula la abstracción algebraica con la fenomenología visual a fecha de {fecha_actual}, buscando cerrar la brecha entre la teoría pura y la aplicación práctica.",
        "conclu": f"Tras el estudio exhaustivo de los modelos presentados en '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los comportamientos analíticos analizados.",
        "recom": f"Se recomienda realizar un contraste crítico entre la resolución analítica manual y la verificación computacional presentada para consolidar el pensamiento lógico-matemático avanzado."
    }

# --- FUNCIÓN PARA IMAGEN CIRCULAR ---
def preparar_foto_circular(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        # Hacerla cuadrada
        ancho, alto = img.size
        min_dim = min(ancho, alto)
        img = img.crop(((ancho - min_dim) // 2, (alto - min_dim) // 2, (ancho + min_dim) // 2, (alto + min_dim) // 2))
        
        # Crear máscara circular
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

st.title("🎓 Sistema de Producción Científica - Ismael Cárdenas")
firma_oficial = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos del Proyecto")
    titulo = st.text_input("Título del Proyecto", "Análisis de Sucesiones y Series")
    
    # Espacio para pegar el contenido de las capturas
    texto_contenido = st.text_area("✍️ Pegue aquí el contenido de sus capturas:", height=200)
    
    # Gráfica HD
    st.markdown("---")
    func_in = st.text_input("📈 Función (ej: 1/n):", "1/x")
    buf_graf = io.BytesIO()
    try:
        plt.style.use('ggplot')
        x = np.linspace(1, 15, 50)
        y = eval(func_in.replace('^', '**'), {"x": x, "np": np})
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, 'o-', color='#003366', label=f'f(n) = {func_in}')
        ax.set_title(f"Gráfica HD: {titulo}")
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300)
        plt.close(fig)
        buf_graf.seek(0)
    except: pass

with col_pre:
    st.subheader("👁️ Vista Previa")
    textos = generar_textos_robustos(titulo)
    with st.container(border=True):
        st.write(f"**Fecha:** {fecha_actual}")
        st.write(f"**Firma:** {firma_oficial}")
        st.markdown(f"### {titulo}")
        st.write(texto_contenido)

# --- COMPILACIÓN ---
if st.button("🚀 Generar Documentos (Word & LaTeX)"):
    # 1. WORD
    doc = Document()
    
    # ENCABEZADO SOLO PRIMERA PÁGINA
    section = doc.sections[0]
    section.different_first_page_header_footer = True
    header = section.first_page_header
    
    # Agregar foto circular y fecha al encabezado de la primera página
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Intentar cargar 'perfil.png' o similar que tengas en tu GitHub
    foto_circ = preparar_foto_circular('perfil.png') 
    if foto_circ:
        p_head.add_run().add_picture(foto_circ, width=Inches(1))
    
    p_head.add_run(f"\nFecha: {fecha_actual}").bold = True

    # Título y Firma
    doc.add_heading(titulo, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    firma_p = doc.add_paragraph(firma_oficial)
    firma_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    firma_p.runs[0].font.size = Pt(12)

    doc.add_heading('I. Introducción', 1); doc.add_paragraph(textos['intro'])
    doc.add_heading('II. Desarrollo', 1); doc.add_paragraph(texto_contenido)
    
    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(4.5))

    doc.add_heading('III. Conclusiones', 1); doc.add_paragraph(textos['conclu'])
    doc.add_heading('IV. Recomendaciones', 1); doc.add_paragraph(textos['recom'])

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # 2. LATEX
    latex_str = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, fancyhdr}}
\\title{{\\textbf{{{titulo}}}}}
\\author{{{firma_oficial}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Desarrollo}} {texto_contenido}
\\section{{Conclusiones}} {textos['conclu']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Premium", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_str, f"{titulo}.tex")
    st.success("¡Documentos generados con éxito!")
