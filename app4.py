import streamlit as st
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_HOY = obtener_fecha_espanol()
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Asistente Matemático - Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ---
def generar_prosa_automatica(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en el estudio de '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una resolución eficaz de problemas complejos.",
        "recom": "Se recomienda integrar estos resultados en esquemas de investigación interdisciplinaria para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR ANTIPEGO (CORRIGE TEXTOS MEZCLADOS) ---
def renderizar_bloques_limpios(texto):
    if not texto: return
    # Dividimos por líneas para procesar una por una
    lineas = texto.split('\n')
    
    for linea in lineas:
        l = linea.strip()
        if not l: 
            st.write("") # Espacio en blanco real
            continue
        
        # A. Detección de Viñetas (Diamantes)
        if l.startswith(('-', '*', '•', '◈')) or re.match(r'^[0-9|a-z]\.', l):
            # Limpiamos el texto de la viñeta y lo mostramos con espacio
            contenido_vineta = l.lstrip('-*•◈').strip()
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {contenido_vineta}")
            continue

        # B. Cuadros Académicos (Teoremas, Definiciones)
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{l}**")
            continue
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
            continue
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**")
            continue

        # C. Renderizado de TEXTO MEZCLADO O MATEMÁTICO
        # Si la línea tiene $, la procesamos para que no salga pegada
        if "$" in l:
            # Separamos el texto de la fórmula para dar aire
            partes = l.split("$")
            for p in partes:
                p = p.strip()
                if not p: continue
                # Si la parte es matemática (intentamos renderizarla)
                if len(p) > 1 and any(c in p for c in r"+-*/=^_\()"):
                    st.latex(p)
                else:
                    st.write(p)
        else:
            st.write(l)

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    tema = st.text_input("Título del Tema:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.desarrollo, height=300, placeholder="Escriba aquí... Use $ para fórmulas.")
    st.session_state.ejercicios = st.text_area("Sección de Práctica:", value=st.session_state.ejercicios, height=150)

with col_pre:
    textos_ia = generar_prosa_automatica(tema)
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        # Cabecera Institucional Limpia
        st.markdown(f"<div style='text-align:right; font-size:12px; color:gray;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-left: 5px solid #1A5276; padding-left: 15px;'><b>{IDENTIDAD}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. Introducción")
        st.write(textos_ia['intro'])
        st.markdown("<br>", unsafe_allow_html=True)
        
        renderizar_bloques_limpios(st.session_state.desarrollo)
        renderizar_bloques_limpios(st.session_state.ejercicios)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### IV. Conclusiones")
        st.write(textos_ia['conclu'])

# --- 5. EXPORTACIÓN A LATEX (CONSTRUCCIÓN SEGURA) ---
if st.button("🚀 Generar Código LaTeX (Sin Errores)"):
    textos_ia = generar_prosa_automatica(tema)
    
    # Usamos concatenación (+) en lugar de f-strings para evitar errores con las llaves {}
    latex_final = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, tcolorbox, geometry}
\geometry{margin=1in}

\begin{document}
\begin{flushright} """ + FECHA_HOY + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + tema + r"""}} \\[0.5cm]
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

    st.download_button("⬇️ Descargar archivo .tex", latex_final, f"{tema}.tex")
    st.code(latex_final, language='latex')
