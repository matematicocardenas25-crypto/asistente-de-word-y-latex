import streamlit as st
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA (2026-01-12) ---
def obtener_fecha_nicaragua():
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    f = datetime.now()
    return f"{f.day} de {meses[f.month-1]}, {f.year}"

FECHA_HOY = obtener_fecha_nicaragua()
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Académico - Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE PROSA (No quita nada) ---
def generar_prosa(titulo):
    return {
        "intro": "El presente compendio técnico enfocado en '" + titulo + "' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": "Tras la revisión de los elementos que integran '" + titulo + "', se concluye que la estructuración lógica permite una resolución eficaz de problemas complejos."
    }

# --- 3. PROCESADOR DE TEXTO MIXTO (SOLUCIONA EL TEXTO PEGADO) ---
def renderizar_bloques(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l:
            st.write("")
            continue
        
        # Formato para Teoremas, Ejemplos y Definiciones
        up = l.upper()
        if "TEOREMA" in up: st.info("📜 **" + l + "**")
        elif "EJEMPLO" in up or "EJERCICIO" in up: st.warning("✏️ **" + l + "**")
        elif "DEFINICIÓN" in up: st.success("📘 **" + l + "**")
        
        # Procesado de fórmulas mixtas
        elif "$" in l:
            partes = re.split(r'(\$\$.*?\$\$|\$.*?\$)', l)
            for p in partes:
                if not p: continue
                if p.startswith('$'):
                    st.latex(p.replace('$', ''))
                else:
                    st.write(p.strip())
        else:
            st.write(l)

# --- 4. INTERFAZ ORIGINAL (DOS COLUMNAS) ---
st.title("🎓 Sistema de Compilación - Lic. Ismael Cárdenas")

# Recuperamos los dos cuadros de entrada
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    tema = st.text_input("Título del Tema:", "Sucesiones y Series")
    
    # Los dos archivos/bloques que pediste
    desarrollo = st.text_area("Cuerpo del Desarrollo (Word/LaTeX):", height=300, placeholder="Definiciones, teoremas...")
    ejercicios = st.text_area("Sección de Práctica y Ejercicios:", height=200, placeholder="Enuncie aquí los ejercicios...")

with col_pre:
    textos_ia = generar_prosa(tema)
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        # Cabecera solicitada
        st.markdown("<div style='text-align:right; font-size:12px; color:gray;'>" + FECHA_HOY + "</div>", unsafe_allow_html=True)
        st.markdown("<div style='border-left: 5px solid #1A5276; padding-left: 15px;'><b>" + IDENTIDAD + "</b></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#1A5276;'>" + tema + "</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. INTRODUCCIÓN")
        st.write(textos_ia["intro"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Mostramos ambos bloques en la vista previa
        renderizar_bloques(desarrollo)
        st.markdown("<br>", unsafe_allow_html=True)
        renderizar_bloques(ejercicios)
        
        st.markdown("---")
        st.markdown("### IV. CONCLUSIONES")
        st.write(textos_ia["conclu"])

# --- 5. GENERADOR DE LATEX (SIN ERRORES DE LLAVES) ---
if st.button("🚀 Generar Código LaTeX"):
    # Usamos concatenación (+) para que las llaves de LaTeX no choquen con Python
    c_tex = r"\documentclass[12pt]{article}" + "\n" + r"\usepackage[spanish]{babel}" + "\n"
    c_tex += r"\usepackage{amsmath, amssymb, geometry}" + "\n" + r"\geometry{margin=1in}" + "\n"
    c_tex += r"\begin{document}" + "\n"
    c_tex += r"\title{" + tema + "}\n" + r"\author{" + IDENTIDAD + "}\n" + r"\date{" + FECHA_HOY + "}\n" + r"\maketitle" + "\n"
    
    c_tex += r"\section{Desarrollo Teórico}" + "\n" + desarrollo + "\n"
    c_tex += r"\section{Práctica}" + "\n" + ejercicios + "\n"
    
    c_tex += r"\end{document}"
    
    st.code(c_tex, language="latex")
    st.success("¡Código listo! Copia esto en Overleaf.")
