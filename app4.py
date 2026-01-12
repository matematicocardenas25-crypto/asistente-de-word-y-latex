import streamlit as st
from pix2tex.cli import LatexOCR
from PIL import Image, ImageOps, ImageDraw
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import os

st.set_page_config(page_title="Calculo Pro: Compilador Científico", layout="wide")

def hacer_circulo(imagen_path):
    try:
        img = Image.open(imagen_path).convert("RGBA")
        ancho, alto = img.size
        min_dim = min(ancho, alto)
        img = img.crop(((ancho - min_dim) // 2, (alto - min_dim) // 2, (ancho + min_dim) // 2, (alto + min_dim) // 2))
        mascara = Image.new('L', (min_dim, min_dim), 0)
        dibujo = ImageDraw.Draw(mascara)
        dibujo.ellipse((0, 0, min_dim, min_dim), fill=255)
        resultado = ImageOps.fit(img, mascara.size, centering=(0.5, 0.5))
        resultado.putalpha(mascara)
        buf = io.BytesIO()
        resultado.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except:
        return None

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📋 Configuración")
    titulo = st.text_input("Título del Proyecto", "Análisis de Funciones y Cálculo Diferencial")
    autor_predeterminado = "Ismael Antonio Cárdenas, Licenciado en Matemáticas, UNAN-León, Nicaragua"
    autor = st.text_input("Autor del Proyecto", autor_predeterminado)
    st.info("Sube 'perfil.jpeg' para ver tu foto en la portada.")

st.title("🎓 Compilador Educativo: Vista Previa Científica")

# LÓGICA DE TEXTOS CIENTÍFICOS AUTOMATIZADOS (Se definen arriba para usarlos en la vista previa)
intro_gen = f"La presente investigación técnica, centrada en el estudio de '{titulo}', constituye una aproximación formal a las estructuras matemáticas contemporáneas. Bajo la autoría del {autor}, este documento sistematiza los principios teóricos fundamentales y su correlación con la fenomenología gráfica, garantizando un rigor deductivo en la transición de la abstracción analítica a la representación digital."
conclu_gen = f"Tras el análisis riguroso de '{titulo}', se establece que la convergencia entre el cálculo simbólico y la visualización paramétrica permite una comprensión holística de los puntos críticos y el comportamiento asintótico."
recom_gen = f"Para optimizar el proceso de aprendizaje vinculado a '{titulo}', se recomienda al investigador un contraste dialéctico entre los algoritmos computacionales y los métodos de demostración clásica."

# --- DISEÑO DE COLUMNAS PARA ENTRADA ---
col_input, col_preview = st.columns([1, 1.2])

with col_input:
    st.subheader("🛠️ Entrada de Datos")
    
    # 1. OCR
    uploaded_file = st.file_uploader("1. Sube el ejercicio resuelto", type=["png", "jpg", "jpeg"])
    latex_res = ""
    if uploaded_file:
        img = Image.open(uploaded_file)
        model = LatexOCR()
        latex_res = model(img)
    
    # 2. Gráfica
    func_input = st.text_input("2. Función matemática:", "np.cos(x)")
    buf_graf = io.BytesIO()
    try:
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = eval(func_input.replace('^', '**'), {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x_vals, y_vals, color='blue', linewidth=2)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        fig.savefig(buf_graf, format='png')
        buf_graf.seek(0)
    except:
        st.warning("Escribiendo función...")

    # 3. Ejercicios
    texto_ejercicios = st.text_area("3. Enunciados (Escribe 'Fuente: Stewart'):", 
                                    "1. Calcule la derivada según Stewart.\n2. Determine puntos críticos (Fuente: Larson).")
    
    img_ejercicios = st.file_uploader("4. Capturas de apoyo", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    list_img_buf = []
    if img_ejercicios:
        for file in img_ejercicios:
            img_p = Image.open(file)
            b = io.BytesIO(); img_p.save(b, format="PNG"); b.seek(0)
            list_img_buf.append(b)

with col_preview:
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        # Simulación de la hoja
        st.markdown(f"<div style='text-align: right;'><b>{autor}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{titulo}</h1>", unsafe_allow_html=True)
        
        st.markdown("### 1. Introducción Formal")
        st.write(intro_gen)
        
        st.markdown("### 2. Desarrollo y Gráfica")
        if latex_res: st.latex(latex_res)
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf, use_container_width=True)
        
        st.markdown("### 3. Ejercicios Propuestos")
        st.write(texto_ejercicios)
        
        st.markdown("---")
        st.caption("Nota: Las conclusiones y bibliografía se generan automáticamente en el archivo final.")

# --- BOTONES DE DESCARGA ---
st.divider()
if st.button("🚀 Compilar y Generar Archivos Finales (Word & LaTeX)"):
    # Lógica de bibliografía
    fuentes_db = {
        "stewart": "Stewart, J. (2015). Cálculo de una variable: Trascendentes tempranas. Cengage Learning.",
        "larson": "Larson, R., & Edwards, B. H. (2017). Cálculo (11a ed.). Cengage Learning.",
        "leithold": "Leithold, L. (1998). El Cálculo (7a ed.). Oxford University Press.",
        "piskunov": "Piskunov, N. (1977). Cálculo Diferencial e Integral. Editorial Mir.",
        "spivak": "Spivak, M. (2006). Calculus (3ra ed.). Reverté."
    }
    bib_detectada = [cita for clave, cita in fuentes_db.items() if clave in texto_ejercicios.lower()]
    if not bib_detectada: bib_detectada.append("Recursos digitales generados mediante Asistente de IA Matemática.")

    # --- GENERACIÓN WORD ---
    doc = Document()
    seccion = doc.sections[0]
    seccion.different_first_page_header_footer = True
    header = seccion.first_page_header
    p_h = header.paragraphs[0]; p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_circ = hacer_circulo('perfil.jpeg')
    if f_circ: p_h.add_run().add_picture(f_circ, width=Inches(1.2))
    
    doc.add_heading(titulo, 0)
    doc.add_paragraph(f"Elaborado por: {autor}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading('Introducción Formal', 1); doc.add_paragraph(intro_gen)
    doc.add_heading('Análisis Matemático', 1); doc.add_paragraph(latex_res)
    doc.add_picture(buf_graf, width=Inches(5))
    doc.add_heading('Consolidación Práctica', 1); doc.add_paragraph(texto_ejercicios)
    for b_img in list_img_buf: doc.add_picture(b_img, width=Inches(4))
    doc.add_heading('Conclusiones Académicas', 1); doc.add_paragraph(conclu_gen)
    doc.add_heading('Recomendaciones Metodológicas', 1); doc.add_paragraph(recom_gen)
    doc.add_page_break(); doc.add_heading('Referencias Bibliográficas (APA)', 1)
    for cita in bib_detectada: doc.add_paragraph(cita)
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)

    # --- GENERACIÓN LATEX ---
    citas_latex = "\\begin{itemize}\n" + "\n".join([f"\\item {c}" for c in bib_detectada]) + "\n\\end{itemize}"
    latex_file = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, graphicx, tikz}}
\\begin{{document}}
\\begin{{tikzpicture}}[remember picture,overlay]
\\node[anchor=north east, xshift=-1cm, yshift=-1.5cm] at (current page.north east) {{
    \\begin{{tikzpicture}} \\clip [circle] (0,0) circle (1.5cm); \\node at (0,0) {{\\includegraphics[width=3cm]{{perfil.jpeg}}}}; \\end{{tikzpicture}}
}};
\\end{{tikzpicture}}
\\title{{\\textbf{{{titulo}}}}} \\author{{Elaborado por: \\\\ {autor}}} \\maketitle
\\section{{Introducción Formal}} {intro_gen}
\\section{{Análisis Técnico}} $ {latex_res} $ 
\\section{{Consolidación Práctica}} {texto_ejercicios.replace('\\n', ' \\\\ ')}
\\section{{Conclusiones}} {conclu_gen}
\\newpage
\\section{{Bibliografía (APA)}} {citas_latex}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word", w_io, f"{titulo}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_file, f"{titulo}.tex")
