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

# --- CONFIGURACIÓN DE IDENTIDAD ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
# Firma en dos líneas como solicitado
firma_linea1 = "Ismael Antonio Cardenas López"
firma_linea2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- MOTOR DE LIMPIEZA DE LATEX PARA WORD ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Traducir fracciones de LaTeX a formato texto legible: \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # Limpiar comandos de formato y símbolos comunes
    reemplazos = {
        "\\left(": "(", "\\right)": ")", "\\left[": "[", "\\right]": "]",
        "\\dots": "...", "\\cdots": "...", "\\times": "x", "\\cdot": "·",
        "\\infty": "∞", "$": "", "\\": ""
    }
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    # Eliminar cualquier comando restante tipo \comando{...}
    texto = re.sub(r'\\[a-zA-Z]+\{(.*?)\}', r'\1', texto)
    return texto.strip()

# --- GENERADOR DE IMAGEN CIRCULAR ---
def obtener_foto_circular():
    try:
        # Intenta cargar tu foto personal; si no, genera un círculo azul elegante
        img = Image.open("foto.png").convert("RGBA")
    except:
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

# --- LÓGICA DE LA PÁGINA (Sin quitar nada de lo anterior) ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Respaldo")
    if st.button("📥 Crear Punto de Restauración"):
        data = {"titulo": "Proyecto", "contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo (.json)", json.dumps(data), "respaldo_ismael.json")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    st.session_state.contenido = st.text_area("Cuerpo del Contenido:", value=st.session_state.contenido, height=300)
    
    st.subheader("📊 Gráfico")
    func_in = st.text_input("Función f(x):", "np.sin(x) * np.exp(-x/10)")
    buf_graf = io.BytesIO()
    try:
        x = np.linspace(-10, 20, 1000)
        y = eval(func_in, {"x": x, "np": np})
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(x, y, color='#1A5276', linewidth=2)
        ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png', dpi=200); plt.close(fig); buf_graf.seek(0)
    except: pass
    
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><i>{firma_line1}<br>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(st.session_state.contenido)

# --- GENERACIÓN DE WORD ---
if st.button("🚀 Compilar Documentación de Élite"):
    doc = Document()
    
    # 1. Foto Circular y Fecha (Solo primera página)
    header_table = doc.add_table(rows=1, cols=2)
    header_table.columns[0].width = Inches(4)
    header_table.columns[1].width = Inches(2)
    
    # Fecha a la izquierda del encabezado o derecha (según elegancia)
    p_fecha = header_table.cell(0, 0).add_paragraph(fecha_actual)
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Foto circular a la derecha
    celda_img = header_table.cell(0, 1).add_paragraph()
    celda_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_img = celda_img.add_run()
    run_img.add_picture(obtener_foto_circular(), width=Inches(1.1))

    # 2. Título y Firma centrada
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1 = doc.add_paragraph(firma_line1)
    f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1.runs[0].font.size = Pt(12)
    
    f2 = doc.add_paragraph(firma_line2)
    f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2.runs[0].font.italic = True
    f2.runs[0].font.size = Pt(11)

    # 3. Secciones con limpieza de LaTeX
    secciones = [
        ("I. Desarrollo Teórico", st.session_state.contenido),
        ("II. Ejercicios Propuestos", st.session_state.ejercicios)
    ]
    
    for tit, cont in secciones:
        doc.add_heading(tit, 1)
        texto_limpio = limpiar_para_word(cont)
        for linea in texto_limpio.split('\n'):
            if linea.strip(): doc.add_paragraph(linea.strip())

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    # Guardado y descarga
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LaTeX (Se mantiene intacto para conservar sus fórmulas)
    latex_code = f"\\documentclass{{article}}\n\\usepackage[spanish]{{babel}}\n\\title{{{titulo_proy}}}\n\\author{{{firma_line1} \\\\ {firma_line2}}}\n\\begin{{document}}\n\\maketitle\n{st.session_state.contenido}\n\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar Código LaTeX", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documento compilado con elegancia!")
