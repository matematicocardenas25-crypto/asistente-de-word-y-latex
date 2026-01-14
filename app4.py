import streamlit as st
import re
from datetime import datetime

# --- 1. DATOS DEL LICENCIADO Y FECHA ---
def obtener_fecha_nicaragua():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_ACTUAL = obtener_fecha_nicaragua()
FIRMA_OFICIAL = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Compilador Ismael Cárdenas", layout="wide")

# --- 2. GENERADOR DE TEXTO ACADÉMICO ---
def redactar_prosa(titulo):
    return {
        "intro": "El presente compendio técnico, centrado en el estudio de '" + titulo + "', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso, garantizando la coherencia teórica necesaria para el estudio avanzado en la UNAN León.",
        "conclu": "Tras la revisión de los elementos que integran '" + titulo + "', se concluye que la estructuración lógica permite una transición fluida hacia modelos de mayor complejidad analítica.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución interdisciplinarios para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR ANTIPEGO (SEPARA TEXTO DE FÓRMULAS) ---
def renderizado_profesional(texto):
    if not texto: return
    # Separamos por saltos de línea para procesar bloques independientes
    bloques = texto.split('\n')
    
    for bloque in bloques:
        b = bloque.strip()
        if not b: 
            st.write("") 
            continue
        
        # A. Detección de Viñetas de Diamante
        if b.startswith(('-', '*', '•', '◈')) or re.match(r'^[0-9|a-z]\.', b):
            st.markdown("  ◈ " + b.lstrip('-*•◈').strip())
            continue

        # B. Cuadros para Teoremas y Definiciones
        UPPER_B = b.upper()
        if any(k in UPPER_B for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info("📜 **" + b + "**")
        elif any(k in UPPER_B for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success("📘 **" + b + "**")
        elif any(k in UPPER_B for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning("✏️ **" + b + "**")
        
        # C. Manejo de Fórmulas para que NO salgan pegadas
        elif "$" in b:
            partes = b.split("$")
            for p in partes:
                p_limpia = p.strip()
                if not p_limpia: continue
                # Si parece fórmula (tiene símbolos matemáticos), usamos latex
                if any(c in p_limpia for c in "+-*/=^_\\()0123456789"):
                    st.latex(p_limpia)
                else:
                    st.write(p_limpia)
        else:
            st.write(b)

# --- 4. INTERFAZ ---
st.title("🎓 Sistema de Compilación Académica - UNAN León")

if 'teoria' not in st.session_state: st.session_state.teoria = ""
if 'practica' not in st.session_state: st.session_state.practica = ""

col_izq, col_der = st.columns([1, 1.3])

with col_izq:
    st.subheader("📥 Entrada de Datos")
    titulo_tema = st.text_input("Título del Documento:", "Sucesiones y Series parte 1")
    st.session_state.teoria = st.text_area("Desarrollo Teórico (Use $ para fórmulas):", value=st.session_state.teoria, height=300)
    st.session_state.practica = st.text_area("Sección de Ejercicios:", value=st.session_state.practica, height=150)

with col_der:
    textos_pro = redactar_prosa(titulo_tema)
    st.subheader("👁️ Vista Previa Profesional")
    with st.container(border=True):
        # Encabezado limpio
        st.markdown("<div style='text-align:right; font-size:12px;'>" + FECHA_ACTUAL + "</div>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; border-left: 4px solid #1A5276; padding-left:10px;'><b>" + FIRMA_OFICIAL + "</b></p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#1A5276;'>" + titulo_tema + "</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. INTRODUCCIÓN")
        st.write(textos_pro['intro'])
        st.markdown("<br>", unsafe_allow_html=True) # Espacio extra para que no pegue
        
        renderizado_profesional(st.session_state.teoria)
        renderizado_profesional(st.session_state.practica)
        
        st.markdown("---")
        st.markdown("### IV. CONCLUSIONES")
        st.write(textos_pro['conclu'])
        st.markdown("**Recomendación:** " + textos_pro['recom'])

# --- 5. EXPORTACIÓN A LATEX (CONSTRUCCIÓN SEGURA) ---
if st.button("🚀 Generar Código LaTeX para Overleaf"):
    textos_pro = redactar_prosa(titulo_tema)
    
    # Construcción manual para evitar el error de SyntaxError por llaves
    codigo_latex = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, tcolorbox, geometry}
\geometry{margin=1in}
\begin{document}
\begin{flushright} """ + FECHA_ACTUAL + r""" \end{flushright}
\begin{center}
    {\Huge \textbf{""" + titulo_tema + r"""}} \\[0.5cm]
    {\large \textbf{""" + FIRMA_ID + r"""}}
\end{center}
\section{Introducción}
""" + textos_pro['intro'] + r"""
\section{Desarrollo}
""" + st.session_state.teoria + r"""
\section{Ejercicios}
""" + st.session_state.practica + r"""
\section{Conclusiones}
""" + textos_pro['conclu'] + r"""
\end{document}"""

    st.download_button("⬇️ Descargar archivo .tex", codigo_latex, titulo_tema + ".tex")
    st.code(codigo_latex, language='latex')
    st.success("¡Código generado! Cópialo en Overleaf para un PDF perfecto.")
