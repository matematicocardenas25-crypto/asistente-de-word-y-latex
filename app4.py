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
        "intro": f"El presente compendio técnico enfocado en el estudio de '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una resolución eficaz de problemas complejos.",
        "recom": "Se recomienda integrar estos resultados en esquemas de investigación interdisciplinaria para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR DE ESTILIZADO CON ESPACIADO (CORRIGE TEXTOS PEGADOS) ---
def renderizar_bloques_limpios(texto):
    if not texto: return
    # Separamos por líneas y eliminamos espacios vacíos extra
    lineas = [l.strip() for l in texto.split('\n') if l.strip()]
    
    for linea in lineas:
        # A. Detección de Viñetas (Diamantes)
        if linea.startswith(('-', '*', '•', '◈')) or re.match(r'^[0-9|a-z]\.', linea):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {linea.lstrip('-*•◈')}")
            st.markdown("<div style='margin-bottom: -10px;'></div>", unsafe_allow_html=True) # Ajuste de espacio
            continue

        # B. Cuadros Académicos (Teoremas, Definiciones)
        up = linea.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{linea}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{linea}**")
        else:
            # C. Renderizado de LaTeX con ESPACIADO AUTOMÁTICO
            if "$" in linea:
                # Limpiamos espacios internos que causan el texto "pegado"
                formula = linea.replace("$", "")
                st.latex(formula)
                # Forzamos un pequeño espacio debajo de cada fórmula
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.write(linea)

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    tema = st.text_input("Título del Tema:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.desarrollo, height=300, placeholder="Escribe aquí teoremas y definiciones...")
    st.session_state.ejercicios = st.text_area("Sección de Práctica:", value=st.session_state.ejercicios, height=150, placeholder="Escribe aquí los ejercicios...")

with col_pre:
    textos_ia = generar_prosa_automatica(tema)
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        # Cabecera Institucional
        st.markdown(f"<div style='text-align:right; font-size:12px; color:gray;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-left: 5px solid #1A5276; padding-left: 15px; margin-bottom: 20px;'><b>{IDENTIDAD}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276; margin-bottom: 30px;'>{tema}</h1>", unsafe_allow_html=True)
        
        st.markdown("### I. Introducción")
        st.write(textos_ia['intro'])
        st.markdown("---")
        
        renderizar_bloques_limpios(st.session_state.desarrollo)
        renderizar_bloques_limpios(st.session_state.ejercicios)
        
        st.markdown("---")
        st.markdown("### IV. Conclusiones")
        st.write(textos_ia['conclu'])
        st.markdown(f"*Recomendación:* {textos_ia['recom']}")

# --- 5. EXPORTACIÓN A LATEX (CON ESPACIOS DE IMPRESIÓN) ---
if st.button("🚀 Generar Código LaTeX para Impresión"):
    textos_ia = generar_prosa_automatica(tema)
    
    # Construcción de string robusta
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

\section{Desarrollo Teórico}
""" + st.session_state.desarrollo.replace("$", "\\[ ").replace("$", " \\]") + r"""

\section{Ejercicios Propuestos}
""" + st.session_state.ejercicios.replace("$", "\\[ ").replace("$", " \\]") + r"""

\section{Conclusiones}
""" + textos_ia['conclu'] + r"""

\end{document}"""

    st.download_button("⬇️ Descargar .tex", latex_final, f"{tema}.tex")
    st.code(latex_final, language='latex')
    st.success("¡Listo! Este código separa las fórmulas automáticamente en Overleaf.")
