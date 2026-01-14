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

# --- 1. IDENTIDAD Y FECHA (BLINDAJE TOTAL) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ROBUSTA ---
def generar_textos_academicos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. MOTOR DE ESTILIZADO CON VIÑETAS (VISTA PREVIA) ---
def renderizar_bloques(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia: continue
        
        # Detector de Viñetas de LaTeX
        if linea_limpia.startswith(r"\item"):
            contenido_item = linea_limpia.replace(r"\item", "").strip()
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;● {contenido_item}")
            continue

        upper_line = linea_limpia.upper()
        if any(k in upper_line for k in ["TEOREMA", "PROPOSICIÓN", "LEMA", "AXIOMA"]):
            st.info(f"✨ **{linea_limpia}**")
        elif any(k in upper_line for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea_limpia}**")
        elif any(k in upper_line for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"📝 **{linea_limpia}**")
        elif "SOLUCIÓN" in upper_line or "SOLUCION" in upper_line:
            st.markdown(f"✅ **{linea_limpia}**")
        else:
            st.markdown(linea_limpia)

# --- 4. LIMPIEZA PARA WORD CON SOPORTE DE VIÑETAS ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Transformar items en viñetas físicas para Word
    limpio = texto.replace(r"\item", "● ")
    limpio = limpio.replace("$", "").replace(r"\[", "").replace(r"\]", "")
    reemplazos = {
        r"\dots": "...", r"\cdots": "...", r"\,": " ", r"\\": "\n",
        r"\infty": "∞", r"\to": "→", r"\alpha": "α", r"\beta": "β"
    }
    limpio = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', limpio)
    limpio = re.sub(r'\\([a-zA-Z]+)', r'\1', limpio)
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

st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN León")

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
        st.markdown(f"**I. Introducción**\n\n{textos_auto['intro']}")
        renderizar_bloques(st.session_state.contenido)
        renderizar_bloques(st.session_state.ejercicios)
        st.success(f"**IV. Conclusiones**\n\n{textos_auto['conclu']}")
        st.info(f"**V. Recomendaciones**\n\n{textos_auto['recom']}")

# --- 7. DESCARGAS ---
if st.button("🚀 Compilar Documentación de Élite", key="compilar_principal"):
    textos_auto = generar_textos_academicos(titulo_proy)
    
    # Preparar el contenido para LaTeX
    cuerpo_tex = procesar_a_latex(st.session_state.contenido)
    ejercicios_tex = procesar_a_latex(st.session_state.ejercicios)

    latex_final = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, amsfonts}} % <--- AQUÍ ESTÁ EL ARREGLO (sin la 't')
\\usepackage[most]{{tcolorbox}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}

% DEFINICIÓN DE ESTILOS (COINCIDE CON TU VISTA PREVIA)
\\newtcolorbox{{teorema_box}}{{colback=blue!5!white, colframe=blue!75!black, arc=4pt, fontupper=\\bfseries}}
\\newtcolorbox{{definicion_box}}{{colback=green!5!white, colframe=green!50!black, arc=4pt}}
\\newtcolorbox{{ejercicio_box}}{{colback=orange!5!white, colframe=orange!75!black, arc=4pt}}

\\title{{\\textbf{{{titulo_proy}}}}}
\\author{{\\textbf{{{firma_line1}}} \\\\ \\textit{{{firma_line2}}}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{textos_auto['intro']}

\\section{{Desarrollo Teórico}}
{cuerpo_tex}

\\section{{Ejercicios y Soluciones}}
{ejercicios_tex}

\\section{{Conclusiones}}
\\begin{{tcolorbox}}[colback=green!10!white, colframe=green!50!black, title=Robustas Conclusiones]
{textos_auto['conclu']}
\\end{{tcolorbox}}

\\section{{Recomendaciones}}
\\begin{{tcolorbox}}[colback=blue!10!white, colframe=blue!50!black, title=Robustas Recomendaciones]
{textos_auto['recom']}
\\end{{tcolorbox}}

\\end{{document}}
"""
    # Usamos keys únicas para evitar el error 'DuplicateElementId'
    st.download_button("⬇️ Descargar Word", b"archivo_word", key="dl_word_key") # Reemplaza con tu lógica de word
    st.download_button("⬇️ Descargar LaTeX", latex_final, f"{titulo_proy}.tex", key="dl_latex_key")
