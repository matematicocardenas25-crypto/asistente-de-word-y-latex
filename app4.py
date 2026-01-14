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

# --- 1. CONFIGURACIÓN DE IDENTIDAD (DEFINICIÓN INICIAL PARA EVITAR NAMEERROR) ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    nombre_mes = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {nombre_mes}, {ahora.year}"

# Variables de firma obligatorias (Globales)
fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE LIMPIEZA TOTAL (ELIMINA LATEX EN WORD) ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Eliminar símbolos de dólar y puntos de LaTeX que se ven en las capturas
    texto = texto.replace("$", "")
    texto = texto.replace(r"\dots", "...")
    texto = texto.replace(r"\cdots", "...")
    texto = texto.replace(r"\,", " ")
    
    # Reemplazar comandos de formato matemático comunes por texto legible
    reemplazos = {
        r"\\left(": "(", r"\\right)": ")", 
        r"\\left[": "[", r"\\right]": "]",
        r"\\infty": "infinito", r"\\times": "x", 
        r"\\cdot": "·", r"\\": ""
    }
    
    # Traducir fracciones \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # Traducir exponentes básicos a^b -> a^b (sin llaves)
    texto = re.sub(r'\^\{(.*?)\}', r'^\1', texto)
    # Eliminar comandos restantes de barra invertida
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
        
    return texto.strip()

# --- 3. GESTIÓN DE IMAGEN CIRCULAR ---
def preparar_foto_circular():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        # Círculo azul profesional si no hay archivo
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    
    mask = Image.new('L', (400, 400), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- 4. PERSISTENCIA Y UI ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Gestión de Datos")
    if st.button("📥 Crear Punto de Restauración"):
        data = {"contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo", json.dumps(data), "respaldo_ismael.json")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    st.session_state.contenido = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=200)

with col_pre:
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        # Aquí se usa el nombre correcto de las variables definidas arriba
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(st.session_state.contenido)

# --- 5. COMPILACIÓN DE DOCUMENTOS ---
if st.button("🚀 Compilar Documentación de Élite"):
    # --- WORD ---
    doc = Document()
    
    # Encabezado: Fecha a la izquierda, Foto a la derecha
    header_table = doc.add_table(rows=1, cols=2)
    header_table.columns[0].width = Inches(4.5)
    header_table.cell(0, 0).text = fecha_actual
    
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(1.0))

    # Título y Firma
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1 = doc.add_paragraph(firma_line1)
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2 = doc.add_paragraph(firma_line2)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.runs[0].font.italic = True

    # Secciones con LIMPIEZA DE LATEX
    for t, c in [("I. Contenido", st.session_state.contenido), ("II. Ejercicios", st.session_state.ejercicios)]:
        doc.add_heading(t, 1)
        texto_limpio = limpiar_para_word(c)
        for linea in texto_limpio.split('\n'):
            if linea.strip(): doc.add_paragraph(linea.strip())

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # --- LATEX (Se mantiene original) ---
    latex_code = f"\\documentclass{{article}}\\usepackage[spanish]{{babel}}\\title{{{titulo_proy}}}\\author{{{firma_line1} \\\\ {firma_line2}}}\\begin{{document}}\\maketitle\n{st.session_state.contenido}\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar LaTeX", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documento procesado con éxito!")
