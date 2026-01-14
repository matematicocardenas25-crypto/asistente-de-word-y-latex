import streamlit as st
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN Y FIRMA ---
def obtener_fecha():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_DOC = obtener_fecha()
# Firma solicitada por el Licenciado
FIRMA_ID = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Académico Cárdenas", layout="wide")

# --- 2. MOTOR DE PROSA ACADÉMICA ---
def generar_prosa(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento formaliza los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León.",
        "conclu": f"Tras la revisión de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad analítica.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución interdisciplinarios para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR DE ESTILIZADO ROBUSTO (SIN DELTAGENERATOR ERROR) ---
def renderizar_bloques_pro(texto):
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

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🎓 Compilador de Ingeniería Matemática - Lic. Ismael Cárdenas")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    tema = st.text_input("Título del Proyecto:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Contenido Teórico (LaTeX):", value=st.session_state.desarrollo, height=300)
    st.session_state.ejercicios = st.text_area("Sección de Práctica:", value=st.session_state.ejercicios, height=150)

with col_pre:
    prosa = generar_prosa(tema)
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        # Cabecera con Firma y Fecha
        st.markdown(f"<div style='text-align:right; font-size:12px;'>{FECHA_DOC}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:14px; color:#1A5276;'><b>{FIRMA_ID}</b></p>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Secciones Automatizadas
        st.markdown(f"**I. INTRODUCCIÓN**\n\n{prosa['intro']}")
        st.markdown("---")
        renderizar_bloques_pro(st.session_state.desarrollo)
        renderizar_bloques_pro(st.session_state.ejercicios)
        st.markdown("---")
        st.markdown(f"**IV. CONCLUSIONES**\n\n{prosa['conclu']}")

# --- 5. GENERACIÓN DE CÓDIGO LATEX (BLINDADO CONTRA SYNTAXERROR) ---
if st.button("🚀 Generar Código LaTeX de Alta Gama"):
    prosa = generar_prosa(tema)
    
    # Construcción por partes para evitar el error de llaves de f-strings
    parte1 = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, tcolorbox, geometry}
\geometry{margin=1in}
\newtcolorbox{mybox}[2]{colback=#1!5!white,colframe=#1!75!black,fonttitle=\bfseries,title=#2}
\begin{document}
\begin{flushright} """ + FECHA_DOC + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + tema + r"""}} \\[0.5cm]
    {\large \textbf{""" + FIRMA_ID + r"""}}
\end{center}

\section{Introducción}
""" + prosa['intro'] + r"""

\section{Marco Teórico}
""" + st.session_state.desarrollo + r"""

\section{Ejercicios}
""" + st.session_state.ejercicios + r"""

\section{Conclusiones y Recomendaciones}
""" + prosa['conclu'] + r"""
\vspace{0.5cm}
""" + prosa['recom'] + r"""

\end{document}"""

    st.download_button("⬇️ Descargar archivo .tex", parte1, f"{tema}.tex")
    st.code(parte1, language='latex')
    st.success("¡Código para Overleaf generado! No olvides darle a 'Recompile' en Overleaf para ver los cuadros.")
