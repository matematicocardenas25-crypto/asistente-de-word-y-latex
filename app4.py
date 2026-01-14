import streamlit as st
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA (Requisitos del Licenciado) ---
FECHA_HOY = "14 de Enero, 2026" # Basado en tus capturas recientes
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Compilador Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE PROSA ACADÉMICA ---
def generar_prosa(titulo):
    return {
        "intro": f"El presente compendio técnico enfocado en '{titulo}' constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León Nicaragua.",
        "conclu": f"Tras la revisión de los elementos que integran '{titulo}', se concluye que la estructuración lógica permite una resolución eficaz de problemas complejos."
    }

# --- 3. PROCESADOR DE TEXTO MIXTO (EVITA EL TEXTO PEGADO) ---
def renderizar_matematica_limpia(texto):
    if not texto: return
    # Dividimos por saltos de línea para respetar tus párrafos
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l:
            st.write("") # Espacio en blanco
            continue
        
        # Resaltado de secciones importantes (Teoremas, Ejemplos)
        if any(k in l.upper() for k in ["TEOREMA", "DEFINICIÓN", "EJEMPLO"]):
            st.markdown(f"#### {l}")
            continue

        # Detección de matemáticas para que NO se amontonen
        if "$" in l:
            # Separamos el texto de las fórmulas
            partes = re.split(r'(\$\$.*?\$\$|\$.*?\$)', l)
            for p in partes:
                if not p: continue
                if p.startswith('$'):
                    # Renderizamos la matemática sola para que tenga su espacio
                    st.latex(p.replace('$', ''))
                else:
                    # El texto plano sale normal
                    st.write(p.strip())
        else:
            st.write(l)

# --- 4. INTERFAZ DE DOS COLUMNAS (RECUPERADA) ---
st.title("🎓 Sistema Académico Profesional - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Entrada de Contenido")
    tema = st.text_input("Título del Tema:", "Sucesiones y Series")
    
    # Bloques de entrada que pediste de vuelta
    desarrollo = st.text_area("Desarrollo Teórico (Word/LaTeX):", height=300)
    ejercicios = st.text_area("Sección de Práctica:", height=200)

with col_pre:
    textos_ia = generar_prosa(tema)
    st.subheader("👁️ Vista Previa del Documento")
    with st.container(border=True):
        # Cabecera Institucional
        st.markdown(f"<div style='text-align:right; font-size:12px;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"**{IDENTIDAD}**")
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### I. INTRODUCCIÓN")
        st.write(textos_ia["intro"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Renderizado de tus textos con el motor de matemática limpia
        renderizar_matematica_limpia(desarrollo)
        st.markdown("<br>", unsafe_allow_html=True)
        renderizar_matematica_limpia(ejercicios)
        
        st.markdown("---")
        st.markdown("### IV. CONCLUSIONES")
        st.write(textos_ia["conclu"])

# --- 5. GENERADOR DE LATEX Y WORD (CÓDIGO PURO) ---
st.divider()
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🚀 Generar Código LaTeX (Sin Errores)"):
        # Construcción manual para evitar el error de llaves de tus capturas
        latex_final = r"\documentclass[12pt]{article}" + "\n" + r"\usepackage[spanish]{babel}" + "\n"
        latex_final += r"\begin{document}" + "\n" + r"\title{" + tema + "}\n"
        latex_final += r"\author{" + IDENTIDAD + "}\n" + r"\maketitle" + "\n"
        latex_final += r"\section{Contenido}" + "\n" + desarrollo + "\n"
        latex_final += r"\section{Ejercicios}" + "\n" + ejercicios + "\n"
        latex_final += r"\end{document}"
        
        st.code(latex_final, language="latex")

with col_btn2:
    st.info("Para exportar a Word: Copia la Vista Previa y pégala directamente en un archivo Word. El formato se mantendrá limpio.")
