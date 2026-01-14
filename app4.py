import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y CONFIGURACIÓN (INVICTO CONTRA ERRORES) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

# Variables estables para evitar NameError y SyntaxError
FECHA_HOY = obtener_fecha_espanol()
NOMBRE_AUTOR = "Ismael Antonio Cardenas López"
CARGO_AUTOR = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMÁTICA ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico sobre '{titulo}' constituye una sistematización rigurosa de los fundamentos analíticos de la materia. Bajo la autoría del Lic. Ismael Cárdenas López, este documento formaliza los conceptos mediante un lenguaje axiomático preciso para la UNAN León.",
        "conclu": "Se ratifica que la estructuración lógica de los contenidos expuestos permite una resolución eficaz de problemas complejos. La rigurosidad analítica aquí presentada es la base para el desarrollo del pensamiento matemático avanzado.",
        "recom": "Se recomienda profundizar en la revisión de los marcos teóricos aquí abordados y aplicar estos modelos en entornos de investigación interdisciplinaria."
    }

# --- 3. MOTOR DE ESTILIZADO ROBUSTO (CUADROS Y VIÑETAS) ---
def renderizar_todo_elegante(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # A. DETECCIÓN DE VIÑETAS (Listas elegantes)
        if l.startswith(('-', '*', '•')) or re.match(r'^[a-z|0-9]\.', l):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {l.lstrip('-*•')}")
            continue

        # B. CUADROS DE LIBRO (Teoremas, Definiciones, Ejercicios)
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{l}**") # Cuadro Azul
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**") # Cuadro Verde
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**") # Cuadro Naranja
        elif "SOLUCIÓN" in up:
            st.markdown(f"✅ **{l}**")
        else:
            # C. RENDERIZADO DE MATEMÁTICAS (Limpio)
            if "$" in l:
                st.latex(l.replace("$", ""))
            else:
                st.write(l)

# --- 4. INTERFAZ ---
st.title("🎓 Compilador Académico Ismael Cárdenas")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Datos")
    titulo_tema = st.text_input("Tema de la clase:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Contenido Teórico (LaTeX):", value=st.session_state.desarrollo, height=350)
    st.session_state.ejercicios = st.text_area("Sección de Práctica:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Estilo Libro")
    textos_auto = generar_prosa_profesional(titulo_tema)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo_tema}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{NOMBRE_AUTOR}</b><br><i>{CARGO_AUTOR}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### I. Introducción\n{textos_auto['intro']}")
        renderizar_todo_elegante(st.session_state.desarrollo)
        renderizar_todo_elegante(st.session_state.ejercicios)
        st.markdown(f"### IV. Conclusiones\n{textos_auto['conclu']}")

# --- 5. GENERADOR DE CÓDIGO LATEX (FIERROS COMPLETOS) ---
if st.button("🚀 Compilar Código LaTeX de Élite"):
    textos_auto = generar_prosa_profesional(titulo_tema)
    
    # Construcción por bloques para evitar error de llaves
    preambulo = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[spanish]{babel}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, amsthm, amsfonts, tcolorbox, geometry}
\geometry{margin=1in}
\newtcolorbox{estilo_libro}[2]{colback=#1!5!white,colframe=#1!75!black,fonttitle=\bfseries,title=#2}
"""
    cuerpo = f"""\\begin{{document}}
\\begin{{flushright}} {FECHA_HOY} \\end{{flushright}}
\\begin{{center}}
    {{\\Huge \\textbf{{{titulo_tema}}}}} \\\\[0.5cm]
    {{\\large \\textbf{{{NOMBRE_AUTOR}}} \\\\ \\textit{{{CARGO_AUTOR}}}}}
\\end{{center}}

\\section{{Introducción}}
{textos_auto['intro']}

\\section{{Desarrollo}}
{st.session_state.desarrollo}

\\section{{Ejercicios}}
{st.session_state.ejercicios}

\\section{{Conclusiones}}
{textos_auto['conclu']}

\\end{{document}}"""

    latex_final = preambulo + cuerpo
    st.download_button("⬇️ Descargar .tex", latex_final, f"{titulo_tema}.tex")
    st.code(latex_final, language='latex')
    st.success("¡Documento listo para Overleaf!")
