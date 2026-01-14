import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import matplotlib.pyplot as plt
import numpy as np
import io
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    mes_nombre = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {mes_nombre}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA (ROBUSTO E INALTERABLE) ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. NUEVO MOTOR DE DETECCIÓN INTELIGENTE (WEB / WORD / LATEX) ---
# Palabras clave extendidas para capturar variaciones
KEYWORDS = ["TEOREMA", "AXIOMA", "LEMA", "DEFINICIÓN", "DEFINICION", "EJERCICIO", "EJEMPLO", "SOLUCIÓN", "SOLUCION", "PROPIEDADES"]

def es_estructura_especial(linea):
    linea_up = linea.upper().strip()
    return any(linea_up.startswith(kw) for kw in KEYWORDS)

def renderizar_vista_previa_pro(texto):
    if not texto: return ""
    lineas = texto.split('\n')
    html_out = ""
    for linea in lineas:
        linea_strip = linea.strip()
        if not linea_strip: continue
        
        if es_estructura_especial(linea_strip):
            html_out += f"""
            <div style="background-color: #F4F9FF; border-left: 6px solid #1A5276; padding: 15px; margin: 15px 0; border-radius: 0 8px 8px 0; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                <span style="color: #1A5276; font-weight: bold; font-variant: small-caps; font-size: 1.1em;">{linea_strip}</span>
            </div>
            """
        elif linea_strip.startswith(r"\item") or linea_strip.startswith("●"):
            t = linea_strip.replace(r"\item", "").strip()
            html_out += f"<div style='margin-left: 30px; margin-bottom: 8px;'>● {t}</div>"
        else:
            # Reemplazo básico de LaTeX para visualización limpia
            l = linea_strip.replace("$", "").replace(r"\to", "→").replace(r"\infty", "∞")
            html_out += f"<p style='margin-bottom: 10px;'>{l}</p>"
    return html_out

# --- 4. FUNCIONES DE WORD ---
def sombrear_celda(celda, color_hex):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def limpiar_para_word(texto):
    if not texto: return ""
    texto = texto.replace(r"\item", "● ")
    texto = texto.replace("$", "").replace(r"\dots", "...").replace(r"\infty", "infinito")
    reemplazos = {r"\\left(": "(", r"\\right)": ")", r"\\to": "→", r"\\": ""}
    for lat, plain in reemplazos.items(): texto = texto.replace(lat, plain)
    return texto.strip()

# --- 5. GESTIÓN DE FOTO ---
def preparar_foto_circular():
    try: img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO()
    output.save(buf, format='PNG'); buf.seek(0)
    return buf

# --- 6. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Sucesiones y Series")
    st.session_state.contenido = st.text_area("Cuerpo Teórico:", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        # Encabezado Vista Previa
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br>{firma_line2}</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### I. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### II. Desarrollo Teórico")
        st.markdown(renderizar_vista_previa_pro(st.session_state.contenido), unsafe_allow_html=True)
        
        st.markdown("### III. Conclusiones")
        st.write(textos['conclu'])

# --- 7. COMPILACIÓN ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    doc = Document()
    
    # Word Header
    header_table = doc.add_table(rows=1, cols=2)
    header_table.cell(0, 0).text = fecha_actual
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(0.9))

    doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{firma_line1}\n{firma_line2}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    secciones = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    for tit, cont in secciones:
        doc.add_heading(tit, 1)
        for linea in cont.split('\n'):
            linea = linea.strip()
            if not linea: continue
            
            if es_estructura_especial(linea):
                tabla = doc.add_table(rows=1, cols=1)
                tabla.style = 'Table Grid'
                celda = tabla.rows[0].cells[0]
                sombrear_celda(celda, "F2F9FF")
                p = celda.paragraphs[0]
                run = p.add_run(limpiar_para_word(linea))
                run.bold = True
                run.font.color.rgb = RGBColor(26, 82, 118)
            else:
                p = doc.add_paragraph(limpiar_para_word(linea))
                if "●" in linea: p.paragraph_format.left_indent = Inches(0.3)

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # LATEX MEJORADO
    latex_body = st.session_state.contenido
    for kw in KEYWORDS:
        # Busca la palabra clave y la encierra en un tcolorbox elegante
        latex_body = re.sub(f"(?i)({kw}.*?)(\n|$)", r"\\begin{tcolorbox}[colback=blue!5,colframe=blue!75!black,title=Marco Teórico]\\textbf{\1}\\end{tcolorbox}\n", latex_body)

    latex_code = f"""\\documentclass{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage[most]{{tcolorbox}}
\\title{{{titulo_proy}}}
\\author{{{firma_line1} \\\\ {firma_line2}}}
\\begin{{document}}
\\maketitle
\\section{{I. Introducción}} {textos['intro']}
\\section{{II. Desarrollo}} {latex_body}
\\section{{III. Conclusiones}} {textos['conclu']}
\\end{{document}}"""

    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar Código LaTeX", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documento de Élite Compilado!")
