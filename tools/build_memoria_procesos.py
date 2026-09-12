#!/usr/bin/env python3
"""Genera la memoria PDF autocontenida del examen de Procesos Estocásticos."""

from __future__ import annotations

import argparse

from pathlib import Path
from xml.sax.saxutils import escape

from openpyxl import load_workbook
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "entrega-2-procesos-estocasticos"
OUT = PROC / "output" / "memoria_detallada.pdf"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--matriz-operativa", action="store_true",
                    help="Usar la matriz corregida del Excel entregado en lugar del adjunto original.")
args = parser.parse_args()

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F75B5")
LIGHT_BLUE = colors.HexColor("#D9EAF7")
GREEN = colors.HexColor("#E2F0D9")
GOLD = colors.HexColor("#FFF2CC")
LIGHT = colors.HexColor("#F3F6F9")
GRAY = colors.HexColor("#475569")
RULE = colors.HexColor("#CBD5E1")


def register_fonts():
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DV"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DV-Bold"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DV-Italic"),
    ]
    for path, name in candidates:
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-Bold", italic="DV-Italic")


register_fonts()
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", fontName="DV-Bold", fontSize=25, leading=31,
    textColor=NAVY, alignment=TA_CENTER, spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName="DV", fontSize=13, leading=19,
    textColor=GRAY, alignment=TA_CENTER, spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="H1x", parent=styles["Heading1"], fontName="DV-Bold", fontSize=18,
    leading=23, textColor=NAVY, spaceBefore=2, spaceAfter=12, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H2x", parent=styles["Heading2"], fontName="DV-Bold", fontSize=13,
    leading=17, textColor=BLUE, spaceBefore=10, spaceAfter=6, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Bodyx", parent=styles["BodyText"], fontName="DV", fontSize=9.2,
    leading=13.4, alignment=TA_JUSTIFY, textColor=colors.HexColor("#1E293B"),
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Smallx", parent=styles["BodyText"], fontName="DV", fontSize=7.5,
    leading=10.2, textColor=GRAY, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["BodyText"], fontName="DV-Bold", fontSize=7.5,
    leading=10.2, textColor=colors.white, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="Bulletx", parent=styles["BodyText"], fontName="DV", fontSize=9,
    leading=13, leftIndent=14, firstLineIndent=-8, bulletIndent=4, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Formula", parent=styles["BodyText"], fontName="DV", fontSize=10.2,
    leading=15, alignment=TA_CENTER, textColor=NAVY, spaceBefore=4, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["BodyText"], fontName="DV-Italic", fontSize=7.4,
    leading=10, alignment=TA_CENTER, textColor=GRAY, spaceBefore=4, spaceAfter=8,
))


class MemoryDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm,
            topMargin=1.7 * cm, bottomMargin=1.6 * cm,
            title="MEFC 2026 - Memoria de Procesos Estocásticos",
            author="Grupo MEFC 2026",
            subject="Resolución auditada de los ejercicios de Procesos Estocásticos",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="normal", frames=[frame], onPage=self._page))
        self._bookmark_id = 0

    def _page(self, canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.line(self.leftMargin, A4[1] - 1.18 * cm, A4[0] - self.rightMargin, A4[1] - 1.18 * cm)
            canvas.setFont("DV", 7.2)
            canvas.setFillColor(GRAY)
            canvas.drawString(self.leftMargin, A4[1] - 0.88 * cm, "MEFC 2026 · Procesos estocásticos")
            canvas.drawRightString(A4[0] - self.rightMargin, 0.82 * cm, f"Página {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in {"H1x", "H2x"}:
            level = 0 if flowable.style.name == "H1x" else 1
            text = flowable.getPlainText()
            if not hasattr(flowable, "_bookmark_name"):
                self._bookmark_id += 1
                flowable._bookmark_name = f"section-{self._bookmark_id}"
            key = flowable._bookmark_name
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def H1(text):
    return Paragraph(text, styles["H1x"])


def H2(text):
    return Paragraph(text, styles["H2x"])


def bullet(text):
    return Paragraph("• " + text, styles["Bulletx"])


def formula(text):
    t = Table([[Paragraph(text, styles["Formula"]) ]], colWidths=[16.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.7, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def callout(title, text, color=GOLD):
    t = Table([[P(f"<b>{title}</b><br/>{text}")]], colWidths=[16.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def data_table(rows, widths=None, font=7.5, repeat=1):
    cooked = []
    for r, row in enumerate(rows):
        style = "TableHead" if r == 0 else "Smallx"
        cooked.append([P(escape(str(v)) if v is not None else "", style) for v in row])
    t = Table(cooked, colWidths=widths, repeatRows=repeat, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "DV-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "DV"),
        ("FONTSIZE", (0, 0), (-1, -1), font),
        ("LEADING", (0, 0), (-1, -1), font + 2),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def figure(path, caption, max_w=16.8 * cm, max_h=10.2 * cm):
    path = Path(path)
    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / w, max_h / h)
    return KeepTogether([
        Image(str(path), width=w * scale, height=h * scale),
        P(caption, "Caption"),
    ])


def new_chapter(story, title):
    story.extend([PageBreak(), H1(title)])


def matrix_rows():
    if args.matriz_operativa:
        ws = load_workbook(PROC / "output" / "procesos_estocasticos.xlsx", data_only=True)["Datos"]
        return [["Origen"] + [ws.cell(7,c).value for c in range(2,10)]] + [
            [ws.cell(i,1).value] + [f"{ws.cell(i,c).value:.6f}" for c in range(2,10)]
            for i in range(8,16)]
    wb = load_workbook(PROC / "0-enunciado" / "matriz-ratings.xlsx", data_only=True)
    ws = wb.active
    headers = [ws.cell(2, c).value for c in range(3, 11)]
    rows = [["Origen"] + headers]
    # Convención autorizada: conservar la fila Caa (fila 9) como Caa-C.
    for excel_row, label in [(3, "Aaa"), (4, "Aa"), (5, "A"), (6, "Baa"),
                             (7, "Ba"), (8, "B"), (9, "Caa-C"), (11, "Default")]:
        vals = [ws.cell(excel_row, c).value for c in range(3, 11)]
        rows.append([label] + [f"{v:.6f}" for v in vals])
    return rows


def build_story():
    f1 = PROC / "output" / "ejercicio-1"
    f2 = PROC / "output" / "ejercicio-2"
    f3 = PROC / "output" / "ejercicio-3"
    S = []

    S += [Spacer(1, 3.0 * cm), P("MEFC 2026", "CoverSub"),
          P("Fundamentos matemáticos", "CoverSub"),
          P("Procesos estocásticos", "CoverTitle"),
          Spacer(1, 0.4 * cm),
          callout("Memoria explicativa y auditada",
                  "Tres ejercicios resueltos con derivaciones teóricas, simulación reproducible, decisiones de modelización explícitas y controles independientes.", LIGHT_BLUE),
          Spacer(1, 1.0 * cm),
          P("Versión final · septiembre de 2026", "CoverSub"),
          Spacer(1, 3.0 * cm),
          P("Materiales asociados: tres notebooks, tres HTML offline, nueve figuras PNG, un Excel reproducible y un informe de auditoría.", "CoverSub"),
          PageBreak()]

    S += [H1("Índice"), P("La memoria sigue el orden del enunciado. Cada ejercicio separa datos, supuestos, derivación, cálculo, controles y límites.")]
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name="TOC0", fontName="DV-Bold", fontSize=10, leading=16, leftIndent=0, firstLineIndent=0, textColor=NAVY),
        ParagraphStyle(name="TOC1", fontName="DV", fontSize=8.5, leading=13, leftIndent=18, firstLineIndent=0, textColor=GRAY),
    ]
    S += [toc]

    new_chapter(S, "1. Resumen ejecutivo")
    S += [callout("Resultado global: APROBADO",
                  "Los tres ejercicios quedan resueltos, reproducibles y coherentes con el enunciado. La única ambigüedad de datos -la matriz 9×8- se trata exactamente como indicó la profesora.", GREEN),
          Spacer(1, 8),
          bullet("Ejercicio 1: matriz de transición 8×8, probabilidades de primer default, cohorte y distribución a 25 años, con validación Monte Carlo."),
          bullet("Ejercicio 2: cociente de difusiones, integral de Itô y martingala cuadrática; la parte empírica se entrega además en Excel."),
          bullet("Ejercicio 3: calibración de una volatilidad cuadrática determinista y valoración precisa de una call asiática aritmética."),
          H2("Cifras que debe retener el lector"),
          data_table([
              ["Bloque", "Resultado principal", "Control"],
              ["E1 - cohorte", "PD exacta 1Y = 2,2614%; PD acumulada 25Y = 54,1342%", "P25: máx. |z| = 2,41"],
              ["E2 - M1", "E[M1]=0; Var(M1)=2/9", "Excel: media 0,008262; var. 0,224584"],
              ["E3 - asiática", "Precio = 13,621805", "IC95% [13,621644; 13,621966]"],
          ], widths=[3.1*cm, 8.2*cm, 5.5*cm])]

    new_chapter(S, "2. Fuentes, entregables y trazabilidad")
    S += [P("El enunciado pide una memoria explicativa y todas las hojas de cálculo creadas. La resolución amplía ese mínimo con notebooks ejecutables y HTML autocontenidos."),
          data_table([
              ["Fuente o artefacto", "Uso", "Trazabilidad"],
              ["MEFC_2026_examen_procesos.pdf", "Definición literal de los tres ejercicios", "SHA-256 ca6f567b...537f3f5"],
              ["matriz-ratings.xlsx", "Probabilidades de transición anual", "SHA-256 eba5c101...b608289e3"],
              ["Correo de Maite", "Resuelve la dimensión 9×8", "Decisión transcrita y aplicada"],
              ["Notebooks", "Teoría, código y simulaciones", "Semillas fijas y aserciones"],
              ["Excel 2.c", "Trayectoria y 5.000 réplicas", "Fórmulas y Z visibles"],
          ], widths=[5.0*cm, 6.0*cm, 5.8*cm]),
          H2("Clasificación de la evidencia"),
          bullet("Dato: números leídos del PDF o del Excel original."),
          bullet("Aclaración docente: regla autorizada para eliminar una fila inferior."),
          bullet("Derivado: probabilidades, coeficientes y precios obtenidos mediante fórmulas o código."),
          bullet("Supuesto: elección de la raíz no negativa de la volatilidad y convenciones de simulación."),
          bullet("Estimación: cantidades Monte Carlo acompañadas de error estándar o intervalo de confianza.")]

    new_chapter(S, "3. La anomalía de la matriz de ratings")
    S += [P("El PDF define ocho estados: Aaa, Aa, A, Baa, Ba, B, Caa-C y Default. El Excel, sin embargo, contiene ocho columnas pero nueve filas de origen: separa Caa y Ca-C. Por tanto, la matriz no es cuadrada y no se puede elevar directamente a potencias."),
          formula("Excel original: 9 filas de origen × 8 columnas de destino"),
          P("No es correcto añadir de forma automática una novena columna Caa o separar Caa-C sin información adicional. Las probabilidades de salida hacia Caa-C no dicen cómo repartir la masa entre Caa y Ca-C; tampoco conocemos el peso con que habría que combinar las dos filas de origen."),
          callout("Respuesta de la profesora",
                  "Son ocho estados. Las transiciones desde Caa-C quedaron desdobladas en dos filas y no hay información para agregarlas con pesos. Se puede quitar una fila, asignar la restante al estado Caa-C y dejarlo anotado.", GOLD),
          H2("Decisión aplicada"),
          bullet("Se elimina la fila Ca-C."),
          bullet("Se conserva la fila Caa y se renombra como Caa-C."),
          bullet("No se promedian filas ni se inventan ponderaciones."),
          bullet("Todos los resultados del ejercicio 1 son condicionales a esta convención autorizada.")]

    new_chapter(S, "4. Matriz operativa 8×8")
    S += [P("La tabla muestra la matriz anual finalmente utilizada. Cada fila suma uno salvo error numérico de redondeo y Default es absorbente."),
          data_table(matrix_rows(), widths=[1.6*cm]+[1.9*cm]*8, font=5.3),
          Spacer(1, 8),
          callout("Control estructural",
                  "Error máximo de suma por fila: 2,22×10⁻¹⁶. Todos los elementos están entre 0 y 1. La última fila es (0,...,0,1).", GREEN),
          P("Interpretación: el elemento pᵢⱼ es la probabilidad de pasar del estado i al estado j en un año. La hipótesis de Markov supone que, condicionado al estado actual, el siguiente estado no depende de la historia anterior.")]

    new_chapter(S, "5. Ejercicio 1.a - default acumulado y primer default")
    S += [P("Sea P la matriz de transición y D el estado Default. La probabilidad acumulada de estar en default en el año n, partiendo del rating i, es el elemento (i,D) de P elevada a n."),
          formula("Fᵢ(n) = (Pⁿ)ᵢ,D"),
          P('Por qué Pⁿ suma todos los caminos. Cada camino tiene como probabilidad el producto de sus transiciones: (P²)ᵢD = Σⱼ Pᵢⱼ PⱼD; (P³)ᵢD = Σⱼ Σₖ Pᵢⱼ Pⱼₖ PₖD. Las sumas recorren todos los estados intermedios, incluido D: P³ = P²P añade un paso a cada camino de dos años. En general, (Pⁿ)ᵢⱼ suma todos los caminos de i a j en n transiciones. Ejemplo ilustrativo, distinto del dato del ejercicio: con orden A, B, D y filas de P (0.7, 0.2, 0.1), (0.1, 0.6, 0.3), (0, 0, 1), (P²)AD = 0.7×0.1 + 0.2×0.3 + 0.1×1 = 0.23. Son A→A→D, A→B→D y A→D→D. Como PDD = 1, el último camino conserva el default previo: (Pⁿ)ᵢD = Pr(τᵢ ≤ n), donde τᵢ es el año del primer default.', "Smallx"),
          P("La probabilidad de hacer default por primera vez exactamente en el año n es el incremento de la probabilidad acumulada, porque Default es absorbente."),
          formula("fᵢ(n) = Fᵢ(n) - Fᵢ(n-1),   con Fᵢ(0)=0"),
          H2("Lectura económica"),
          bullet("Ratings altos: el riesgo tarda en acumularse; el máximo observado puede quedar al final de la ventana de 25 años, sin implicar que sea el máximo global."),
          bullet("Ratings intermedios: aparece una joroba, porque primero aumenta la población expuesta en estados peores y después se agota por default."),
          bullet("Ratings bajos: domina el default inmediato y la probabilidad de primer default decrece con rapidez."),
          figure(f1 / "grafico_1a_primer_default_ratings.png", "Figura 1. Probabilidad incondicional de primer default por año y rating inicial.", max_h=10.8*cm)]

    new_chapter(S, "6. Ejercicio 1.b - cohorte de 5.002 compañías")
    S += [P("¿Cuántas empresas esperamos que hagan default? En 1.a estudiamos una empresa condicionada a su rating inicial; ahora ponderamos por los tamaños reales de los grupos."),
          P("El enunciado da N₀ = (136, 694, 1298, 1175, 578, 817, 304, 0), en orden Aaa, Aa, A, Baa, Ba, B, Caa-C, Default. Son 136 empresas Aaa, 694 Aa, etc., y suman 5.002."),
          formula("Nₙ = N₀Pⁿ;    [Nₙ]D = defaults esperados acumulados hasta n"),
          P("Nₙ contiene el número esperado en cada estado. Default es absorbente, por lo que incluye también a quienes llegaron antes. En el primer año cada grupo aporta su tamaño por su PD anual:"),
          formula("[N₀P]D = Σᵢ N₀,ᵢ Pᵢ,D = 113,12 compañías esperadas"),
          P("113,12 es una esperanza, no un conteo observado: cualquier realización tiene un número entero de defaults. Para aislar los que ocurren durante n, aplicamos la diferencia de acumulados de 1.a:"),
          formula("dₙ = [N₀Pⁿ]D − [N₀Pⁿ⁻¹]D = Σᵢ N₀,ᵢ [Fᵢ(n) − Fᵢ(n−1)]"),
          P("La proporción esperada de default exacto es dₙ/5002. El notebook calcula proporciones con p₀ = N₀/5002 y las multiplica por 5.002 para recuperar conteos esperados. Sumar esperanzas no exige independencia entre compañías."),
          data_table([
              ["Métrica", "Valor", "Interpretación"],
              ["Default exacto 1Y", "2,2614%", "113,12 compañías esperadas"],
              ["PD acumulada 25Y", "54,1342%", "2.707,79 compañías esperadas"],
              ["Año modal de la cohorte", "2", "Máximo de la distribución anual agregada"],
          ], widths=[5.0*cm, 4.0*cm, 7.8*cm]),
          figure(f1 / "grafico_1b_cohorte_default.png", "Figura 2. Default esperado por año para la cohorte inicial.", max_h=10.6*cm)]

    new_chapter(S, "7. Ejercicio 1.c - distribución a 25 años")
    S += [P("Elegimos una empresa uniformemente entre las 5.002. Antes de observar su rating, X₀ es aleatorio; Xₙ indica su estado al terminar el año n. Su distribución inicial es p₀ = N₀/5002 (también llamada π₀): Pr(X₀ = A) = 1298/5002."),
          formula("Pr(X₂₅ = j) = [p₀P²⁵]ⱼ = Σᵢ p₀,ᵢ (P²⁵)ᵢⱼ"),
          P("Esta es la distribución no condicionada al rating inicial. El enunciado también pide los distintos niveles de partida: si conocemos X₀ = i, usamos su fila de P²⁵."),
          formula("Pr(X₂₅ = j | X₀ = i) = (P²⁵)ᵢⱼ"),
          P("P²⁵ reúne distribuciones condicionadas; p₀P²⁵ es una única distribución ponderada por la cohorte. Ambas tablas completas se conservan en el notebook y la memoria unificada. La PD no condicionada a 25 años es 54,1342 %, coherente con 1.b."),
          P("Ejemplo ilustrativo: 80 % de empresas A y 20 % B, con PD del 10 % y 50 %, dan una PD aleatoria del 18 %: 0,8×0,10 + 0,2×0,50. Si sabemos que empieza en A, la PD es 10 %."),
          H2("Cómo se simula"),
          P("1. Sin condicionar, sortear X₀ con p₀; condicionando, fijar X₀ = i. 2. Sortear X₁ con la fila de X₀, X₂ con la fila de X₁ y continuar hasta X₂₅; Default permanece absorbente. 3. Repetir: las frecuencias aproximan p₀P²⁵ o la fila i de P²⁵, respectivamente."),
          P("El notebook simula 300.000 trayectorias por rating y luego pondera sus frecuencias con p₀. La mezcla estima la distribución no condicionada, pero no es una segunda simulación con X₀ sorteado."),
          P("En las 56 celdas de los siete ratings iniciales, el error absoluto máximo es 0,001486 y el máximo |z| es 2,41, bajo el umbral de 4 errores estándar. Para una frecuencia condicionada, SE = √[p(1−p)/300.000]: compara el error Monte Carlo con su escala; no exige igualdad exacta."),
          figure(f1 / "grafico_1c_distribucion_25y_validacion.png", "Figura 3. P²⁵ analítica y error estandarizado de la simulación.", max_h=8.0*cm)]

    new_chapter(S, "8. Ejercicio 2.a - cociente de dos difusiones")
    S += [P("Se busca el valor de μ que hace martingala a Yₜ=Xₜ/Nₜ. Como ambos procesos dependen de brownianos correlacionados, la covariación no puede omitirse."),
          formula("dXₜ = μXₜdt + σXₜdWₜ⁽¹⁾,   dNₜ = ½Nₜdt + NₜdWₜ⁽²⁾"),
          P("Aplicando Itô a f(x,n)=x/n, con d⟨W⁽¹⁾,W⁽²⁾⟩ₜ=ρdt, se obtiene:"),
          formula("dYₜ = Yₜ[(μ + ½ - σρ)dt + σdWₜ⁽¹⁾ - dWₜ⁽²⁾]"),
          P("El término de drift debe anularse. Por tanto:"),
          formula("μ = σρ - ½"),
          H2("Martingala verdadera"),
          P("Con esa elección, Y es una exponencial estocástica con volatilidad constante efectiva √(σ²+1-2σρ). En horizonte finito satisface las condiciones habituales de integrabilidad; no se queda solo en martingala local."),
          figure(f2 / "grafico_2a_cociente_martingala.png", "Figura 4. Comprobación empírica de que E[Yₜ] permanece constante.", max_h=10.0*cm)]

    new_chapter(S, "9. Ejercicio 2.b - integral de Itô")
    S += [P("La integral es Iₜ=∫₀ᵗ(Wₛ²-s)dWₛ. La pista sugiere aplicar Itô a Wₜ³."),
          formula("d(Wₜ³) = 3Wₜ²dWₜ + 3Wₜdt"),
          P("Reordenando e integrando:"),
          formula("∫₀ᵗ Wₛ²dWₛ = Wₜ³/3 - ∫₀ᵗ Wₛds"),
          P("Además, por integración estocástica por partes, ∫₀ᵗ s dWₛ = tWₜ - ∫₀ᵗWₛds. Al restar ambas expresiones, los términos ordinarios se cancelan."),
          formula("Iₜ = Wₜ³/3 - tWₜ"),
          P("La isometría de Itô proporciona Var(Iₜ)=E∫₀ᵗ(Wₛ²-s)²ds=2t³/3."),
          figure(f2 / "grafico_2b_integral_ito.png", "Figura 5. Convergencia de sumas discretas hacia la expresión cerrada.", max_h=10.0*cm)]

    new_chapter(S, "10. Ejercicio 2.c - martingala cuadrática")
    S += [P("Definimos Aₜ=∫₀ᵗs dWₛ. Es gaussiana centrada y su variación cuadrática determinista es q(t)=∫₀ᵗs²ds=t³/3."),
          formula("Mₜ = Aₜ² - q(t) = (∫₀ᵗs dWₛ)² - t³/3"),
          H2("Primera demostración: fórmula de Itô"),
          P("Como dAₜ=t dWₜ y d⟨A⟩ₜ=t²dt, la fórmula de Itô da d(Aₜ²)=2Aₜt dWₜ+t²dt. Restar dq(t)=t²dt elimina el drift."),
          formula("dMₜ = 2tAₜ dWₜ"),
          H2("Segunda demostración: esperanza condicional"),
          P("Para s&lt;t, Aₜ=Aₛ+(Aₜ-Aₛ), y el incremento es independiente de la información hasta s, con varianza q(t)-q(s). Al expandir el cuadrado, E[Mₜ|Fₛ]=Mₛ."),
          H2("Distribución"),
          formula("Mₜ = [t³/3]·(χ₁²-1),   E[Mₜ]=0,   Var(Mₜ)=2t⁶/9"),
          P("El soporte es Mₜ≥-t³/3. La densidad tiene una singularidad integrable en el borde inferior; no es normal ni simétrica."),
          figure(f2 / "grafico_2c_distribucion_M1.png", "Figura 6. Ley teórica y simulación de M₁.", max_h=8.3*cm)]

    new_chapter(S, "11. Simulación del ejercicio 2.c y diseño del Excel")
    S += [P("Para simular Aₜ sin error de discretización se usa su reloj cuadrático q(t)=t³/3. En una malla 0=t₀&lt;...&lt;tₙ, los incrementos son independientes y normales."),
          formula("ΔAⱼ = √[q(tⱼ)-q(tⱼ₋₁)]·Zⱼ,   Zⱼ ~ N(0,1)"),
          P("Esto no es Euler: es la distribución exacta de cada incremento de la integral gaussiana. El Excel conserva cada Zⱼ como dato fijo y calcula el resto mediante fórmulas."),
          data_table([
              ["Hoja", "Contenido", "Qué permite auditar"],
              ["Resumen", "Parámetros, teoría, estimaciones e IC", "Coherencia estadística y soporte"],
              ["Trayectoria", "101 fechas, Δq, Z, ΔA, A y M", "Cada paso de una trayectoria"],
              ["Replica_t1", "5.000 Z, A1 y M1", "Distribución terminal e histograma"],
          ], widths=[3.3*cm, 6.7*cm, 6.8*cm]),
          H2("Resultados del libro"),
          data_table([
              ["Control", "Teoría", "Excel"],
              ["E[M1]", "0", "0,008261710"],
              ["Var(M1)", "0,222222222", "0,224583814"],
              ["Error estándar media", "-", "0,006701997"],
              ["IC95% media", "contiene 0", "[-0,004874204; 0,021397624]"],
              ["Mínimo", "≥ -0,333333333", "-0,333333301"],
          ], widths=[5.6*cm, 4.6*cm, 6.6*cm]),
          figure(f2 / "grafico_2c_trayectorias_martingala.png", "Figura 7. Trayectorias simuladas de Mₜ.", max_h=8.0*cm)]

    new_chapter(S, "12. Ejercicio 3.1 y 3.2 - modelo y fórmula europea")
    S += [P("El activo satisface dSₜ=rSₜdt+σ(t)SₜdWₜ, con σ determinista. Aplicar Itô a log Sₜ integra exactamente la ecuación."),
          formula("Sₜ = S₀ exp{rt - ½V(t) + ∫₀ᵗσ(s)dWₛ},   V(t)=∫₀ᵗσ²(s)ds"),
          P("La integral es normal con media cero y varianza V(T). Por tanto, la fórmula de una call europea es Black-Scholes reemplazando σ√T por √V(T)."),
          formula("C(T,K)=S₀Φ(d₁)-Ke⁻ʳᵀΦ(d₂)"),
          formula("d₁=[ln(S₀/K)+rT+½V(T)]/√V(T),   d₂=d₁-√V(T)"),
          P("Datos del PDF: S₀=100, K=100, r=1%, precios 9,55 a 1Y, 12,48 a 1,25Y y 23,36 a 2Y. Los precios están redondeados a dos decimales, de modo que no debe atribuirse precisión económica a los últimos dígitos calibrados.")]

    new_chapter(S, "13. Ejercicio 3.3 - calibración de σ(t)")
    S += [P("Se impone σ(t)=at²+bt+c. Su varianza acumulada es un polinomio de grado cinco:"),
          formula("V(t)=a²t⁵/5 + abt⁴/2 + (b²+2ac)t³/3 + bct² + c²t"),
          P("Primero se invierte cada precio de call para obtener V(T). Después se resuelve el sistema no lineal V(Tⱼ)=Vⱼ con múltiples puntos iniciales. Aparecen cuatro raíces reales."),
          data_table([
              ["Vencimiento", "Precio", "V(T) implícita", "Vol. efectiva √(V/T)"],
              ["1,00", "9,55", "0,0521320003", "22,8324%"],
              ["1,25", "12,48", "0,0899877821", "26,8310%"],
              ["2,00", "23,36", "0,3292216020", "40,5723%"],
          ], widths=[3.5*cm, 3.2*cm, 4.8*cm, 5.3*cm]),
          callout("Criterio de selección",
                  "Se exige σ(t)≥0 para todo t∈[0,2]. Solo una raíz cumple la condición: a=0,049958716872, b=0,200094751620, c=0,099881280434.", GREEN),
          figure(f3 / "grafico_3c_calibracion_volatilidad.png", "Figura 8. Curvas algebraicas calibradas y selección de la raíz no negativa.", max_h=9.5*cm),
          P("El error máximo de repricing de las tres calls es 2,13×10⁻¹⁴: el sistema numérico queda resuelto a precisión de máquina.")]

    new_chapter(S, "14. Ejercicio 3.4 - valoración de la call asiática")
    S += [P("El payoff en T=2 es el positivo de la media aritmética de cuatro fijaciones menos K. Las fechas son 1,15; 1,30; 1,60 y 1,70 años."),
          formula("Payoff = max{(S₁.₁₅+S₁.₃₀+S₁.₆₀+S₁.₇₀)/4 - 100, 0}"),
          P("Como σ es determinista, el vector de integrales gaussianas tiene covarianza Cov(Xᵢ,Xⱼ)=V(min(tᵢ,tⱼ)). Una factorización de Cholesky produce las cuatro fijaciones sin discretizar la SDE."),
          formula("Precio = e⁻ʳᵀ · E[Payoff]"),
          H2("Reducción de varianza"),
          bullet("RQMC Sobol con 32 aleatorizaciones independientes y 131.072 caminos por réplica."),
          bullet("Variables antitéticas para cancelar parte de la variabilidad impar."),
          bullet("Call asiática geométrica como variable de control, con precio analítico 12,79677073."),
          data_table([
              ["Estimador", "Precio", "Error / intervalo"],
              ["RQMC + antitéticos + control", "13,62180500", "IC95% [13,62164409; 13,62196591]"],
              ["PRNG independiente", "13,62209062", "SE 0,00105350; z=+0,27"],
          ], widths=[6.2*cm, 4.0*cm, 6.6*cm]),
          figure(f3 / "grafico_3d_valoracion_asiatica.png", "Figura 9. Convergencia y contraste de la valoración asiática.", max_h=9.2*cm)]

    new_chapter(S, "15. Sensibilidad a la raíz algebraica")
    S += [P("Los precios europeos solo identifican la varianza acumulada en tres vencimientos. Distintas curvas σ pueden reproducirlos porque el precio europeo depende de σ², no del signo puntual de σ."),
          P("Una raíz que cruza cero también repricia las tres calls, pero no cumple la interpretación de volatilidad no negativa. Si se utilizara, la asiática valdría 13,740158."),
          data_table([
              ["Curva", "Call asiática", "Diferencia"],
              ["No negativa elegida", "13,621805", "Referencia"],
              ["Con cruce por cero, rechazada", "13,740158", "+0,118353 (+0,869%)"],
          ], widths=[7.3*cm, 4.3*cm, 5.2*cm]),
          callout("Conclusión de modelización",
                  "La restricción de no negatividad no es cosmética: afecta al precio de un derivado dependiente de la trayectoria. El resultado exótico es condicional a esa elección.", GOLD)]

    new_chapter(S, "16. Auditoría independiente")
    S += [P("La revisión se realizó desde las fuentes, reejecutando las 28 celdas de código en orden y contrastando resultados mediante implementaciones separadas."),
          data_table([
              ["Control", "Prueba", "Resultado"],
              ["E1 estructura", "sumas, rango y absorción", "PASS"],
              ["E1 P25", "analítico vs. Monte Carlo", "máx. |z| 2,41"],
              ["E2 identidades", "Itô, momentos y soporte", "PASS"],
              ["E2 condicional", "regresión M1 sobre M0.5", "α=-0,00056; β=1,00149"],
              ["E3 repricing", "tres calls europeas", "error 2,13×10⁻¹⁴"],
              ["E3 contraste", "PRNG vs. RQMC", "z=+0,27"],
              ["HTML", "autosuficiencia y móvil", "0 errores; 0 avisos"],
              ["Excel", "fórmulas y errores", "0 errores de fórmula"],
          ], widths=[3.5*cm, 7.5*cm, 5.8*cm]),
          H2("Correcciones surgidas de la auditoría"),
          bullet("Se precisó que el máximo al año 25 es solo el máximo observado dentro de la ventana."),
          bullet("El mapa de validación de P²⁵ muestra error estandarizado, no error absoluto mal rotulado."),
          bullet("Se repuso el signo + omitido antes del término σdW⁽¹⁾ en la presentación de Itô."),
          bullet("La sensibilidad del ejercicio 3 presenta límites de intervalo, no un ± ambiguo."),
          bullet("El histograma del Excel se amplió para incluir las 5.000 observaciones, incluida la cola hasta 3,63.")]

    new_chapter(S, "17. Limitaciones y alcance")
    S += [bullet("Caa-C: la fila conservada es una convención docente. Elegir Ca-C cambiaría los resultados; no existe información para una agregación ponderada."),
          bullet("Calls redondeadas: los coeficientes a, b y c ajustan exactamente cotizaciones con dos decimales; su precisión numérica no equivale a precisión de mercado."),
          bullet("Riesgo de modelo: el estrecho intervalo Monte Carlo mide error de simulación, no incertidumbre por especificación de σ(t)."),
          bullet("Horizonte de gráficos: que una curva alcance su mayor valor en el año 25 no demuestra que allí esté su máximo global."),
          bullet("Excel: los números normales son fijos para trazabilidad. Cambiar la semilla requiere regenerar los Z; no basta con recalcular fórmulas."),
          callout("Materialidad",
                  "No quedan hallazgos que bloqueen la entrega. El único riesgo residual material es la convención explícita del bucket Caa-C, autorizada por la profesora.", GREEN)]

    new_chapter(S, "18. Reproducción y mapa de archivos")
    S += [P("Desde la raíz del repositorio se crea un entorno, se instalan las dependencias y se ejecutan los notebooks. Los adjuntos originales se colocan en la carpeta 0-enunciado de la Entrega 2; no se publican por ser fuentes suministradas al grupo."),
          formula("python -m venv .venv   →   pip install -r requirements.txt"),
          formula("jupyter nbconvert --to notebook --execute --inplace &lt;notebook.ipynb&gt;"),
          data_table([
              ["Ruta dentro de la Entrega 2", "Contenido"],
              ["1-cadenas-markov-ratings/", "Notebook del ejercicio 1"],
              ["2-ito-martingalas/", "Notebook del ejercicio 2"],
              ["3-volatilidad-determinista-asiatica/", "Notebook del ejercicio 3"],
              ["AUDITORIA.md", "Evidencia y veredicto independiente"],
              ["output/", "Memorias, reportes, Excel y figuras de los tres ejercicios"],
              ["../tools/nb_to_html.py", "Herramienta compartida de conversión HTML offline"],
          ], widths=[8.2*cm, 8.6*cm]),
          H2("Qué revisar antes de entregar"),
          bullet("Abrir los tres HTML sin red y comprobar fórmulas y gráficos."),
          bullet("Abrir el Excel y revisar Resumen, Trayectoria y Replica_t1."),
          bullet("Confirmar que el PDF conserva índice, numeración y nueve figuras."),
          bullet("Entregar una única versión del grupo para evitar divergencias.")]

    new_chapter(S, "19. Conclusión")
    S += [callout("Síntesis",
                  "La resolución mantiene una cadena verificable: fuente → supuesto explícito → derivación → cálculo reproducible → contraste independiente → interpretación.", LIGHT_BLUE),
          Spacer(1, 10),
          P("El ejercicio 1 enseña a distinguir una matriz de transición válida de una tabla dimensionalmente incoherente y a no inventar pesos. El ejercicio 2 conecta cálculo de Itô, variación cuadrática, distribución y simulación exacta. El ejercicio 3 muestra que calibrar instrumentos europeos no elimina la ambigüedad de la trayectoria y que una restricción económica puede ser material para un exótico."),
          P("Con la convención Caa-C documentada, los tres bloques cumplen el enunciado. Los resultados analíticos y numéricos concuerdan dentro de tolerancias justificadas, los artefactos son reproducibles y la auditoría no detecta errores materiales."),
          Spacer(1, 14),
          data_table([
              ["Criterio final", "Estado"],
              ["Cobertura del enunciado", "COMPLETA"],
              ["Coherencia matemática", "PASS"],
              ["Reproducibilidad", "PASS"],
              ["Presentación HTML/PDF/Excel", "PASS"],
              ["Hallazgos bloqueantes", "NINGUNO"],
          ], widths=[10.5*cm, 6.3*cm])]
    return S


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = MemoryDoc(str(OUT))
    doc.multiBuild(build_story())
    print(OUT)


if __name__ == "__main__":
    main()
