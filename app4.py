import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA (BLINDAJE TOTAL CONTRA NAMEERROR) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
# Variables globales para que nunca fallen en la vista previa
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA (ROBUSTO) ---
def generar_textos_academicos(titulo):
    """Genera automáticamente textos profesionales basados en el tema."""
    return {
        "intro": f"El presente documento técnico aborda de manera sistemática los fundamentos analíticos de '{titulo}'. La finalidad de este compendio es articular los conceptos axiomáticos con sus aplicaciones prácticas, estableciendo un marco teórico riguroso que facilite la comprensión de las estructuras matemáticas involucradas bajo los estándares académicos de la UNAN León.",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la correcta aplicación de los métodos expuestos garantiza una resolución eficaz de problemas complejos. La convergencia entre la teoría purista y la práctica aplicada resulta esencial para la validación de los resultados obtenidos en este estudio.",
        "recom": "Se recomienda encarecidamente la revisión periódica de los marcos conceptuales aquí presentados para mantener la precisión en la modelización. Asimismo, se sugiere integrar estas metodologías en entornos de investigación interdisciplinaria para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR DE ESTILIZADO (CUADROS ELEGANTES EN VISTA PREVIA) ---
def renderizar_bloques(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        if not linea.strip(): continue
        upper_line = linea.upper()
        if any(k in upper_line for k in ["TEOREMA", "PROPOSICIÓN", "LEMA"]):
            st.info(f"✨ **{linea}**")
        elif any(k in upper_line for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea}**")
        elif any(k in upper_line for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"📝 **{linea}**")
        elif "SOLUCIÓN" in upper_line:
            st.markdown(f"✅ **{linea}**")
        else:
            st.markdown(linea)

# --- 4. LIMPIEZA TOTAL PARA WORD (CAPTURA DE ERRORES DE SÍMBOLOS) ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Eliminar símbolos de LaTeX que ensucian el Word
    limpio = texto.replace("$", "").replace(r"\[", "").replace(r"\]", "")
    reemplazos = {
        r"\dots": "...", r"\cdots": "...", r"\,": " ", r"\\": "\n",
        r"\left\{": "{", r"\right\}": "}", r"\left(": "(", r"\right)": ")",
        r"\infty": "∞", r"\to": "→", r"\alpha": "α", r"\beta": "β"
    }
    # Fracciones: \frac{a}{b} -> (a/b)
    limpio = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', limpio)
    # Quitar barras invertidas residuales \palabra -> palabra
    limpio = re.sub(r'\\([a-zA-Z]+)', r'\1', limpio)
    # Quitar llaves de exponentes/subíndices
    limpio = limpio.replace("{", "").replace("}", "")
    
    for lat, plain in reemplazos.items():
        limpio = limpio.replace(lat, plain)
    return limpio.strip()

# --- 5. IMAGEN CIRCULAR ---
def preparar_foto():
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

# --- 6. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Entrada de Datos")
    titulo_proy = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")
    st.session_state.contenido = st.text_area("Cuerpo del Tema (LaTeX):", value=st.session_state.contenido, height=300)
    st.session_state.ejercicios = st.text_area("Ejercicios y Soluciones:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos_auto = generar_textos_academicos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.info(f"**I. Introducción (Generada):**\n{textos_auto['intro']}")
        renderizar_bloques(st.session_state.contenido)
        renderizar_bloques(st.session_state.ejercicios)
        st.success(f"**IV. Conclusiones:**\n{textos_auto['conclu']}")

# --- 7. DESCARGAS ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos_auto = generar_textos_academicos(titulo_proy)
    
    # WORD
    doc = Document()
    head = doc.add_table(rows=1, cols=2)
    head.cell(0,0).text = fecha_actual
    p_img = head.cell(0,1).add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_img.add_run().add_picture(preparar_foto(), width=Inches(0.9))
    
    doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_line1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_line2).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    secciones = [
        ("I. Introducción", textos_auto['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios", st.session_state.ejercicios),
        ("IV. Conclusiones", textos_auto['conclu']),
        ("V. Recomendaciones", textos_auto['recom'])
    ]
    
    for t, c in secciones:
        doc.add_heading(t, 1)
        doc.add_paragraph(limpiar_para_word(c))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")

    # LATEX (PARA OVERLEAF)
    latex_code = f"\\documentclass[12pt]{{article}}\\usepackage[spanish]{{babel}}\\usepackage{{amsmath,amssymb,tcolorbox}}\\title{{{titulo_proy}}}\\author{{{firma_line1}}}\\begin{{document}}\\maketitle\\section{{Introducción}}{textos_auto['intro']}\\section{{Contenido}}{st.session_state.contenido}\\section{{Ejercicios}}{st.session_state.ejercicios}\\section{{Conclusiones}}{textos_auto['conclu']}\\end{{document}}"
    st.download_button("⬇️ Descargar Código LaTeX", latex_code, f"{titulo_proy}.tex")
