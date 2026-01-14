import streamlit as st
import re
from datetime import datetime

# 1. Configuración de Identidad (Sin imágenes para evitar errores de servidor)
FECHA_HOY = datetime.now().strftime("%d de %m, %Y")
IDENTIDAD = "Ismael Antonio Cardenas López - Lic. en Matemática (UNAN León)"

st.set_page_config(page_title="Compilador Ismael", layout="wide")

# 2. Motor "Antipego": Separa texto de fórmulas automáticamente
def mostrar_contenido_profesional(texto):
    if not texto: return
    # Dividimos por líneas para evitar que el texto se amontone
    lineas = texto.split('\n')
    for linea in lineas:
        if not linea.strip(): continue
        
        # Si la línea tiene símbolos de dólar, la tratamos con cuidado
        if "$" in linea:
            partes = linea.split("$")
            for i, p in enumerate(partes):
                if i % 2 == 1: # Es contenido entre $$
                    st.latex(p.strip())
                else: # Es texto normal
                    if p.strip(): st.write(p.strip())
        else:
            # Detectar si es un título de Teorema o Ejemplo
            if any(k in linea.upper() for k in ["TEOREMA", "EJEMPLO", "DEFINICIÓN"]):
                st.info(f"📘 {linea}")
            else:
                st.write(linea)

# 3. Interfaz
st.title("🎓 Sistema de Redacción Académica")

tema = st.text_input("Título:", "Sucesiones y Series")
cuerpo = st.text_area("Escribe aquí (Usa $ para fórmulas):", height=250)

if st.button("Visualizar Formato Académico"):
    # Introducción Automática (Prosa elegante)
    intro = f"El presente estudio sobre '{tema}' constituye una síntesis formal realizada por el Lic. Ismael Cárdenas para la UNAN León, Nicaragua."
    
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"**{IDENTIDAD}**")
        st.markdown(f"<h1 style='text-align:center;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader("I. Introducción")
        st.write(intro)
        
        st.subheader("II. Desarrollo")
        mostrar_contenido_profesional(cuerpo)

# 4. Generador de LaTeX (Sin usar f-strings para evitar el SyntaxError)
if st.button("Generar Código .tex"):
    # Concatenación pura para que las llaves de LaTeX no choquen con Python
    codigo_tex = r"\documentclass{article}" + "\n" + r"\begin{document}" + "\n"
    codigo_tex += r"\section{Introducción}" + "\n" + intro + "\n"
    codigo_tex += r"\section{Contenido}" + "\n" + cuerpo + "\n"
    codigo_tex += r"\end{document}"
    
    st.code(codigo_tex, language="latex")
