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

# --- CONFIGURACIÓN DE FECHA EN ESPAÑOL ---
def obtener_fecha_espanol():
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    ahora = datetime.now()
    dia = ahora.strftime("%d")
    mes = meses.get(ahora.strftime("%B"), ahora.strftime("%B"))
    anio = ahora.strftime("%Y")
    return f"{dia} de {mes}, {anio}"

fecha_actual = obtener_fecha_espanol()
# Firma en dos líneas exactas
firma_oficial = "Ismael Antonio Cardenas López\nLicenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- MOTOR DE LIMPIEZA PROFUNDA DE LATEX PARA WORD ---
def limpiar_latex_para_word(texto):
    if not texto: return ""
    
    # 1. Eliminar entornos complejos como \begin{...} y \end{...}
    texto = re.sub(r'\\begin\{.*?\}.*?\\end\{.*?\}', '[Ecuación]', texto, flags=re.DOTALL)
    texto = re.sub(r'\\begin\{.*?\}|\\end\{.*?\}', '', texto)
    
    # 2. Limpiar comandos de formato matemático común
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto) # Convierte fracciones a (a/b)
    texto = re.sub(r'\\sqrt\{(.*?)\}', r'sqrt(\1)', texto)         # Convierte raíces
    texto = re.sub(r'\\textbf\{(.*?)\}', r'\1', texto)            # Quita negritas LaTeX
    texto = re.sub(r'\\textit\{(.*?)\}', r'\1', texto)            # Quita cursivas LaTeX
    
    # 3. Eliminar caracteres especiales de escape y símbolos de dólar
    texto = texto.replace('$', '')
    texto = texto.replace('\\\\', '\n')
    texto = texto.replace('\\sum', 'SUMATORIA')
    texto = texto.replace('\\int', 'INTEGRAL')
    texto = texto.replace('\\infty', 'infinito')
    
    # 4. Eliminar barras invertidas restantes de comandos simples (ej. \alpha -> alpha)
    texto = re.sub(r'\\([a-zA-Z]+)', r'\1', texto)
    
    # 5. Limpiar llaves sobrantes
    texto = texto.replace('{', '').replace('}', '')
    
    return texto.strip()

# --- FUNCIÓN PARA IMAGEN CIRCULAR ---
def preparar_imagen_circular():
    try:
        # Intenta cargar 'foto.png'. Si no existe, genera una elegante por defecto
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (500, 500), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, 500, 500), fill=(26, 82, 118)) # Azul institucional
    
    size = (500, 500)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    
    buf = io.BytesIO()
    output.save(buf, format='PNG')
    buf.seek(0)
    return buf

# --- MOTOR DE REDACCIÓN ---
def generar_textos_robustos(titulo):
    return {
        "intro": f"El presente compendio técnico, titulado '{titulo}', constituye una sistematización rigurosa de los fundamentos analíticos y estructurales de las ciencias exactas. Bajo la autoría del Lic. Ismael Cárdenas López, este documento articula la abstracción simbólica con la verificación fenomenológica, estableciendo una base sólida para el pensamiento lógico-matemático avanzado.",
        "conclu": f"Tras el análisis de '{titulo}', se concluye que la convergencia entre el rigor analítico y la modelización computacional permite una comprensión holística de los comportamientos estudiados.",
        "recom": "Se recomienda someter los resultados analíticos a un proceso de contraste crítico frente a modelos de simulación numérica para validar su estabilidad."
    }

# --- LÓGICA DE LA INTERFAZ (Se mantiene igual para no perder nada) ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Científico de Élite - UNAN León")

with st.sidebar:
    st.header("💾 Respaldo de Seguridad")
    if st.button("📥 Crear Punto de Restauración"):
        data_respaldo = {"titulo": "Proyecto", "contenido": st.session_state.contenido, "ejercicios": st.session_state.ejercicios}
        st.download_button("Descargar Respaldo (.json)", json.dumps(data_respaldo), "respaldo_ismael.json")

col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Panel de Insumos")
    titulo_proy = st.text_input("Título del Proyecto", "Análisis y Modelado Matemático")
    cont_input = st.text_area("Cuerpo del Contenido (Soporta LaTeX):", value=st.session_state.contenido, height=350)
    st.session_state.contenido = cont_input
    
    st.subheader("📊 Gráfico")
    func_in = st.text_input("Función f(x):", "np.sin(x) * np.exp(-x/10)")
    buf_graf = io.BytesIO()
    try:
        x_vals = np.linspace(-10, 20, 1000)
        y_vals = eval(func_in, {"x": x_vals, "np": np})
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x_vals, y_vals, color='#1A5276', linewidth=2)
        fig.savefig(buf_graf, format='png', dpi=300); plt.close(fig); buf_graf.seek(0)
    except: pass

    ejer_input = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=200)
    st.session_state.ejercicios = ejer_input

with col_pre:
    st.subheader("👁️ Vista Previa")
    textos = generar_textos_robustos(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align: right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>{firma_oficial.replace(chr(10), '<br>')}</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(st.session_state.contenido)
        if buf_graf.getbuffer().nbytes > 0: st.image(buf_graf)

# --- GENERACIÓN DE DOCUMENTOS ---
if st.button("🚀 Compilar Documentación de Élite"):
    textos = generar_textos_robustos(titulo_proy)
    
    # 1. WORD CON LIMPIEZA Y ELEGANCIA
    doc = Document()
    
    # Imagen circular en la esquina superior derecha
    img_circular = preparar_imagen_circular()
    parrafo_img = doc.add_paragraph()
    parrafo_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_img = parrafo_img.add_run()
    run_img.add_picture(img_circular, width=Inches(1.0))

    # Título
    h = doc.add_heading(titulo_proy, 0)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Firma en dos líneas
    f = doc.add_paragraph()
    f.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_f = f.add_run(firma_oficial)
    run_f.italic = True
    run_f.font.size = Pt(12)
    
    # Fecha
    p_fecha = doc.add_paragraph(f"\nFecha: {fecha_actual}")
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    secciones = [
        ("I. Introducción", textos['intro']),
        ("II. Desarrollo Teórico", st.session_state.contenido),
        ("III. Ejercicios Propuestos", st.session_state.ejercicios),
        ("IV. Conclusiones", textos['conclu']),
        ("V. Recomendaciones", textos['recom'])
    ]

    for tit, cont in secciones:
        doc.add_heading(tit, 1)
        # Aquí ocurre la magia: limpiamos el contenido antes de insertarlo en Word
        cont_limpio = limpiar_latex_para_word(cont)
        for p in cont_limpio.split('\n'):
            if p.strip(): doc.add_paragraph(p.strip())

    if buf_graf.getbuffer().nbytes > 0:
        doc.add_picture(buf_graf, width=Inches(5.5))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    
    # 2. LATEX (Se mantiene el código intacto con sus símbolos originales)
    latex_code = f"\\documentclass{{article}}\n\\usepackage[spanish]{{babel}}\n\\title{{{titulo_proy}}}\n\\author{{{firma_oficial.replace(chr(10), ' \\\\ ')}}}\n\\begin{{document}}\n\\maketitle\n{st.session_state.contenido}\n\\end{{document}}"
    
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")
    st.download_button("⬇️ Descargar LaTeX (Original)", latex_code, f"{titulo_proy}.tex")
    st.success("¡Documentación procesada con éxito!")
