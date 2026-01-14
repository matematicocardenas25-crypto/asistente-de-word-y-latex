import streamlit as st
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA (BLINDAJE TOTAL) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_ACTUAL = obtener_fecha_espanol()
FIRMA_TEXTO = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en el análisis de '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento formaliza los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León.",
        "conclu": f"Tras la revisión pormenorizada de '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad analítica y aplicabilidad técnica.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución interdisciplinarios para potenciar el alcance del análisis matemático en el contexto de las ciencias exactas."
    }

# --- 3. MOTOR DE ESTILIZADO (VIÑETAS Y CUADROS) ---
def renderizar_bloques(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Detección de Viñetas Elegantes
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
st.title("🎓 Compilador de Élite - Lic. Ismael Cárdenas")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_tema = st.text_input("Título del Documento:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Contenido Teórico (LaTeX):", value=st.session_state.desarrollo, height=300)
    st.session_state.ejercicios = st.text_area("Sección de Práctica:", value=st.session_state.ejercicios, height=150)

with col_pre:
    textos = generar_prosa_profesional(titulo_tema)
    st.subheader("👁️ Vista Previa Institucional")
    
    # Simulación de la foto de perfil circular si no existe el archivo
    with st.container(border=True):
        c1, c2 = st.columns([1, 4])
        with c1:
            st.markdown("🟡", help="Espacio para Foto") # Placeholder circular simple
        with c2:
            st.markdown(f"<div style='text-align:right; font-size:12px;'>{FECHA_ACTUAL}</div>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:14px;'><b>{FIRMA_TEXTO}</b></p>", unsafe_allow_html=True)
        
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo_tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### I. Introducción\n{textos['intro']}")
        renderizar_bloques(st.session_state.desarrollo)
        renderizar_bloques(st.session_state.ejercicios)
        st.markdown(f"### IV. Conclusiones\n{textos['conclu']}")
        st.markdown(f"### V. Recomendaciones\n{textos['recom']}")

# --- 5. EXPORTACIÓN (PDF Y LATEX) ---
st.markdown("### 🚀 Generar Archivos Finales")
b1, b2 = st.columns(2)

with b1:
    if st.button("📄 Preparar Impresión PDF"):
        st.info("💡 **Instrucción:** Se abrirá una vista limpia. Pulsa `Ctrl + P` y elige 'Guardar como PDF' para obtener tu documento con todos los cuadros y colores.")
        # Se genera una versión minimalista para impresión
        st.markdown(f"## {titulo_tema}\n{FIRMA_TEXTO}\n{FECHA_ACTUAL}")
        st.write(textos['intro'])
        st.write(st.session_state.desarrollo)
        st.write(st.session_state.ejercicios)

with b2:
    # Código LaTeX usando concatenación manual para evitar error de llaves
    latex_out = r"""\documentclass[12pt]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, tcolorbox, geometry}
\geometry{margin=1in}
\newtcolorbox{mybox}[2]{colback=#1!5!white,colframe=#1!75!black,fonttitle=\bfseries,title=#2}
\begin{document}
\begin{flushright} """ + FECHA_ACTUAL + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + titulo_tema + r"""}} \\[0.5cm]
    {\large \textbf{""" + FIRMA_TEXTO + r"""}}
\end{center}
\section{Introducción}
""" + textos['intro'] + r"""
\section{Desarrollo}
""" + st.session_state.desarrollo + r"""
\section{Ejercicios}
""" + st.session_state.ejercicios + r"""
\section{Conclusiones}
""" + textos['conclu'] + r"""
\end{document}"""

    st.download_button("⬇️ Descargar Código .tex", latex_out, f"{titulo_tema}.tex")
