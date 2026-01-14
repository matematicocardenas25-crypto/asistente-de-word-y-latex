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
    mes = meses.get(ahora.strftime("%B"), ahora.strftime("%B"))
    return f"{ahora.day} de {mes}, {ahora.year}"

# Variables de identidad (Definidas al inicio para evitar NameError)
fecha_actual = obtener_fecha_espanol()
firma_linea1 = "Ismael Antonio Cardenas López"
firma_linea2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- MOTOR DE LIMPIEZA SUPREMA PARA WORD ---
def limpiar_para_word_elegante(texto):
    if not texto: return ""
    # 1. Eliminar símbolos de dólar de LaTeX
    texto = texto.replace("$", "")
    # 2. Traducir comandos matemáticos a texto legible
    reemplazos = {
        r"\dots": "...", 
        r"\cdots": "...", 
        r"\alpha": "alpha", 
        r"\beta": "beta",
        r"\infty": "infinito",
        r"\\": "",
        r"\{": "{",
        r"\}": "}",
        r"\left": "",
        r"\right": ""
    }
    # Traducir fracciones \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # Eliminar cualquier comando de barra invertida restante
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    # Limpiar espacios extra
    return texto.strip()

# --- GENERADOR DE IMAGEN CIRCULAR ---
def preparar_foto_circular():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        # Si no hay foto, crea un círculo institucional elegante
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

# --- INTERFAZ STREAMLIT ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Gestión de Datos")
    if st.button("📥 Punto de Restauración"):
        data = {"contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo", json.dumps(data), "respaldo.json")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    st.session_state.contenido = st.text_area("Desarrollo Teórico:", value=st.session_state.contenido, height=300)
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=200)

with col_pre:
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(st.session_state.contenido)

# --- GENERACIÓN DE DOCUMENTACIÓN ---
if st.button("🚀 Compilar Documentación de Élite"):
    # --- 1. PROCESO WORD ---
    doc = Document()
    
    # Encabezado (Foto y Fecha)
    tabla_enc = doc.add_table(rows=1, cols=2)
    tabla_enc.columns[0].width = Inches(4.5)
    
    p_fecha = tabla_enc.cell(0, 0).add_paragraph(fecha_actual)
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    p_img = tabla_enc.cell(0, 1).add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_img.add_run().add_picture(preparar_foto_circular(), width=Inches(1.1))

    # Título y Firma
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    f1 = doc.add_paragraph(firma_line1)
    f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2 = doc.add_paragraph(firma_line2)
    f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f2.runs[0].font.italic = True

    # Secciones con limpieza aplicada
    for tit, cont in [("Desarrollo Teórico", st.session_state.contenido), ("Ejercicios", st.session_state.ejercicios)]:
        doc.add_heading(tit, 1)
        # LIMPIEZA CRUCIAL PARA WORD
        cont_limpio = limpiar_para_word_elegante(cont)
        for linea in cont_limpio.split('\n'):
            if linea.strip(): doc.add_paragraph(linea.strip())

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # --- 2. PROCESO LATEX ---
    latex_code = f"""
\\documentclass{{article}}
\\usepackage[spanish]{{babel}}
\\title{{{titulo_proy}}}
\\author{{{firma_line1} \\\\ {firma_line2}}}
\\date{{{fecha_actual}}}
\\begin{{document}}
\\maketitle
{st.session_state.contenido}
\\end{{document}}
"""
    
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar LaTeX (Original)", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documentación compilada con éxito y sin errores!")
