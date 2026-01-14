import streamlit as st
import re
from datetime import datetime

# --- IDENTIDAD (Solicitada 2026-01-12) ---
FECHA_HOY = datetime.now().strftime("%d de Enero, %2026")
IDENTIDAD = "Ismael Antonio Cardenas López Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Compilador Ismael", layout="wide")

# --- MOTOR DE TEXTO MIXTO (LA SOLUCIÓN DEFINITIVA) ---
def renderizar_texto_mixto(texto):
    if not texto: return
    # Dividimos por líneas para mantener tu estructura de Word
    lineas = texto.split('\n')
    
    for linea in lineas:
        l = linea.strip()
        if not l:
            st.write("") # Mantiene el aire entre párrafos
            continue
        
        # 1. Detección de Títulos Académicos
        if any(k in l.upper() for k in ["TEOREMA", "DEFINICIÓN", "EJEMPLO"]):
            st.markdown(f"### {l}")
            continue

        # 2. PROCESADO DE TEXTO MIXTO (Fórmulas entre palabras)
        # Buscamos todo lo que esté entre $ o $$
        partes = re.split(r'(\$\$.*?\$\$|\$.*?\$)', l)
        
        # Creamos una línea de texto que combine ambos
        html_linea = ""
        for p in partes:
            if p.startswith('$'): # Es matemática
                # La envolvemos en un contenedor que no deje que se pegue
                formula = p.replace('$', '')
                st.latex(formula)
            else: # Es texto plano
                if p.strip():
                    st.write(p.strip())

# --- INTERFAZ ORIGINAL ---
st.title("🎓 Sistema de Texto Mixto - Lic. Ismael Cárdenas")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Pegue su texto de Word")
    titulo = st.text_input("Tema:", "Sucesiones")
    cuerpo_doc = st.text_area("Contenido completo:", height=500)

with col2:
    st.subheader("👁️ Vista Previa Real")
    with st.container(border=True):
        # Cabecera Institucional
        st.markdown(f"<div style='text-align:right;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"**{IDENTIDAD}**")
        st.markdown(f"<h1 style='text-align:center;'>{titulo}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Introducción Automática (Sin errores de SyntaxError)
        intro_texto = "El presente compendio técnico sobre '" + titulo + "' constituye una síntesis rigurosa para la UNAN León."
        st.write(intro_texto)
        
        # LLAMADA AL NUEVO MOTOR (Aquí ocurre la magia)
        renderizar_texto_mixto(cuerpo_doc)

# --- GENERADOR DE LATEX SEGURO (CONCATENACIÓN PURA) ---
if st.button("🚀 Generar Código .tex"):
    # Evitamos f-strings para que las llaves {} no den SyntaxError de nuevo
    cod_tex = r"\documentclass{article}" + "\n" + r"\usepackage[utf8]{inputenc}" + "\n"
    cod_tex += r"\begin{document}" + "\n" + r"\title{" + titulo + "}\n"
    cod_tex += r"\author{" + IDENTIDAD + "}\n" + r"\maketitle" + "\n"
    cod_tex += cuerpo_doc + "\n" + r"\end{document}"
    
    st.code(cod_tex, language="latex")
