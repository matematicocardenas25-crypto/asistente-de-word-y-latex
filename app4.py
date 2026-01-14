import streamlit as st
import re
from datetime import datetime

# --- 1. IDENTIDAD INSTITUCIONAL (2026-01-12) ---
def obtener_fecha():
    # Localización manual para asegurar español en el servidor
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    f = datetime.now()
    return f"{f.day} de {meses[f.month-1]}, {f.year}"

FECHA_HOY = obtener_fecha()
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Compilador Matemático - Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE PROSA (No quita nada, solo añade) ---
def generar_introduccion(titulo):
    return f"El presente compendio técnico enfocado en '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua."

# --- 3. PROCESADOR DE TEXTO MIXTO (SOPORTA PÁRRAFOS LARGOS) ---
def renderizar_guia(texto):
    if not texto: return
    
    # Dividimos por bloques de párrafos para mantener la estructura de tu Word
    bloques = texto.split('\n')
    
    for bloque in bloques:
        b = bloque.strip()
        if not b:
            st.write("") # Mantiene tus espacios entre párrafos
            continue
        
        # Detección de títulos y énfasis (TEOREMA, EJEMPLO, DEFINICIÓN)
        upper_b = b.upper()
        if "TEOREMA" in upper_b:
            st.info(f"📜 **{b}**")
        elif "EJEMPLO" in upper_b:
            st.warning(f"✏️ **{b}**")
        elif "DEFINICIÓN" in upper_b:
            st.success(f"📘 **{b}**")
        elif b.startswith(('a.', 'b.', 'c.', 'd.', 'e.', '1.', '2.')):
            # Formato especial para enumeraciones de ejercicios
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**{b}**")
        
        # PROCESADO DE MATEMÁTICAS EN LÍNEA Y BLOQUE
        elif "$" in b:
            # Esta parte es vital: separa el texto de la fórmula para que no se pegue
            partes = re.split(r'(\$\$.*?\$\$|\$.*?\$)', b)
            cols = st.container()
            with cols:
                for p in partes:
                    if not p: continue
                    if p.startswith('$$'): # Ecuación centrada
                        st.latex(p.replace('$$', ''))
                    elif p.startswith('$'): # Ecuación en línea
                        # Para evitar que se pegue al texto, le damos un pequeño margen
                        st.latex(p.replace('$', ''))
                    else:
                        st.write(p)
        else:
            # Texto normal de los párrafos
            st.write(b)

# --- 4. INTERFAZ PROFESIONAL ---
st.title("🎓 Sistema de Compilación Académica")

col_input, col_view = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Entrada de Texto (Copie de su Word)")
    tema_titulo = st.text_input("Título de la Guía:", "Sucesiones y Series parte 1")
    contenido_word = st.text_area("Pegue aquí todo el contenido:", height=500, placeholder="Ejemplo: Definición del límite de una sucesión...")

with col_view:
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        # Cabecera según tu instrucción
        st.markdown(f"<div style='text-align:right; font-size:12px;'>León, Nicaragua. {FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-left: 5px solid #1A5276; padding-left: 10px; color: #1A5276;'><b>{IDENTIDAD}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{tema_titulo}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Introducción Automática
        st.markdown("### I. Introducción")
        st.write(generar_introduccion(tema_titulo))
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Contenido íntegro del usuario
        renderizar_guia(contenido_word)
        
        st.markdown("<br>---")
        st.caption("Documento generado para fines académicos - Licenciatura en Matemática")

# --- 5. EXPORTACIÓN A LATEX (CONSTRUCCIÓN SEGURA) ---
if st.button("🚀 Generar Código LaTeX para Impresión"):
    # Construcción limpia para evitar SyntaxError
    codigo_final = r"""\documentclass[12pt]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, geometry}
\geometry{margin=1in}
\begin{center}
    {\Large \textbf{""" + tema_titulo + r"""}} \\
    """ + IDENTIDAD + r""" \\
    """ + FECHA_HOY + r"""
\end{center}
\section{Introducción}
""" + generar_introduccion(tema_titulo) + r"""
\section{Desarrollo}
""" + contenido_word + r"""
\end{document}"""

    st.code(codigo_final, language='latex')
