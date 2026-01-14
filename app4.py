import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import re
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD (BLINDAJE TOTAL AL INICIO) ---
def obtener_fecha_espanol():
    meses = {"January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto", "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
    ahora = datetime.now()
    return f"{ahora.day} de {meses.get(ahora.strftime('%B'))}, {ahora.year}"

# Definición global para evitar NameError en la vista previa
fecha_actual = obtener_fecha_espanol()
firma_line1 = "Ismael Antonio Cardenas López"
firma_line2 = "Licenciado en Matemática Unan León Nicaragua"

st.set_page_config(page_title="Sistema Ismael Cárdenas - UNAN León", layout="wide")

# --- 2. MOTOR DE REDACCIÓN ACADÉMICA AUTOMÁTICA (ROBUSTA) ---
def generar_prosa_profesional(titulo):
    return {
        "intro": f"El presente compendio técnico, enfocado en '{titulo}', constituye una síntesis rigurosa de los principios analíticos fundamentales. Bajo la autoría del Lic. Ismael Cárdenas López, este documento busca formalizar los conceptos matemáticos mediante un lenguaje axiomático preciso, garantizando la coherencia teórica necesaria para el estudio avanzado en la UNAN León.",
        "conclu": f"Tras la revisión pormenorizada de los elementos que integran '{titulo}', se concluye que la estructuración lógica de los contenidos permite una transición fluida hacia modelos de mayor complejidad. La evidencia analítica aquí expuesta ratifica la validez de los métodos empleados.",
        "recom": "Se recomienda integrar estos resultados en esquemas de resolución de problemas interdisciplinarios. Asimismo, es imperativo mantener un contraste constante entre la abstracción simbólica y su verificación empírica para asegurar la robustez de los modelos presentados."
    }

# --- 3. MOTOR DE ESTILIZADO (CUADROS ELEGANTES Y VIÑETAS LATEX) ---
def renderizar_cuadros_estilizados(texto):
    if not texto: return
    lineas = texto.split('\n')
    for linea in lineas:
        l = linea.strip()
        if not l: continue
        
        # --- DETECCIÓN DE VIÑETAS ELEGANTES ---
        # Si la línea empieza con -, *, • o un patrón de lista (1., a., etc.)
        if l.startswith(('-', '*', '•')) or re.match(r'^[0-9|a-z]\.', l):
            # Limpiamos el marcador original y ponemos el diamante elegante azul
            contenido_v = re.sub(r'^[-*•]|^[0-9|a-z]\.', '', l).strip()
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#1A5276;'>◈</span> {contenido_v}", unsafe_allow_html=True)
            continue

        txt_up = l.upper()
        if any(k in txt_up for k in ["TEOREMA", "PROPOSICIÓN"]):
            st.info(f"✨ **{linea}**") # Azul elegante
        elif any(k in txt_up for k in ["DEFINICIÓN", "CONCEPTO"]):
            st.success(f"📘 **{linea}**") # Verde académico
        elif any(k in txt_up for k in ["EJERCICIO", "EJEMPLO"]):
            st.warning(f"📝 **{linea}**") # Naranja libro
        elif "SOLUCIÓN" in txt_up:
            st.markdown(f"✅ **{linea}**")
        else:
            # Soporte para texto mixto con LaTeX
            if "$" in l:
                partes = re.split(r'(\$.*?\$)', l)
                for p in partes:
                    if p.startswith('$'):
                        st.latex(p.replace('$', ''))
                    else:
                        st.write(p)
            else:
                st.markdown(linea)

# --- 4. LIMPIEZA AGRESIVA PARA WORD ---
def limpiar_para_word(texto):
    if not texto: return ""
    texto = texto.replace("$", "").replace(r"\dots", "...").replace(r"\cdots", "...")
    texto = texto.replace(r"\left", "").replace(r"\right", "").replace(r"\,", " ")
    reemplazos = {
        r"\infty": "infinito", r"\to": "→", r"\alpha": "α", r"\beta": "β",
        r"\epsilon": "ε", r"\\": "\n", r"\times": "x", r"\{": "{", r"\}": "}"
    }
    texto = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'(\1/\2)', texto)
    texto = re.sub(r'\\([a-zA-Z]+)', r'\1', texto)
    for lat, plain in reemplazos.items():
        texto = texto.replace(lat, plain)
    return texto.replace("{", "").replace("}", "").strip()

# --- 5. FOTO CIRCULAR ---
def preparar_foto():
    try:
        img = Image.open("foto.png").convert("RGBA")
    except:
        img = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        ImageDraw.Draw(img).ellipse((0, 0, 400, 400), fill=(26, 82, 118))
    mask = Image.new('L', (400, 400), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 400, 400), fill=255)
    output = ImageOps.fit(img, (400, 400), centering=(0.5, 0.5))
    output.putalpha(mask)
    buf = io.BytesIO(); output.save(buf, format='PNG'); buf.seek(0)
    return buf

# --- 6. INTERFAZ ---
if 'contenido' not in st.session_state: st.session_state.contenido = ""
if 'ejercicios' not in st.session_state: st.session_state.ejercicios = ""

st.title("🎓 Compilador Ismael Cárdenas - UNAN León")
col_in, col_pre = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Insumos Científicos")
    titulo_proy = st.text_input("Tema de la clase:", "Sucesiones y Series parte 1")
    st.session_state.contenido = st.text_area("Contenido (LaTeX):", value=st.session_state.contenido, height=350)
    st.session_state.ejercicios = st.text_area("Ejercicios:", value=st.session_state.ejercicios, height=150)

with col_pre:
    st.subheader("👁️ Vista Previa Institucional")
    textos_pro = generar_prosa_profesional(titulo_proy)
    with st.container(border=True):
        # Cabecera con Foto y Fecha
        c_head1, c_head2 = st.columns([3, 1])
        with c_head1:
            st.markdown(f"<div style='text-align:left;'><b>Fecha:</b> {fecha_actual}</div>", unsafe_allow_html=True)
            st.markdown(f"<b>{firma_line1}</b><br><i>{firma_line2}</i>", unsafe_allow_html=True)
        with c_head2:
            st.image(preparar_foto(), width=90)
        
        st.markdown(f"<h2 style='text-align:center; color:#1A5276;'>{titulo_proy}</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown(f"**I. Introducción**\n\n{textos_pro['intro']}")
        renderizar_cuadros_estilizados(st.session_state.contenido)
        renderizar_cuadros_estilizados(st.session_state.ejercicios)
        st.markdown(f"**IV. Conclusiones**\n\n{textos_pro['conclu']}")
        st.markdown(f"**V. Recomendaciones**\n\n{textos_pro['recom']}")

# --- 7. BOTONES DE COMPILACIÓN ---
st.divider()
if st.button("🚀 Compilar Documentación de Élite"):
    textos_pro = generar_prosa_profesional(titulo_proy)
    
    # --- WORD (LIMPIEZA TOTAL Y FOTO) ---
    doc = Document()
    head = doc.add_table(rows=1, cols=2)
    head.cell(0,0).text = f"{fecha_actual}\n{firma_line1}\n{firma_line2}"
    p_img = head.cell(0,1).add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_img.add_run().add_picture(preparar_foto(), width=Inches(0.9))
    
    doc.add_heading(titulo_proy, 0).alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    secciones_w = [
        ("I. Introducción", textos_pro['intro']),
        ("II. Contenido", st.session_state.contenido),
        ("III. Ejercicios", st.session_state.ejercicios),
        ("IV. Conclusiones", textos_pro['conclu']),
        ("V. Recomendaciones", textos_pro['recom'])
    ]
    
    for t, c in secciones_w:
        doc.add_heading(t, 1)
        doc.add_paragraph(limpiar_para_word(c))

    w_io = io.BytesIO(); doc.save(w_io); w_io.seek(0)
    st.download_button("⬇️ Descargar Word (Limpio)", w_io, f"{titulo_proy}.docx")

    # --- LATEX (ROBUSTO OVERLEAF) ---
    latex_overleaf = f"\\documentclass[12pt]{{article}}\\usepackage[spanish]{{babel}}\\usepackage{{amsmath,amssymb,tcolorbox}}\\title{{{titulo_proy}}}\\author{{{firma_line1}}}\\begin{{document}}\\maketitle\\section{{Introducción}}{textos_pro['intro']}\\section{{Desarrollo}}{st.session_state.contenido}\\section{{Ejercicios}}{st.session_state.ejercicios}\\section{{Conclusiones}}{textos_pro['conclu']}\\section{{Recomendaciones}}{textos_pro['recom']}\\end{{document}}"
    st.download_button("⬇️ Descargar LaTeX (Overleaf)", latex_overleaf, f"{titulo_proy}.tex")
    st.success("¡Compilación finalizada con éxito!")
