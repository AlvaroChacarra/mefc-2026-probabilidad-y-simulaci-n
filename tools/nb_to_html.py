#!/usr/bin/env python3
"""
Genera el reporte HTML de un notebook con las fórmulas matemáticas renderizadas
de forma 100% offline (sin depender de ningún CDN de MathJax).

El HTML estándar de `jupyter nbconvert` deja las fórmulas LaTeX como texto y
confía en cargar MathJax desde un CDN en tiempo de visualización. Si el lector
abre el archivo sin internet (o el CDN está bloqueado/caído), las fórmulas no se
renderizan. Para un entregable autocontenido convertimos el LaTeX a MathML
nativo, que cualquier navegador moderno (Chrome/Edge/Firefox) pinta sin JS ni red.

Uso:
    python tools/nb_to_html.py <notebook.ipynb> <salida.html>
"""
import re
import sys
import subprocess
import tempfile
from pathlib import Path

import latex2mathml.converter as L2M
from bs4 import BeautifulSoup, NavigableString

# $$...$$ (display) o $...$ (inline). El display tiene prioridad en el alternado.
MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)


def tex_a_mathml(tex: str, display: bool) -> str:
    mml = L2M.convert(tex.strip())
    if display:
        mml = mml.replace('display="inline"', 'display="block"', 1)
    return mml


def trocea(texto: str, soup: BeautifulSoup):
    """Convierte un string con $...$/$$...$$ en una lista de nodos (texto + <math>)."""
    nodos, pos = [], 0
    for m in MATH_RE.finditer(texto):
        if m.start() > pos:
            nodos.append(NavigableString(texto[pos:m.start()]))
        display = m.group(1) is not None
        tex = m.group(1) if display else m.group(2)
        frag = BeautifulSoup(tex_a_mathml(tex, display), "html.parser")
        math = frag.find("math")
        math["role"] = "math"
        math["aria-label"] = tex.strip()
        nodos.append(math)
        pos = m.end()
    if pos < len(texto):
        nodos.append(NavigableString(texto[pos:]))
    return nodos


def renderiza_math(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport is None:
        viewport = soup.new_tag("meta", attrs={"name": "viewport"})
        (soup.head or soup).append(viewport)
    viewport["content"] = "width=device-width, initial-scale=1, viewport-fit=cover"

    # Eliminamos los scripts de MathJax/require desde CDN: ya no hacen falta
    # (el LaTeX se convierte a MathML) y así el HTML no hace peticiones externas.
    for sc in soup.find_all("script"):
        src = sc.get("src", "")
        cuerpo = sc.string or ""
        if any(k in src for k in ("mathjax", "require.js", "cdnjs")) or \
           "MathJax" in cuerpo or "displayMath" in cuerpo or \
           "mermaid" in cuerpo or "cdnjs" in cuerpo:
            sc.decompose()

    # Solo tocamos las celdas markdown renderizadas; el código queda intacto.
    for cont in soup.select(".jp-RenderedMarkdown"):
        for txt in list(cont.find_all(string=True)):
            if "$" not in txt:
                continue
            if txt.find_parent(["code", "pre"]) is not None:
                continue
            nodos = trocea(str(txt), soup)
            if len(nodos) == 1 and isinstance(nodos[0], NavigableString):
                continue
            txt.replace_with(*nodos)

    # Las tablas y ecuaciones anchas se desplazan localmente en pantallas
    # pequeñas, sin forzar un scroll horizontal de toda la página.
    for table in soup.find_all("table"):
        if table.parent and "table-scroll" in table.parent.get("class", []):
            continue
        hint = soup.new_tag("p", attrs={"class": "swipe-hint"})
        hint.string = "Desliza para ver más →"
        table.insert_before(hint)
        wrapper = soup.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0"})
        table.wrap(wrapper)
    for img in soup.find_all("img"):
        if not img.get("alt"):
            img["alt"] = "Gráfico o tabla generada por el notebook"
    for math in soup.find_all("math", attrs={"display": "block"}):
        if math.parent and "math-scroll" in math.parent.get("class", []):
            continue
        wrapper = soup.new_tag("div", attrs={"class": "math-scroll", "tabindex": "0"})
        math.wrap(wrapper)

    # Capa responsive y accesible, deliberadamente añadida al final para que
    # prevalezca sobre el CSS de nbconvert.
    style = soup.new_tag("style")
    style.string = (
        ":root{color-scheme:light;}"
        "html{box-sizing:border-box;-webkit-text-size-adjust:100%;}"
        "*,*:before,*:after{box-sizing:inherit;}"
        "body{max-width:1120px;margin:0 auto;line-height:1.55;overflow-wrap:anywhere;"
        "padding-top:max(1.25rem,env(safe-area-inset-top));"
        "padding-right:max(1rem,env(safe-area-inset-right));"
        "padding-bottom:max(1.5rem,env(safe-area-inset-bottom));"
        "padding-left:max(1rem,env(safe-area-inset-left));}"
        ".jp-Cell,.jp-Cell-inputWrapper,.jp-Cell-outputWrapper{min-width:0;}"
        "img,svg,canvas{max-width:100%;height:auto;}"
        "pre,.table-scroll,.math-scroll{max-width:100%;overflow-x:auto;"
        "-webkit-overflow-scrolling:touch;}"
        ".table-scroll,.math-scroll{margin:.8rem 0;}"
        ".swipe-hint{display:none;color:#64748b;font-size:.76rem;margin:.3rem 0;}"
        ".table-scroll table{margin:0;}"
        "math[display='block']{display:block;text-align:center;margin:.9em auto;"
        "font-size:1.15em;min-width:max-content;}"
        "math{font-size:1.05em;}"
        "@media(max-width:700px){body{font-size:16px;line-height:1.58;}"
        "h1{font-size:1.7rem;line-height:1.18;}h2{font-size:1.4rem;}"
        "h3{font-size:1.18rem;}pre,code{font-size:.82rem;}"
        ".table-scroll table{font-size:.82rem;min-width:max-content;}"
        ".swipe-hint{display:block;}"
        ".jp-RenderedHTMLCommon{overflow:visible;}"
        "math[display='block']{font-size:1.05em;}}"
    )
    (soup.head or soup).append(style)
    return str(soup)


def main():
    nb, salida = Path(sys.argv[1]), Path(sys.argv[2])
    with tempfile.TemporaryDirectory() as tmp:
        tmp_html = Path(tmp) / "raw.html"
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "html", "--embed-images",
             str(nb), "--output", tmp_html.stem, "--output-dir", str(tmp)],
            check=True,
        )
        html = renderiza_math(tmp_html.read_text(encoding="utf-8"))
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(html, encoding="utf-8")
    print(f"✓ Reporte offline escrito en {salida}")


if __name__ == "__main__":
    main()
