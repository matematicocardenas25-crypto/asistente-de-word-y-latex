import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD (FIJA Y SEGURA) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

# Variables globales para evitar NameError
FECHA_ACTUAL = obtener_fecha_espanol()
FIRMA_NOMBRE = "Ismael Antonio Cardenas López"
FIRMA_CARGO = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMATIZADA ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso, garantizando la coherencia teórica necesaria para el estudio avanzado en la UNAN León.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución de problemas interdisciplinarios para potenciar el alcance del análisis matemático."
    }

# --- 3. MOTOR DE VISTA PREVIA (CORREGIDO PARA EVITAR DELTAGENERATOR ERROR) ---
def renderizar_bloques_previa(texto):
    if not texto:
        return
    lineas = texto.split('\n')
    for linea in lineas:
        if not linea.strip(): 
            continue
        
        up = linea.upper()
        # Detección de palabras clave para cuadros elegantes
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN", "LEMA"]):
            st.info(f"📜 **{linea}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{linea}**")
        elif "SOLUCIÓN" in up:
            st.write(f"✅ **{linea}**")
        else:
            # Si contiene símbolos matemáticos, intentamos renderizar con st.latex
            if "$" in linea:
                # Limpiamos los $ para que st.latex no falle
                limpia = linea.replace("$", "")
                st.latex(limpia)
            else:
                st.markdown(linea)

# --- 4. GESTIÓN DE IMAGEN CIRCULAR ---
def preparar_foto():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    
    mask = Image.new('L', (400, 400), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 400, 400), fill=255)
    
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- 5. INTERFAZ ---
st.title("🎓 Compilador LaTeX de Élite - Lic. Ismael Cárdenas")

if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Sucesiones y Series parte 1")
    st.session_state.contenido = st.text_area("Desarrollo Matemático (LaTeX):", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Sección de Ejercicios:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Académica")
    textos_pro = generar_prosa_profesional(titulo_proy)
    with st.container(border=True):
        # Encabezado manual para la vista previa
        st.markdown(f"<div style='text-align:right;'>{FECHA_ACTUAL}</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{titulo_proy}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{FIRMA_NOMBRE}</b><br><i>{FIRMA_CARGO}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"### I. Introducción\n{textos_pro['intro']}")
        st.markdown("### II. Desarrollo")
        renderizar_bloques_previa(st.session_state.contenido)
        st.markdown("### III. Ejercicios")
        renderizar_bloques_previa(st.session_state.ejercicios)
        st.markdown(f"### IV. Conclusiones\n{textos_pro['conclu']}")

# --- 6. GENERACIÓN DE CÓDIGO LATEX PROFESIONAL ---
if st.button("🚀 Generar Código LaTeX para Overleaf"):
    textos_pro = generar_prosa_profesional(titulo_proy)
    
    codigo_latex = f"""% Compilador Académico Ismael Cardenas - UNAN LEON
\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath, amssymb, amsthm, amsfonts}}
\\usepackage{{tcolorbox}} % Cuadros de colores para teoremas
\\usepackage{{pgfplots}} % Gráficas matemáticas profesionales
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\pgfplotsset{{compat=1.18}}

% Estilos de cuadros elegantes
\\newtcolorbox{{mybox}}[2]{{colback=#1!5!white,colframe=#1!75!black,fonttitle=\\bfseries,title=#2}}

\\title{{\\Huge \\textbf{{{titulo_proy}}}}}
\\author{{\\textbf{{{FIRMA_NOMBRE}}} \\\\ \\small {FIRMA_CARGO}}}
\\date{{{FECHA_ACTUAL}}}

\\begin{{document}}
\\maketitle

\\section{{Introducción}}
{textos_pro['intro']}

\\section{{Desarrollo Teórico}}
{st.session_state.contenido}

\\section{{Ejercicios y Aplicaciones}}
{st.session_state.ejercicios}

\\section{{Conclusiones}}
{textos_pro['conclu']}

\\section{{Recomendaciones}}
{textos_pro['recom']}

\\end{{document}}
"""
    st.download_button("⬇️ Descargar Archivo .tex", codigo_latex, f"{titulo_proy}.tex")
    st.code(codigo_latex, language='latex')
    st.success("¡Código generado con éxito! Todo listo para Overleaf.")
