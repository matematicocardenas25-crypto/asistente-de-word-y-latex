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

# --- CONFIGURACIÓN DE IDENTIDAD Y FECHA ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    nombre_mes = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {nombre_mes}, {ahora.year}"

# Variables Globales de Identidad
fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- MOTOR DE LIMPIEZA PROFUNDA (ELIMINA LATEX EN WORD) ---
def limpiar_texto_word(texto):
    if not texto: return ""
    # 1. Reemplazos de símbolos matemáticos comunes a texto plano
    reemplazos = {
        r"\\left\( ": "(", r"\\right\)": ")", r"\\left\[": "[", r"\\right\]": "]",
        r"\\dots": "...", r"\\cdots": "...", r"\\alpha": "alpha", r"\\beta": "beta",
        r"\\theta": "theta", r"\\infty": "infinito", r"\\times": "x", r"\\cdot": "·",
        r"\$": "", r"\_": "_", r"\\": ""
    }
    # 2. Traducir fracciones: \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # 3. Quitar comandos de formato: \textbf{texto} -> texto
    texto = re.sub(r'\\[a-zA-Z]+\{(.*?)\}', r'\1', texto)
    # 4. Aplicar los reemplazos de la lista
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    return texto.strip()

# --- GENERADOR DE IMAGEN CIRCULAR ---
def obtener_foto_circular():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        # Genera un círculo elegante si no encuentra el archivo
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    
    size = (400, 400)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- PERSISTENCIA Y PANEL (Sin quitar nada) ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Respaldo")
    if st.button("📥 Crear Punto de Restauración"):
        data_respaldo = {"titulo": "Proyecto", "contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
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
        ax.grid(True, linestyle='--', alpha=0.6)
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: pass
    
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=200)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        # CORRECCIÓN DEL ERROR DE VARIABLE:
        st.markdown(f"<p style='text-align:center;'><i>{firma_line1}<br>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(st.session_state.contenido)
        if buf_graf.getbuffer().nbytes > 0:
            st.image(buf_graf)

# --- GENERACIÓN DE DOCUMENTACIÓN ---
if st.button("🚀 Compilar Documentación de Élite"):
    # 1. WORD (Limpio de LaTeX y con foto circular)
    doc = Document()
    
    # Encabezado: Foto a la derecha y Fecha
    encabezado = doc.add_table(rows=1, cols=2)
    encabezado.columns[0].width = Inches(4.5)
    
    p_fecha = encabezado.cell(0, 0).add_paragraph(fecha_actual)
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    celda_foto = encabezado.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_foto = celda_foto.add_run()
    run_foto.add_picture(obtener_foto_circular(), width=Inches(1.1))

    # Título y Firma
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1 = doc.add_paragraph(firma_line1)
    f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2 = doc.add_paragraph(firma_line2)
    f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2.runs[0].font.italic = True

    # Secciones Limpias
    for t, c in [("I. Contenido Analítico", st.session_state.contenido), ("II. Ejercicios", st.session_state.ejercicios)]:
        doc.add_heading(t, 1)
        texto_limpio = limpiar_texto_word(c)
        for p in texto_limpio.split('\n'):
            if p.strip(): doc.add_paragraph(p.strip())

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # 2. LATEX (Original para mantener fórmulas perfectas)
    latex_code = f"\\documentclass{{article}}\n\\usepackage[spanish]{{babel}}\n\\title{{{titulo_proy}}}\n\\author{{{firma_line1} \\\\ {firma_line2}}}\n\\date{{{fecha_actual}}}\n\\begin{{document}}\n\\maketitle\n{st.session_state.contenido}\n\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word (Sin símbolos LaTeX)", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar LaTeX (Original)", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documentación corregida y lista para descargar!")
