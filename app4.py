import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y CONFIGURACIÓN (BLINDAJE TOTAL) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_HOY = obtener_fecha_espanol()
NOMBRE_DOC = "Ismael Antonio Cardenas López"
CARGO_DOC = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Académico Ismael Cárdenas", layout="wide")

# --- 2. MOTOR DE REDACCIÓN AUTOMÁTICA PROFESIONAL ---
def generar_prosa(titulo):
    return {
        "intro": f"El presente compendio técnico sobre '{titulo}' ha sido desarrollado con el objetivo de formalizar los principios analíticos de la materia. Bajo un enfoque axiomático, se presentan las estructuras fundamentales necesarias para el dominio del cálculo avanzado, cumpliendo con los estándares de excelencia de la UNAN León.",
        "conclu": "Se concluye que la comprensión de estos modelos matemáticos es vital para la resolución de problemas de ingeniería y ciencias exactas. La rigurosidad en la notación asegura una base sólida para estudios posteriores.",
        "recom": "Se recomienda al estudiante profundizar en la práctica de los teoremas expuestos y utilizar software computacional para validar los modelos de convergencia aquí presentados."
    }

# --- 3. MOTOR DE ESTILIZADO (CUADROS, VIÑETAS Y LATEX) ---
def renderizar_contenido_elegante(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Detección de Viñetas (Bullets)
        if l.startswith(('-', '*', '•')) or re.match(r'^[a-z]\.', l):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;🔹 {l.lstrip('-*•')}")
            continue

        # Detección de Cuadros Elegantes
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN", "LEMA"]):
            st.info(f"📜 **{l}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**")
        elif "SOLUCIÓN" in up:
            st.write(f"✅ **{l}**")
        else:
            # Renderizado inteligente de LaTeX
            if "$" in l:
                partes = l.split('$')
                for i, p in enumerate(partes):
                    if i % 2 != 0: st.latex(p)
                    else: st.write(p)
            else:
                st.write(l)

# --- 4. INTERFAZ DE USUARIO ---
st.title("🎓 Compilador de Ingeniería Matemática - Ismael Cárdenas")

if 'desarrollo' not in st.session_state: st.session_state.desarrollo = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_input, col_preview = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Panel de Control")
    titulo = st.text_input("Título del Tema:", "Sucesiones y Series parte 1")
    st.session_state.desarrollo = st.text_area("Contenido Teórico (LaTeX):", value=st.session_state.desarrollo, height=350)
    st.session_state.ejercicios = st.text_area("Práctica y Problemas:", value=st.session_state.ejercicios, height=150)

with col_preview:
    st.subheader("👁️ Vista Previa Académica")
    textos = generar_prosa(titulo)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{FECHA_HOY}</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{NOMBRE_DOC}</b><br><i>{CARGO_DOC}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### I. Introducción\n{textos['intro']}")
        st.markdown("### II. Marco Teórico")
        renderizar_contenido_elegante(st.session_state.desarrollo)
        st.markdown("### III. Ejercicios")
        renderizar_contenido_elegante(st.session_state.ejercicios)
        st.markdown(f"### IV. Conclusiones\n{textos['conclu']}")

# --- 5. BOTÓN DE EXPORTACIÓN (CÓDIGO CON TODOS LOS FIERROS) ---
if st.button("🚀 Generar Código LaTeX de Élite"):
    textos = generar_prosa(titulo)
    codigo_latex = f"""
\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, amssymb, amsthm, amsfonts, tcolorbox, pgfplots, geometry}}
\\geometry{{margin=1in}}
\\pgfplotsset{{compat=1.18}}

% Cuadros estilo libro de texto
\\newtcolorbox{{mybox}}[2]{{colback=#1!5!white,colframe=#1!75!black,fonttitle=\\bfseries,title=#2}}

\\begin{{document}}
\\begin{{flushright}} {FECHA_HOY} \\end{{flushright}}
\\begin{{center}}
    {{\\Huge \\textbf{{{titulo}}}}} \\\\[0.5cm]
    {{\\large \\textbf{{{NOMBRE_DOC}}}} \\\\ \\textit{{{CARGO_DOC}}}}}
\\end{{center}}
\\hr

\\section{{Introducción}}
{textos['intro']}

\\section{{Desarrollo}}
{st.session_state.desarrollo}

\\section{{Ejercicios}}
{st.session_state.ejercicios}

\\section{{Conclusiones}}
{textos['conclu']}

\\end{{document}}
"""
    st.download_button("⬇️ Descargar archivo .tex", codigo_latex, f"{titulo}.tex")
    st.code(codigo_latex, language='latex')
    st.success("¡Documento compilado para Overleaf!")
