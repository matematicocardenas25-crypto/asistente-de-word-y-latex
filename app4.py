import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE ESTILIZADO ACADÉMICO (CUADROS ELEGANTES) ---
def renderizar_texto_estilizado(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        if not linea.strip(): continue
        
        # Detección de bloques por palabras clave
        if any(keyword in linea.upper() for keyword in ["TEOREMA", "PROPOSICIÓN", "LEMA"]):
            st.info(f"**📜 {linea}**")
        elif any(keyword in linea.upper() for keyword in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"**📘 {linea}**")
        elif any(keyword in linea.upper() for keyword in ["EJERCICIO", "PROBLEMA"]):
            st.warning(f"**✏️ {linea}**")
        elif "SOLUCIÓN" in linea.upper():
            st.markdown(f"**✅ {linea}**")
        else:
            st.markdown(linea)

# --- 3. MOTOR DE REDACCIÓN Y LIMPIEZA ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas bajo la autoría del Lic. Ismael Cárdenas López...",
        "conclu": "Se ratifica la importancia de la precisión axiomática en la resolución de problemas complejos y la modelización matemática avanzada.",
        "recom": "Se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados para futuras aplicaciones interdisciplinarias."
    }

def limpiar_para_word(texto):
    if not texto: return ""
    limpio = texto.replace("$", "").replace(r"\dots", "...").replace(r"\cdots", "...")
    limpio = limpio.replace(r"\left", "").replace(r"\right", "").replace(r"\,", " ")
    limpio = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', limpio)
    limpio = re.sub(r'\\([a-zA-Z]+)', r'\1', limpio)
    return limpio.replace("{", "").replace("}", "").strip()

# --- 4. PREPARACIÓN DE FOTO ---
def preparar_foto_circular():
    try: img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        ImageDraw.Draw(img).ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO(); output.save(buf, format='PNG'); buf.seek(0)
    return buf

# --- 5. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    titulo_proy = st.text_input("Título", "Sucesiones y Series parte 1")
    st.session_state.contenido = st.text_area("Desarrollo (LaTeX):", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Sección de Ejercicios:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.info(f"**1. Introducción**\n\n{textos['intro']}")
        renderizar_texto_estilizado(st.session_state.contenido)
        renderizar_texto_estilizado(st.session_state.ejercicios)

# --- 6. BOTONES DE DESCARGA ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    
    # WORD
    doc = Document()
    head = doc.add_table(rows=1, cols=2)
    head.cell(0,0).text = fecha_actual
    p_img = head.cell(0,1).add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_img.add_run().add_picture(preparar_foto_circular(), width=Inches(0.9))
    
    doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_line1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_line2).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    for t, c in [("I. Introducción", textos['intro']), ("II. Contenido Analítico", st.session_state.contenido), ("III. Ejercicios", st.session_state.ejercicios)]:
        doc.add_heading(t, 1)
        doc.add_paragraph(limpiar_para_word(c))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")

    # LATEX ROBUSTO
    latex_robust = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, amssymb, amsthm, amsfonts}}
\\usepackage{{tcolorbox}} % Cuadros elegantes
\\usepackage{{pgfplots}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}

\\newtcolorbox{{mybox}}[1]{{colback=blue!5!white,colframe=blue!75!black,fonttitle=\\bfseries,title=#1}}

\\title{{\\textbf{{{titulo_proy}}}}}
\\author{{{firma_line1} \\\\ \\small {firma_line2}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{textos['intro']}

\\begin{{mybox}}{{Desarrollo y Definiciones}}
{st.session_state.contenido}
\\end{{mybox}}

\\section{{Ejercicios}}
{st.session_state.ejercicios}

\\end{{document}}"""
    
    st.download_button("⬇️ Descargar LaTeX (Overleaf)", latex_robust, f"{titulo_proy}.tex")
    st.success("¡Documentación robusta generada!")
