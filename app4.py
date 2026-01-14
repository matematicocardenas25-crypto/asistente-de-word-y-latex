import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

# --- 2. MOTOR DE REDACCIÓN ---
def generar_textos_academicos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica...",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística...",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica..."
    }

# --- 3. FUNCIÓN PROCESADORA (ESTA ES LA QUE DABA NameError) ---
def procesar_a_latex(texto):
    if not texto: return ""
    lineas = texto.split('\n')
    resultado = []
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        upper_l = l.upper()
        # Envolvemos en cajas de tcolorbox según la palabra clave
        if any(k in upper_l for k in ["TEOREMA", "PROPOSICIÓN", "LEMA", "AXIOMA"]):
            resultado.append(f"\\begin{{teorema_box}}\n{l}\n\\end{{teorema_box}}")
        elif any(k in upper_l for k in ["DEFINICIÓN", "CONCEPTO"]):
            resultado.append(f"\\begin{{definicion_box}}\n{l}\n\\end{{definicion_box}}")
        elif any(k in upper_l for k in ["EJERCICIO", "EJEMPLO"]):
            resultado.append(f"\\begin{{ejercicio_box}}\n{l}\n\\end{{ejercicio_box}}")
        else:
            resultado.append(l)
    return "\n".join(resultado)

def renderizar_bloques(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        upper_l = l.upper()
        if any(k in upper_l for k in ["TEOREMA", "PROPOSICIÓN", "LEMA"]): st.info(f"✨ **{l}**")
        elif any(k in upper_l for k in ["DEFINICIÓN", "CONCEPTO"]): st.success(f"📘 **{l}**")
        elif any(k in upper_l for k in ["EJERCICIO", "EJEMPLO"]): st.warning(f"📝 **{l}**")
        else: st.markdown(l)

# --- 4. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN León")
titulo_proy = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")

col_in, col_pre = st.columns([1, 1.2])
with col_in:
    st.session_state.contenido = st.text_area("Contenido Teórico:", height=250)
    st.session_state.ejercicios = st.text_area("Ejercicios:", height=150)

with col_pre:
    st.subheader("👁️ Vista Previa")
    textos = generar_textos_academicos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"**{titulo_proy}**")
        renderizar_bloques(st.session_state.contenido)
        renderizar_bloques(st.session_state.ejercicios)

# --- 5. EL BOTÓN DE COMPILACIÓN (CORREGIDO) ---
if st.button("🚀 Compilar Documentos", key="main_comp_btn"):
    # Procesar textos
    cuerpo_tex = procesar_a_latex(st.session_state.contenido)
    ejercicios_tex = procesar_a_latex(st.session_state.ejercicios)
    textos = generar_textos_academicos(titulo_proy)

    # CÓDIGO LATEX FINAL (SIN EL ERROR amstfonts)
    latex_final = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, amsfonts}} % <--- ARREGLADO (sin la 't')
\\usepackage[most]{{tcolorbox}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}

% DEFINICIÓN DE CAJAS PARA OVERLEAF
\\newtcolorbox{{teorema_box}}{{colback=blue!5!white, colframe=blue!75!black, fontupper=\\bfseries, arc=4pt}}
\\newtcolorbox{{definicion_box}}{{colback=green!5!white, colframe=green!50!black, arc=4pt}}
\\newtcolorbox{{ejercicio_box}}{{colback=orange!5!white, colframe=orange!75!black, arc=4pt}}

\\title{{\\textbf{{{titulo_proy}}}}}
\\author{{{firma_line1} \\\\ \\small {firma_line2}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{textos['intro']}

\\section{{Contenido}}
{cuerpo_tex}

\\section{{Ejercicios}}
{ejercicios_tex}

\\section{{Conclusiones}}
\\begin{{tcolorbox}}[colback=green!10!white, colframe=green!50!black]
{textos['conclu']}
\\end{{tcolorbox}}

\\end{{document}}
"""
    # Botón de descarga con KEY ÚNICA para evitar error de duplicados
    st.download_button("⬇️ Descargar archivo .TEX para Overleaf", latex_final, f"{titulo_proy}.tex", key="dl_tex_final")
    st.success("¡Documento LaTeX generado con éxito! Pégalo en Overleaf y compilará de una.")
