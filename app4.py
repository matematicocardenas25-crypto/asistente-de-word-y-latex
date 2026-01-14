import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso para la UNAN León.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica permite una transición fluida hacia modelos de mayor complejidad."
    }

# --- 3. MOTOR DE RENDERIZADO (VIÑETAS Y CUADROS) ---
def renderizar_cuadros_estilizados(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Viñetas elegantes de diamante
        if l.startswith(('-', '*', '•')) or re.match(r'^[0-9|a-z]\.', l):
            contenido = re.sub(r'^[-*•]|^[0-9|a-z]\.', '', l).strip()
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#1A5276;'>◈</span> {contenido}", unsafe_allow_html=True)
            continue

        txt_up = l.upper()
        if any(k in txt_up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"✨ **{l}**")
        elif any(k in txt_up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
        elif any(k in txt_up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"📝 **{l}**")
        else:
            if "$" in l:
                partes = re.split(r'(\$.*?\$)', l)
                for p in partes:
                    if p.startswith('$'): st.latex(p.replace('$', ''))
                    else: st.write(p)
            else:
                st.write(l)

# --- 4. FOTO CIRCULAR ---
def preparar_foto():
    try: img = Image.open("foto.png").convert("RGBA")
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
st.title("🎓 Compilador Ismael Cárdenas - UNAN León")
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos Científicos")
    titulo_proy = st.text_input("Tema:", "Sucesiones")
    contenido = st.text_area("Contenido (LaTeX):", height=300)
    ejercicios = st.text_area("Ejercicios:", height=150)

with col_pre:
    st.subheader("👁️ Vista Previa")
    textos_pro = generar_prosa_profesional(titulo_proy)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{fecha_actual}</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown(f"**I. Introducción**\n\n{textos_pro['intro']}")
        renderizar_cuadros_estilizados(contenido)
        renderizar_cuadros_estilizados(ejercicios)

# --- 6. BOTONES DE DESCARGA ---
st.divider()
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🚀 Generar PDF Profesional"):
        st.info("Para PDF: En la vista previa, presiona Ctrl+P y elige 'Guardar como PDF'. El sistema está optimizado para que el diseño se mantenga exacto.")

with c2:
    # Lógica de Word abreviada
    doc = Document()
    doc.add_heading(titulo_proy, 0)
    doc.add_paragraph(textos_pro['intro'])
    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word", w_io, f"{titulo_proy}.docx")

with c3:
    latex_code = f"\\documentclass{{article}}\\begin{{document}}\\title{{{titulo_proy}}}\\maketitle{contenido}\\end{{document}}"
    st.download_button("⬇️ Descargar LaTeX", latex_code, f"{titulo_proy}.tex")
