import streamlit as st
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN E IDENTIDAD (UNAN LEÓN) ---
FECHA_DOC = datetime.now().strftime("%d de %m, %Y")
FIRMA = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Compilador Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ---
def generar_prosa(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": f"Tras la revisión de los elementos que integran '{titulo}', se concluye que la estructuración lógica permite una resolución eficaz de problemas complejos."
    }

# --- 3. MOTOR DE RENDERIZADO (ESTE ARREGLA EL TEXTO PEGADO) ---
def renderizado_mejorado(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Viñetas de diamante
        if l.startswith(('-', '*', '•', '◈')):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {l.lstrip('-*•◈')}")
            continue

        # Cuadros de colores (Teoremas y Ejemplos)
        if "TEOREMA" in l.upper():
            st.info(f"📜 **{l}**")
        elif "EJEMPLO" in l.upper() or "EJERCICIO" in l.upper():
            st.warning(f"✏️ **{l}**")
        elif "DEFINICIÓN" in l.upper():
            st.success(f"📘 **{l}**")
        
        # PROCESADO DE MATEMÁTICAS (Para que no se corte el texto)
        elif "$" in l:
            # Dividimos la línea para que la matemática respire
            partes = l.split("$")
            for p in partes:
                if not p.strip(): continue
                # Si detectamos símbolos matemáticos, usamos latex() solo para esa parte
                if any(c in p for c in "=^\\/_+"):
                    st.latex(p.strip())
                else:
                    st.write(p.strip())
        else:
            st.write(l)

# --- 4. INTERFAZ ORIGINAL DE DOS COLUMNAS ---
st.title("🎓 Asistente de Redacción Científica - Lic. Ismael Cárdenas")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Entrada de Contenido")
    tema = st.text_input("Título del Proyecto:", "Sucesiones y Series")
    contenido = st.text_area("Desarrollo (Use $ para fórmulas):", height=400, placeholder="Escriba aquí sus definiciones y ejercicios...")

with col_pre:
    textos = generar_prosa(tema)
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        # Cabecera solicitada
        st.markdown(f"<div style='text-align:right; font-size:12px;'>{FECHA_DOC}</div>", unsafe_allow_html=True)
        st.markdown(f"**{FIRMA}**")
        st.markdown(f"<h1 style='text-align:center;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. INTRODUCCIÓN")
        st.write(textos["intro"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Renderizado del cuerpo
        renderizado_mejorado(contenido)
        
        st.markdown("<br>---")
        st.markdown("### IV. CONCLUSIONES")
        st.write(textos["conclu"])

# --- 5. GENERADOR DE CÓDIGO LATEX (BLINDADO) ---
if st.button("🚀 Obtener Código para Overleaf"):
    # Usamos concatenación (+) para evitar el error de llaves de las capturas
    latex_final = r"\documentclass[12pt]{article}" + "\n" + r"\usepackage[spanish]{babel}" + "\n"
    latex_final += r"\begin{document}" + "\n"
    latex_final += r"\section{Introducción}" + "\n" + textos["intro"] + "\n"
    latex_final += r"\section{Desarrollo}" + "\n" + contenido + "\n"
    latex_final += r"\end{document}"
    
    st.code(latex_final, language="latex")
