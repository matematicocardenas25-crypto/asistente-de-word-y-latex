import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
import re
from datetime import datetime
from fpdf import FPDF # Librería para generar el PDF

# --- 1. CONFIGURACIÓN DE IDENTIDAD Y FECHA ---
def obtener_fecha():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

FECHA_TEXTO = obtener_fecha()
AUTOR = "Ismael Antonio Cardenas López"
INFO_AUTOR = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas", layout="wide")

# --- 2. CLASE PARA GENERAR EL PDF ELEGANTE ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, f'Fecha: {FECHA_TEXTO}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- 3. MOTOR DE RENDERIZADO (VISTA PREVIA) ---
def mostrar_contenido_estilizado(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # Detección de Viñetas
        if l.startswith(('-', '*', '•')) or re.match(r'^[0-9|a-z]\.', l):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;◈ {l.lstrip('-*•')}")
            continue

        # Cuadros Académicos
        up = l.upper()
        if any(k in up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"📜 **{l}**")
        elif any(k in up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{l}**")
        elif any(k in up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"✏️ **{l}**")
        else:
            if "$" in l: st.latex(l.replace("$", ""))
            else: st.write(l)

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🎓 Sistema de Compilación Académica - UNAN León")

if 'txt_teoria' not in st.session_state: st.session_state.txt_teoria = ""
if 'txt_ejercicios' not in st.session_state: st.session_state.txt_ejercicios = ""

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("📥 Insumos del Documento")
    tema = st.text_input("Título del Tema:", "Sucesiones y Series parte 1")
    st.session_state.txt_teoria = st.text_area("Contenido Teórico:", value=st.session_state.txt_teoria, height=300)
    st.session_state.txt_ejercicios = st.text_area("Sección de Ejercicios:", value=st.session_state.txt_ejercicios, height=150)

with col_der:
    st.subheader("👁️ Vista Previa Institucional")
    with st.container(border=True):
        st.markdown(f"<div style='text-align:right;'>{FECHA_TEXTO}</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align:center; color:#1A5276;'>{tema}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'><b>{AUTOR}</b><br><i>{INFO_AUTOR}</i></p>", unsafe_allow_html=True)
        st.markdown("---")
        mostrar_contenido_estilizado(st.session_state.txt_teoria)
        mostrar_contenido_estilizado(st.session_state.txt_ejercicios)

# --- 5. GENERACIÓN DE ARCHIVOS (PDF, LATEX) ---
st.markdown("### 🚀 Exportar Documentación")
c1, c2 = st.columns(2)

with c1:
    if st.button("📄 Generar y Descargar PDF"):
        pdf = PDF()
        pdf.add_page()
        # Título y Autor
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, tema, 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, AUTOR, 0, 1, 'C')
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, INFO_AUTOR, 0, 1, 'C')
        pdf.ln(10)
        # Contenido
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 10, st.session_state.txt_teoria + "\n" + st.session_state.txt_ejercicios)
        
        pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
        st.download_button("⬇️ Descargar PDF Final", data=pdf_output, file_name=f"{tema}.pdf", mime="application/pdf")

with c2:
    # Código LaTeX blindado (usando % para escapar llaves si es necesario)
    latex_code = f"""\\documentclass[12pt]{{article}}
\\usepackage[spanish]{{babel}}
\\usepackage{{amsmath, amssymb, tcolorbox}}
\\title{{{tema}}}
\\author{{{AUTOR} \\\\ \\small {INFO_AUTOR}}}
\\date{{{FECHA_TEXTO}}}
\\begin{{document}}
\\maketitle
\\section{{Contenido}}
{st.session_state.txt_teoria}
\\section{{Ejercicios}}
{st.session_state.txt_ejercicios}
\\end{{document}}"""
    st.download_button("⬇️ Descargar Código .tex", latex_code, file_name=f"{tema}.tex")
