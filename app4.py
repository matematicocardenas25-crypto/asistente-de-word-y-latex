import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA (SIN ERRORES) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_ACTUAL = obtener_fecha_espanol()
NOMBRE_FIRMA = "Ismael Antonio Cardenas López"
CARGO_FIRMA = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE RENDERIZADO (VIÑETAS Y CUADROS) ---
def renderizar_estilo_academico(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # A. Detección de Viñetas (Bullets Elegantes)
        if l.startswith(('-', '*', '•', '◈')) or re.match(r'^[0-9|a-z]\.', l):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {l.lstrip('-*•◈')}")
            continue

        # B. Cuadros Tipo Libro
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{l}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**")
        else:
            # C. Renderizado de LaTeX Seguro
            if "$" in l:
                st.latex(l.replace("$", ""))
            else:
                st.write(l)

# --- 3. INTERFAZ PRINCIPAL ---
st.title("🎓 Compilador Académico Ismael Cárdenas - UNAN")

if 'desarrollo_txt' not in st.session_state: st.session_state.desarrollo_txt = ""
if 'ejercicios_txt' not in st.session_state: st.session_state.ejercicios_txt = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_tema = st.text_input("Título del Documento:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo_txt = st.text_area("Contenido Teórico (LaTeX):", value=st.session_state.desarrollo_txt, height=350)
    st.session_state.ejercicios_txt = st.text_area("Sección de Ejercicios:", value=st.session_state.ejercicios_txt, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{FECHA_ACTUAL}</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo_tema}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{NOMBRE_FIRMA}</b><br><i>{CARGO_FIRMA}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. Marco Teórico")
        renderizar_estilo_academico(st.session_state.desarrollo_txt)
        st.markdown("### II. Ejercicios y Práctica")
        renderizar_estilo_academico(st.session_state.ejercicios_txt)

# --- 4. GENERADOR DE CÓDIGO LATEX (BLINDADO) ---
if st.button("🚀 Generar Código LaTeX para Overleaf"):
    # Usamos Raw Strings (r"") para que las llaves no causen SyntaxError
    latex_final = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, tcolorbox, geometry}
\geometry{margin=1in}
\newtcolorbox{mybox}[2]{colback=#1!5!white,colframe=#1!75!black,fonttitle=\bfseries,title=#2}

\begin{document}
\begin{flushright} """ + FECHA_ACTUAL + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + titulo_tema + r"""}} \\[0.5cm]
    {\large \textbf{""" + NOMBRE_FIRMA + r"""} \\ \textit{""" + CARGO_FIRMA + r"""}}
\end{center}

\section{Desarrollo}
""" + st.session_state.desarrollo_txt + r"""

\section{Ejercicios}
""" + st.session_state.ejercicios_txt + r"""

\end{document}"""

    st.download_button("⬇️ Descargar archivo .tex", latex_final, f"{titulo_tema}.tex")
    st.code(latex_final, language='latex')
    st.success("¡Código generado! Pégalo en Overleaf para un PDF perfecto.")
