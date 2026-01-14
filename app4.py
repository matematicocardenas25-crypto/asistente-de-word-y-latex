import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import json
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD (DEFINICIÓN ABSOLUTA) ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    mes_nombre = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {mes_nombre}, {ahora.year}"

# Variables Globales de Identidad para evitar NameError
fecha_actual = obtener_fecha_espanol()
firma_linea1 = "Ismael Antonio Cardenas López"
firma_linea2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA (ROBUSTO) ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. MOTOR DE LIMPIEZA DE LATEX PARA WORD ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Eliminar delimitadores de ecuación y puntos suspensivos de LaTeX
    texto = texto.replace("$", "").replace(r"\dots", "...").replace(r"\cdots", "...")
    # Reemplazos de comandos comunes
    reemplazos = {
        r"\\left(": "(", r"\\right)": ")", r"\\left[": "[", r"\\right]": "]",
        r"\\infty": "infinito", r"\\times": "x", r"\\cdot": "·", r"\\": "", r"\,": " "
    }
    # Traducir fracciones \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # Eliminar cualquier comando \comando{...} restante
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

# --- 5. LÓGICA DE INTERFAZ Y PERSISTENCIA ---
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
    st.session_state.contenido = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.contenido, height=350)
    
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
        st.markdown("### 2. Desarrollo")
        st.markdown(st.session_state.contenido)
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)

# --- 6. GENERACIÓN DE DOCUMENTOS ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    doc = Document()
    
    # Encabezado: Fecha y Foto Circular (Solo primera página)
    header_table = doc.add_table(rows=1, cols=2)
    header_table.columns[0].width = Inches(4.5)
    header_table.cell(0, 0).text = fecha_actual
    
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(1.0))

    # Título y Firma centrada
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1 = doc.add_paragraph(firma_line1)
    f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2 = doc.add_paragraph(firma_line2)
    f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2.runs[0].font.italic = True

    # Secciones Combinadas (Automáticas + Usuario) con Limpieza
    secciones_finales = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios Propuestos", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    for tit, cont in secciones_finales:
        doc.add_heading(tit, 1)
        # Limpieza profunda de LaTeX para que el Word sea elegante
        texto_limpio = limpiar_para_word(cont)
        for linea in texto_limpio.split('\n'):
            if linea.strip(): doc.add_paragraph(linea.strip())

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX (Se mantiene con toda la robustez de fórmulas)
    latex_code = f"\\documentclass{{article}}\\usepackage[spanish]{{babel}}\\title{{{titulo_proy}}}\\author{{{firma_line1} \\\\ {firma_line2}}}\\begin{{document}}\\maketitle\n\\section{{I. Introducción}}{textos['intro']}\n\\section{{II. Desarrollo}}{st.session_state.contenido}\n\\section{{III. Conclusiones}}{textos['conclu']}\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar Código LaTeX", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documentación compilada con éxito!")
