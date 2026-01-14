import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
from datetime import datetime

# --- 1. CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

def obtener_fecha():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha()
firma_full = "Ismael Antonio Cardenas López"
firma_cargo = "Licenciado en Matemática Unan León Nicaragua"

# --- 2. MOTOR DE REDACCIÓN ROBUSTA ---
def generar_textos_academicos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística del fenómeno estudiado, estableciendo una base sólida para el pensamiento lógico matemático avanzado.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica, fomentando la aplicación de estos marcos teóricos en contextos interdisciplinarios."
    }

# --- 3. PROCESADORES DE ESTILO (VISTA PREVIA Y LATEX) ---
def renderizar_vista_previa(texto):
    for linea in texto.split('\n'):
        if not linea.strip(): continue
        up = linea.upper()
        if any(k in up for k in ["TEOREMA", "AXIOMA", "PROPOSICIÓN"]): st.info(f"✨ **{linea}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]): st.success(f"📘 **{linea}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]): st.warning(f"📝 **{linea}**")
        elif "SOLUCIÓN" in up or "SOLUCION" in up: st.markdown(f"✅ *{linea}*")
        else: st.write(linea)

def procesar_a_latex(texto):
    resultado = []
    for l in texto.split('\n'):
        if not l.strip(): continue
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "AXIOMA"]): resultado.append(f"\\begin{{teorema_box}} {l} \\end{{teorema_box}}")
        elif "DEFINICIÓN" in up: resultado.append(f"\\begin{{definicion_box}} {l} \\end{{definicion_box}}")
        elif "EJERCICIO" in up: resultado.append(f"\\begin{{ejercicio_box}} {l} \\end{{ejercicio_box}}")
        elif "SOLUCIÓN" in up: resultado.append(f"\\begin{{solucion_box}} {l} \\end{{solucion_box}}")
        else: resultado.append(l)
    return "\n".join(resultado)

# --- 4. INTERFAZ ---
st.title("🎓 Sistema de Documentación - Lic. Ismael Cárdenas")

tema = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    teoria = st.text_area("Desarrollo Teórico:", height=200)
    ejercicios = st.text_area("Ejercicios y Soluciones:", height=150)

# --- 5. GENERACIÓN AUTOMÁTICA DE CONTENIDO ROBUSTO ---
textos_robustos = generar_textos_academicos(tema)

with col_pre:
    st.subheader("👁️ Vista Previa de Élite")
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{tema}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_full}</b><br>{firma_cargo}</p>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("### I. Introducción")
        st.write(textos_robustos['intro'])
        
        st.markdown("### II. Contenido")
        renderizar_vista_previa(teoria)
        
        st.markdown("### III. Ejercicios")
        renderizar_vista_previa(ejercicios)
        
        st.success(f"**IV. Conclusiones Robustas**\n\n{textos_robustos['conclu']}")
        st.info(f"**V. Recomendaciones Robustas**\n\n{textos_robustos['recom']}")

# --- 6. BOTONES DE DESCARGA CON CONTENIDO REAL ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    # Generar Word en memoria
    doc = Document()
    doc.add_paragraph(fecha_actual).alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.add_heading(tema, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{firma_full}\n{firma_cargo}").alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading("I. Introducción", 1); doc.add_paragraph(textos_robustos['intro'])
    doc.add_heading("II. Contenido", 1); doc.add_paragraph(teoria)
    doc.add_heading("III. Conclusiones", 1); doc.add_paragraph(textos_robustos['conclu'])
    
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word Completo", w_io, f"{tema}.docx", key="dw_w")

with c2:
    # Generar LaTeX en memoria
    tex_body = procesar_a_latex(teoria)
    tex_ex = procesar_a_latex(ejercicios)
    latex_final = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, amsfonts}} 
\\usepackage[most]{{tcolorbox}}
\\geometry{{margin=1in}}

\\newtcolorbox{{teorema_box}}{{colback=blue!5, colframe=blue!75!black, title=TEOREMA, arc=4pt}}
\\newtcolorbox{{definicion_box}}{{colback=green!5, colframe=green!50!black, title=DEFINICIÓN, arc=4pt}}
\\newtcolorbox{{ejercicio_box}}{{colback=orange!5, colframe=orange!75!black, title=EJERCICIO, arc=4pt}}
\\newtcolorbox{{solucion_box}}{{colback=gray!10, colframe=black, title=SOLUCIÓN, arc=4pt}}

\\title{{\\textbf{{{tema}}}}}
\\author{{{firma_full} \\\\ \\small {firma_cargo}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos_robustos['intro']}
\\section{{Desarrollo}} {tex_body}
\\section{{Ejercicios}} {tex_ex}
\\section{{Conclusiones}} {textos_robustos['conclu']}
\\section{{Recomendaciones}} {textos_robustos['recom']}
\\end{{document}}"""
    
    st.download_button("⬇️ Descargar LaTeX Completo", latex_final, f"{tema}.tex", key="dw_t")
