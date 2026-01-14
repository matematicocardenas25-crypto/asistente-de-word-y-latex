import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
from datetime import datetime

# --- 1. IDENTIDAD Y CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Ismael Cárdenas", layout="wide")

def obtener_fecha():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha()
firma_full = "Ismael Antonio Cardenas López"
sub_firma = "Licenciado en Matemática Unan León Nicaragua"

# --- 2. MOTOR DE TEXTOS ROBUSTOS ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica...",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística...",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica..."
    }

# --- 3. PROCESADOR DE BLOQUES (DETECCIÓN DE PALABRAS CLAVE) ---
def procesar_a_latex(texto):
    lineas = texto.split('\n')
    resultado = []
    for l in lineas:
        if not l.strip(): continue
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "AXIOMA", "PROPOSICIÓN"]):
            resultado.append(f"\\begin{{teorema_box}} {l} \\end{{teorema_box}}")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            resultado.append(f"\\begin{{definicion_box}} {l} \\end{{definicion_box}}")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            resultado.append(f"\\begin{{ejercicio_box}} {l} \\end{{ejercicio_box}}")
        elif "SOLUCIÓN" in up or "SOLUCION" in up:
            resultado.append(f"\\begin{{solucion_box}} {l} \\end{{solucion_box}}")
        else:
            resultado.append(l)
    return "\n".join(resultado)

# --- 4. INTERFAZ ---
st.title("🎓 Sistema Académico Ismael Cárdenas - UNAN León")

tema = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")
col_in, col_pre = st.columns([1, 1])

with col_in:
    cuerpo = st.text_area("Desarrollo Teórico (Teoremas, etc.)", height=200)
    ejercicios = st.text_area("Ejercicios y Soluciones", height=150)

# --- 5. GENERACIÓN DE ARCHIVOS (MEMORIA INTERNA) ---
textos = generar_textos_robustos(tema)

# Lógica para Word
doc = Document()
doc.add_paragraph(fecha_actual).alignment = WD_ALIGN_PARAGRAPH.RIGHT
doc.add_heading(tema, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph(f"{firma_full}\n{sub_firma}").alignment = WD_ALIGN_PARAGRAPH.CENTER
doc.add_heading("I. Introducción", 1)
doc.add_paragraph(textos['intro'])
doc.add_heading("II. Desarrollo", 1)
doc.add_paragraph(cuerpo)
doc.add_heading("IV. Conclusiones", 1)
doc.add_paragraph(textos['conclu'])

w_io = io.BytesIO()
doc.save(w_io)
w_io.seek(0)

# Lógica para LaTeX
cuerpo_tex = procesar_a_latex(cuerpo)
ejercicios_tex = procesar_a_latex(ejercicios)
latex_code = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, amsfonts}} 
\\usepackage[most]{{tcolorbox}}
\\geometry{{margin=1in}}

\\newtcolorbox{{teorema_box}}{{colback=blue!5, colframe=blue!75!black, arc=4pt, fontupper=\\bfseries}}
\\newtcolorbox{{definicion_box}}{{colback=green!5, colframe=green!50!black, arc=4pt}}
\\newtcolorbox{{ejercicio_box}}{{colback=orange!5, colframe=orange!75!black, arc=4pt}}
\\newtcolorbox{{solucion_box}}{{colback=gray!10, colframe=black, arc=4pt}}

\\title{{\\textbf{{{tema}}}}}
\\author{{{firma_full} \\\\ \\small {sub_firma}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Contenido}} {cuerpo_tex}
\\section{{Ejercicios}} {ejercicios_tex}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}"""

# --- 6. MENÚ DE DESCARGA CON VISTA PREVIA ---
with col_pre:
    st.subheader("👁️ Vista Previa")
    with st.container(border=True):
        st.markdown(f"**{tema}**")
        st.caption(f"{firma_full} - {fecha_actual}")
        st.write(textos['intro'])
        # (Aquí podrías poner la función renderizar_estilos para ver colores)
    
    st.divider()
    st.download_button("⬇️ Descargar Word (.docx)", w_io, f"{tema}.docx", key="word_final")
    st.download_button("⬇️ Descargar LaTeX (.tex)", latex_code, f"{tema}.tex", key="latex_final")
