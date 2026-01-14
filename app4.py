import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re
from datetime import datetime

# --- 1. IDENTIDAD Y FECHA ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

# --- 2. MOTOR DE REDACCIÓN ROBUSTA ---
def generar_textos_academicos(titulo):
    return {
        "intro": f"El presente compendio técnico constituye una sistematización rigurosa de los fundamentos analíticos de '{titulo}'. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica...",
        "conclu": f"Tras el análisis exhaustivo de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización permite una comprensión holística...",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica..."
    }

# --- 3. PROCESADOR DE BLOQUES PARA LATEX ---
def procesar_a_latex(texto):
    lineas = texto.split('\n')
    resultado = []
    for linea in lineas:
        l = linea.strip()
        if not l: continue
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
titulo_proy = st.text_input("Tema de la clase", "Sucesiones y Series parte 1")
contenido = st.text_area("Cuerpo del Tema:", height=200)
ejercicios = st.text_area("Ejercicios y Soluciones:", height=150)

# --- 5. GENERACIÓN Y MENÚS SEPARADOS ---
if st.button("🚀 Compilar Documentación de Élite", key="btn_main"):
    textos = generar_textos_academicos(titulo_proy)
    
    # --- MENÚ WORD ---
    with st.expander("📝 MENÚ WORD (Configuración Final)", expanded=True):
        doc = Document()
        # Imagen circular y fecha
        head = doc.add_table(rows=1, cols=2)
        head.cell(0,0).text = fecha_actual
        # (Aquí va tu lógica de foto circular para Word)
        
        doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph(f"{firma_line1}\n{firma_line2}").alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Secciones Robustas
        for t, c in [("I. Introducción", textos['intro']), ("II. Contenido", contenido), 
                     ("III. Ejercicios", ejercicios), ("IV. Conclusiones", textos['conclu']), 
                     ("V. Recomendaciones", textos['recom'])]:
            doc.add_heading(t, 1)
            doc.add_paragraph(c)

        w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
        st.download_button("⬇️ Descargar Word", w_io, f"{titulo_proy}.docx", key="dl_word")

    # --- MENÚ LATEX ---
    with st.expander("⚛️ MENÚ LATEX (Código para Overleaf)", expanded=True):
        cuerpo_tex = procesar_a_latex(contenido)
        ejercicios_tex = procesar_a_latex(ejercicios)
        
        latex_final = f"""\\documentclass[12pt, letterpaper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, amsfonts}} % CORREGIDO: amsfonts
\\usepackage[most]{{tcolorbox}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}

% ESTILOS DE COLORES LLAMATIVOS
\\newtcolorbox{{teorema_box}}{{colback=blue!5, colframe=blue!75!black, title=TEOREMA/AXIOMA, arc=4pt}}
\\newtcolorbox{{definicion_box}}{{colback=green!5, colframe=green!50!black, title=DEFINICIÓN, arc=4pt}}
\\newtcolorbox{{ejercicio_box}}{{colback=orange!5, colframe=orange!75!black, title=EJERCICIO, arc=4pt}}
\\newtcolorbox{{solucion_box}}{{colback=gray!10, colframe=black, title=SOLUCIÓN, arc=4pt}}

\\title{{\\textbf{{{titulo_proy}}}}}
\\author{{{firma_line1} \\\\ \\small {firma_line2}}}
\\date{{{fecha_actual}}}

\\begin{{document}}
\\maketitle
\\section{{Introducción}} {textos['intro']}
\\section{{Contenido}} {cuerpo_tex}
\\section{{Ejercicios}} {ejercicios_tex}
\\section{{Conclusiones}} {textos['conclu']}
\\section{{Recomendaciones}} {textos['recom']}
\\end{{document}}
"""
        st.code(latex_final, language="latex")
        st.download_button("⬇️ Descargar .TEX", latex_final, f"{titulo_proy}.tex", key="dl_latex")
