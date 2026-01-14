import streamlit as st
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_HOY = obtener_fecha_espanol()
# Texto de identidad solicitado
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Asistente Matemático - Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ---
def generar_prosa_automatica(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad analítica y aplicabilidad técnica.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución interdisciplinarios para potenciar el alcance del análisis matemático en el contexto de las ciencias exactas."
    }

# --- 3. MOTOR DE ESTILIZADO (VIÑETAS Y CUADROS) ---
def renderizar_bloques_academicos(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Detección de Viñetas (Bullets de Diamante)
        if l.startswith(('-', '*', '•', '◈')) or re.match(r'^[0-9|a-z]\.', l):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {l.lstrip('-*•◈')}")
            continue

        # Cuadros Académicos
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{l}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**")
        else:
            if "$" in l: st.latex(l.replace("$", ""))
            else: st.write(l)

# --- 4. INTERFAZ DE USUARIO ---
st.title("🎓 Sistema de Compilación Académica - Lic. Ismael Cárdenas")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_input, col_preview = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Panel de Insumos")
    titulo_doc = st.text_input("Título del Tema:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Cuerpo Teórico (LaTeX):", value=st.session_state.desarrollo, height=300)
    st.session_state.ejercicios = st.text_area("Práctica Propuesta:", value=st.session_state.ejercicios, height=150)

with col_preview:
    textos_ia = generar_prosa_automatica(titulo_doc)
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        # Cabecera Tipográfica (Sin imágenes para evitar errores)
        st.markdown(f"<div style='text-align:right; font-size:12px;'>León, Nicaragua. {FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-left: 5px solid #1A5276; padding-left: 15px;'><b>{IDENTIDAD}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo_doc}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### I. Introducción\n{textos_ia['intro']}")
        renderizar_bloques_academicos(st.session_state.desarrollo)
        renderizar_bloques_academicos(st.session_state.ejercicios)
        st.markdown(f"### IV. Conclusiones\n{textos_ia['conclu']}")

# --- 5. EXPORTACIÓN A LATEX ---
if st.button("🚀 Generar Código LaTeX Profesional"):
    textos_ia = generar_prosa_automatica(titulo_doc)
    
    # Construcción de string pura para evitar conflicto de llaves {}
    latex_final = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, tcolorbox, geometry}
\geometry{margin=1in}

\begin{document}
\begin{flushright} """ + FECHA_HOY + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + titulo_doc + r"""}} \\[0.5cm]
    {\large \textbf{""" + IDENTIDAD + r"""}}
\end{center}

\section{Introducción}
""" + textos_ia['intro'] + r"""

\section{Desarrollo}
""" + st.session_state.desarrollo + r"""

\section{Ejercicios}
""" + st.session_state.ejercicios + r"""

\section{Conclusiones}
""" + textos_ia['conclu'] + r"""

\end{document}"""

    st.download_button("⬇️ Descargar archivo .tex", latex_final, f"{titulo_doc}.tex")
    st.code(latex_final, language='latex')
