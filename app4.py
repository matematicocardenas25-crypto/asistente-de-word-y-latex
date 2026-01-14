import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import matplotlib.pyplot as plt
import numpy as np
import io
import json
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD Y FECHA (BLINDADO) ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    mes_nombre = meses.get(ahora.strftime('%B'), ahora.strftime('%B'))
    return f"{ahora.day} de {mes_nombre}, {ahora.year}"

# Variables globales de firma (Esencial para evitar NameError)
fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ROBUSTA ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado y garantizando un rigor académico acorde a los más altos estándares institucionales de la UNAN León.",
        "conclu": f"Tras el análisis pormenorizado de los elementos expuestos en torno a '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados. La evidencia teórica aquí presentada ratifica la importancia de la precisión axiomática en la resolución de problemas complejos.",
        "recom": "Se recomienda encarecidamente someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad. Asimismo, se sugiere profundizar en el estudio de las propiedades intrínsecas de los marcos teóricos aquí abordados, fomentando la aplicación de estos modelos en contextos interdisciplinarios."
    }

# --- 3. MOTOR DE LIMPIEZA TOTAL DE LATEX PARA WORD ---
def limpiar_para_word(texto):
    if not texto: return ""
    # Eliminar símbolos de dólar y delimitadores de código
    texto = texto.replace("$", "").replace(r"\[", "").replace(r"\]", "")
    
    # Reemplazos específicos de comandos que se ven en tus capturas
    reemplazos = {
        r"\dots": "...", r"\cdots": "...", r"\,": " ", r"\\": "\n",
        r"\left\{": "{", r"\right\}": "}", r"\left(": "(", r"\right)": ")",
        r"\left[": "[", r"\right]": "]", r"\infty": "infinito", r"\times": "x"
    }
    
    # Traducir fracciones \frac{a}{b} -> (a/b)
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    # Eliminar cualquier barra invertida residual antes de palabras (ej. \alpha -> alpha)
    texto = re.sub(r'\\([a-zA-Z]+)', r'\1', texto)
    # Limpiar llaves sobrantes de exponentes o subíndices
    texto = texto.replace("{", "").replace("}", "")
    
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
        
    return texto.strip()

# --- 4. GESTIÓN DE IMAGEN CIRCULAR ---
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

# --- 5. INTERFAZ Y VISTA PREVIA ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Sucesiones y Series parte 1")
    st.session_state.contenido = st.text_area("Cuerpo del Contenido (LaTeX):", value=st.session_state.contenido, height=300)
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=150)
    
    # Motor Gráfico
    func_in = st.text_input("Función f(x):", "np.sin(x)")
    buf_graf = io.BytesIO()
    try:
        x = np.linspace(0, 10, 100)
        y = eval(func_in, {"x": x, "np": np})
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(x, y, color='#1A5276'); ax.grid(True, alpha=0.3)
        fig.savefig(buf_graf, format='png'); plt.close(fig); buf_graf.seek(0)
    except: pass

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{firma_line1}</b><br><i>{firma_line2}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"**1. Introducción**\n\n{textos['intro']}")
        st.markdown(f"**2. Desarrollo**\n\n{st.session_state.contenido}")
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)
        st.markdown(f"**3. Ejercicios**\n\n{st.session_state.ejercicios}")
        st.markdown(f"**4. Conclusiones**\n\n{textos['conclu']}")

# --- 6. COMPILACIÓN WORD ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    doc = Document()
    
    # Encabezado con Fecha y Foto Circular
    header_table = doc.add_table(rows=1, cols=2)
    header_table.columns[0].width = Inches(4.5)
    header_table.cell(0, 0).text = fecha_actual
    
    celda_foto = header_table.cell(0, 1).add_paragraph()
    celda_foto.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    celda_foto.add_run().add_picture(preparar_foto_circular(), width=Inches(1.0))

    # Título y Firma
    doc.add_heading('\n' + titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph(firma_line1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2 = doc.add_paragraph(firma_line2)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.runs[0].font.italic = True

    # Secciones con LIMPIEZA AGRESIVA
    secciones = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios Propuestos", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    for tit, cont in secciones:
        doc.add_heading(tit, 1)
        texto_limpio = limpiar_para_word(cont)
        for linea in texto_limpio.split('\n'):
            if linea.strip(): doc.add_paragraph(linea.strip())

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word Final", w_io, f"{titulo_proy}.docx")
    st.success("¡Documento listo!")
