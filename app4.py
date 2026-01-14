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
import json
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

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA (CONSERVADO SEGÚN INSTRUCCIONES) ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. MOTOR DE RENDERIZADO PARA VISTA PREVIA (ESTILO LIBRO) ---
def renderizar_vista_previa(texto):
    """Convierte texto plano/LaTeX en HTML con cuadros elegantes para la vista previa."""
    if not texto: return ""
    palabras_clave = ["Teorema", "Axioma", "Lema", "Definición", "Definicion", "Ejercicio", "Ejemplo", "Solución", "Solucion"]
    lineas = texto.split('\n')
    resultado_html = ""
    
    for linea in lineas:
        linea = linea.strip()
        if not linea: continue
        
        # Detectar si la línea es un cuadro
        es_cuadro = any(linea.startswith(pc) for pc in palabras_clave)
        
        if es_cuadro:
            resultado_html += f"""
            <div style="background-color: #F0F7FF; border-left: 5px solid #1A5276; padding: 15px; margin: 10px 0; border-radius: 4px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                <strong style="color: #1A5276;">{linea}</strong>
            </div>
            """
        elif linea.startswith(r"\item") or linea.startswith("•"):
            item_text = linea.replace(r"\item", "").strip()
            resultado_html += f"<li style='margin-left: 20px;'>{item_text}</li>"
        else:
            # Limpieza básica de LaTeX para la web
            linea_limpia = linea.replace("$", "")
            resultado_html += f"<p>{linea_limpia}</p>"
            
    return resultado_html

# --- 4. FUNCIONES DE WORD (SOMBREADO) ---
def sombrear_celda(celda, color_hex):
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color_hex)
    celda._tc.get_or_add_tcPr().append(shading_elm)

def limpiar_para_word(texto):
    if not texto: return ""
    texto = texto.replace(r"\item", "• ")
    texto = texto.replace("$", "").replace(r"\dots", "...").replace(r"\cdots", "...")
    reemplazos = {r"\\left(": "(", r"\\right)": ")", r"\\infty": "infinito", r"\\times": "x", r"\\": ""}
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    return texto.strip()

# --- 5. GESTIÓN DE IMAGEN CIRCULAR ---
def preparar_foto_circular():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- 6. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    st.session_state.contenido = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.contenido, height=300, placeholder="Escriba aquí: Teorema 1: ...")
    st.session_state.ejercicios = st.text_area("Ejercicios Propuestos:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("### 1. Introducción")
        st.write(textos['intro'])
        
        st.markdown("### 2. Desarrollo Teórico")
        st.write(renderizar_vista_previa(st.session_state.contenido), unsafe_allow_html=True)
        
        st.markdown("### 3. Ejercicios Propuestos")
        st.write(renderizar_vista_previa(st.session_state.ejercicios), unsafe_allow_html=True)
        
        st.markdown("### 4. Conclusiones")
        st.write(textos['conclu'])
        
        st.markdown("### 5. Recomendaciones")
        st.write(textos['recom'])

# --- 7. BOTÓN DE COMPILACIÓN ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    doc = Document()
    
    # Encabezado Word
    header_table = doc.add_table(rows=1, cols=2)
    header_table.cell(0, 0).text = fecha_actual
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(1.0))

    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(f"{firma_line1}\n{firma_line2}").alignment = WD_ALIGN_PARAGRAPH.CENTER

    secciones = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios Propuestos", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    palabras_clave = ["Teorema", "Axioma", "Lema", "Definición", "Ejercicio", "Ejemplo", "Solución"]

    for tit, cont in secciones:
        doc.add_heading(tit, 1)
        for linea in cont.split('\n'):
            linea = linea.strip()
            if not linea: continue
            
            if any(linea.startswith(pc) for pc in palabras_clave):
                tabla = doc.add_table(rows=1, cols=1)
                tabla.style = 'Table Grid'
                celda = tabla.rows[0].cells[0]
                sombrear_celda(celda, "EBF5FB") # Azul claro
                p = celda.paragraphs[0]
                run = p.add_run(limpiar_para_word(linea))
                run.bold = True
                run.font.color.rgb = RGBColor(26, 82, 118)
            else:
                p = doc.add_paragraph(limpiar_para_word(linea))
                if "•" in linea or r"\item" in linea:
                    p.paragraph_format.left_indent = Inches(0.3)

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.success("¡Documentación compilada!")
