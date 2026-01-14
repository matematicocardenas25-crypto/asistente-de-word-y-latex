import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import matplotlib.pyplot as plt
import numpy as np
import io
import json
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    mes_nombre = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {mes_nombre}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. FUNCIONES DE DISEÑO PARA WORD ---
def aplicar_formato_cuadro(celda):
    """Aplica un sombreado gris tenue y bordes a una celda de tabla."""
    tc = celda._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), "F2F3F4")  # Gris muy claro
    tcPr.append(shd)
    
def limpiar_para_word(texto):
    if not texto: return ""
    texto = texto.replace("$", "").replace(r"\dots", "...").replace(r"\cdots", "...")
    # Reemplazo de items por viñetas profesionales (●)
    texto = texto.replace(r"\item", "● ")
    reemplazos = {
        r"\\left(": "(", r"\\right)": ")", r"\\left[": "[", r"\\right]": "]",
        r"\\infty": "infinito", r"\\times": "x", r"\\cdot": "·", r"\\": "", r"\,": " "
    }
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    texto = re.sub(r'\\[a-zA-Z]+\{(.*?)\}', r'\1', texto)
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    return texto.strip()

# --- 4. GESTIÓN DE IMAGEN CIRCULAR ---
def preparar_foto_circular():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- 5. LÓGICA DE STREAMLIT ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Respaldo de Seguridad")
    if st.button("📥 Crear Punto de Restauración"):
        data_respaldo = {"contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo (.json)", json.dumps(data_respaldo), "respaldo_ismael.json")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    st.session_state.contenido = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.contenido, height=350, placeholder="Escriba aquí sus Teoremas, Definiciones o Axiomas...")
    
    st.subheader("📊 Motor Gráfico")
    func_in = st.text_input("Función f(x):", "np.sin(x) * np.exp(-x/10)")
    buf_graf = io.BytesIO()
    try:
        x_vals = np.linspace(-10, 20, 1000)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x_vals, y_vals, color='#1A5276', linewidth=2)
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: pass
    
    st.session_state.ejercicios = st.text_area("Ejercicios Propuestos:", value=st.session_state.ejercicios, height=200)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 1. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### 2. Desarrollo Teórico")
        st.markdown(st.session_state.contenido)
        
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf, caption="Análisis Gráfico")
            
        st.markdown("### 3. Ejercicios Propuestos")
        st.markdown(st.session_state.ejercicios)
        
        st.markdown("### 4. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("### 5. Recomendaciones")
        st.write(textos['recom'])

# --- 6. GENERACIÓN DE DOCUMENTOS ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    doc = Document()
    
    # Encabezado: Foto y Fecha
    header_table = doc.add_table(rows=1, cols=2)
    header_table.columns[0].width = Inches(4.5)
    header_table.cell(0, 0).text = fecha_actual
    
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(1.0))

    # Título y Firma
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1 = doc.add_paragraph(firma_line1)
    f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2 = doc.add_paragraph(firma_line2)
    f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2.runs[0].font.italic = True

    secciones_word = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios Propuestos", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    palabras_clave = ["Teorema", "Axioma", "Lema", "Definición", "Ejercicio", "Ejemplo", "Solución", "Definicion", "Solucion"]

    for tit, cont in secciones_word:
        doc.add_heading(tit, 1)
        texto_limpio = limpiar_para_word(cont)
        
        for linea in texto_limpio.split('\n'):
            linea = linea.strip()
            if not linea: continue
            
            # Detectar si la línea empieza con una palabra clave para crear el cuadro
            if any(linea.startswith(pc) for pc in palabras_clave):
                tabla_box = doc.add_table(rows=1, cols=1)
                tabla_box.style = 'Table Grid'
                celda = tabla_box.rows[0].cells[0]
                aplicar_formato_cuadro(celda)
                p = celda.paragraphs[0]
                run = p.add_run(linea)
                run.bold = True
                run.font.color.rgb = RGBColor(26, 82, 118)
            else:
                p = doc.add_paragraph(linea)
                # Aplicar indentación si es una viñeta
                if linea.startswith("●"):
                    p.paragraph_format.left_indent = Inches(0.3)

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # Código LaTeX
    latex_code = f"\\documentclass{{article}}\\usepackage[spanish]{{babel}}\\usepackage{{tcolorbox}}\\title{{{titulo_proy}}}\\author{{{firma_line1} \\\\ {firma_line2}}}\\begin{{document}}\\maketitle\n\\section{{I. Introducción}}{textos['intro']}\\section{{II. Desarrollo}}{st.session_state.contenido}\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar Código LaTeX", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documentación de Élite compilada con éxito!")
