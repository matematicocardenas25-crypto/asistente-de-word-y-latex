import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD (FIJA Y SEGURA) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

# Variables de identidad globales para evitar NameError
fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso, garantizando la coherencia teórica necesaria para el estudio avanzado en la UNAN León.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución de problemas interdisciplinarios para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR DE VISTA PREVIA CON CUADROS ESTILIZADOS ---
def renderizar_cuadros_previa(texto):
    lineas = texto.split('\n')
    for linea in lineas:
        if not linea.strip(): continue
        up = linea.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN", "LEMA"]):
            st.info(f"📜 **{linea}**") # Cuadro Azul
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea}**") # Cuadro Verde
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{linea}**") # Cuadro Naranja
        elif "SOLUCIÓN" in up:
            st.markdown(f"✅ **{linea}**")
        else:
            st.latex(linea) if "$" in linea else st.markdown(linea)

# --- 4. GESTIÓN DE IMAGEN CIRCULAR ---
def preparar_foto():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        ImageDraw.Draw(img).ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO(); output.save(buf, format='PNG'); buf.seek(0)
    return buf

# --- 5. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador LaTeX Profesional - Lic. Ismael Cárdenas")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Tema del Documento", "Sucesiones y Series")
    st.session_state.contenido = st.text_area("Contenido Matemático (LaTeX puro):", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Ejercicios y Soluciones:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Estilo Libro")
    textos = generar_prosa_profesional(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"**Introducción:**\n{textos['intro']}")
        renderizar_cuadros_previa(st.session_state.contenido)
        renderizar_cuadros_previa(st.session_state.ejercicios)

# --- 6. GENERACIÓN DE CÓDIGO LATEX (CON TODOS LOS FIERROS) ---
if st.button("🚀 Generar Código LaTeX para Overleaf"):
    textos = generar_prosa_profesional(titulo_proy)
    
    latex_final = f"""% Compilador Profesional Ismael Cardenas - UNAN LEON
\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, amssymb, amsthm, amsfonts}}
\\usepackage{{tcolorbox}} % Para los cuadros elegantes
\\usepackage{{pgfplots}} % Para gráficas matemáticas
\\usepackage{{geometry}}
\\usepackage{{fancyhdr}}
\\geometry{{margin=1in}}
\\pgfplotsset{{compat=1.18}}

% Definición de colores y cuadros elegantes
\\newtcolorbox{{teorema}}[1]{{colback=blue!5!white,colframe=blue!75!black,fonttitle=\\bfseries,title=#1}}
\\newtcolorbox{{definicion}}[1]{{colback=green!5!white,colframe=green!75!black,fonttitle=\\bfseries,title=#1}}

\\title{{\\textbf{{{titulo_proy}}}}}
\\author{{{firma_line1} \\\\ \\small {firma_line2}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{textos['intro']}

\\section{{Desarrollo del Tema}}
{st.session_state.contenido}

\\section{{Ejercicios Propuestos}}
{st.session_state.ejercicios}

\\section{{Conclusiones}}
{textos['conclu']}

\\section{{Recomendaciones}}
{textos['recom']}

\\end{{document}}"""

    st.download_button("⬇️ Descargar Archivo .tex", latex_final, f"{titulo_proy}.tex")
    st.code(latex_final, language='latex')
    st.success("¡Código generado! Cópialo y pégalo en Overleaf para un acabado de libro profesional.")
