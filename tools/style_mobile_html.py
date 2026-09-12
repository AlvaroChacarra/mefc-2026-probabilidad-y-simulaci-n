#!/usr/bin/env python3
"""Aplica tipografía BBVA y matemáticas SVG accesibles a HTML ya generado.

python tools/style_mobile_html.py archivo.html [otro.html ...]
Preparación del renderizador: npm ci --prefix tools
No cambia texto, resultados ni los MathML originales, que conserva accesibles.
"""
from pathlib import Path
from copy import deepcopy
import argparse
import base64
import json
import re
import subprocess
from bs4 import BeautifulSoup, Tag

TOOLS = Path(__file__).resolve().parent
CACHE = {}


def render_math(items):
    missing = list(dict.fromkeys((m, d) for m, d in items if (m, d) not in CACHE))
    if missing:
        proc = subprocess.run(['node', str(TOOLS / 'render_math_svg.cjs')],
            input=json.dumps([{'mathml':m, 'display':d} for m,d in missing]),
            text=True, capture_output=True, check=True)
        for key, result in zip(missing, json.loads(proc.stdout), strict=True):
            CACHE[key] = result
    return [CACHE[item] for item in items]


def svg_tag(result, soup):
    svg = BeautifulSoup(result['svg'], 'html.parser').svg
    svg['aria-hidden'] = 'true'
    svg['focusable'] = 'false'
    svg.attrs.pop('role', None)
    # Stable em sizing does not depend on the reader's serif font x-height.
    for axis in ('width', 'height'):
        svg[axis] = f"{float(svg[axis].removesuffix('ex')) * .5:.4f}em"
    svg['style'] = re.sub(r'(-?[\d.]+)ex', lambda m: f'{float(m[1])*.5:.4f}em', svg.get('style',''))
    return svg


def split_units(math):
    """Saltos entre términos al nivel exterior, nunca dentro de un paréntesis/fracción."""
    node = deepcopy(math)
    while node.name in ('math', 'mrow') and len(list(node.children)) == 1:
        child = next(node.children)
        if not isinstance(child, Tag): break
        node = child
    # En un resultado largo, el fondo azul agrupa las líneas en lugar del recuadro.
    if node.name == 'menclose':
        node = node.find('mrow', recursive=False) or node
    children = list(node.children) if node.name in ('math','mrow') else [node]
    if children and isinstance(children[0],Tag) and children[0].name == 'menclose':
        enclosed = children[0].find('mrow',recursive=False) or children[0]
        children = list(enclosed.children) + children[1:]
    groups, current, depth = [], [], 0
    for child in children:
        token = child.get_text() if isinstance(child,Tag) else str(child)
        separator = isinstance(child,Tag) and child.name == 'mo' and token in ('=', '+', '−', ',')
        gap = isinstance(child,Tag) and child.name == 'mspace' and child.get('width') in ('1em','2em')
        if depth == 0 and (separator or gap) and current:
            groups.append(''.join(str(x) for x in current)); current=[]
        current.append(child)
        # Un cierre como )^+ está dentro de msup; sigue cerrando el paréntesis exterior.
        boundary=child
        while isinstance(boundary,Tag) and boundary.name in ('msup','msub','msubsup'):
            boundary=next((x for x in boundary.children if isinstance(x,Tag)),None)
        if isinstance(boundary,Tag) and boundary.name=='mo':
            edge=boundary.get_text()
            if edge in ('(', '[', '{', '⟨'): depth += 1
            elif edge in (')', ']', '}', '⟩'): depth = max(0, depth-1)
    if current: groups.append(''.join(str(x) for x in current))
    return groups


def math_fragment(content):
    return '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow>'+content+'</mrow></math>'


def lines_for(math, full):
    if full['widthEx'] <= 37: return [full]
    units = split_units(math)
    if len(units) < 2: return [full]
    keys = {(i,j):(math_fragment(''.join(units[i:j])),True)
            for i in range(len(units)) for j in range(i+1,len(units)+1)}
    render_math(list(keys.values()))
    lines, start = [], 0
    while start < len(units):
        end = start+1
        while end < len(units) and CACHE[keys[start,end+1]]['widthEx'] <= 37:
            end += 1
        lines.append(CACHE[keys[start,end]])
        start=end
    # Evitar presentar solo el miembro izquierdo en una línea, sin ganar anchura.
    if len(lines)>1 and max(x['widthEx'] for x in lines) < full['widthEx']*.9:
        return lines
    return [full]


def apply_style(path):
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    # Idempotencia: restaurar exactamente el MathML original antes de regenerar.
    for wrapper in list(soup.select('.math-render')):
        original=wrapper.find('math')
        if original:
            original=original.extract()
            original.attrs.pop('class',None)
            wrapper.replace_with(original)
    for elem in soup.select('#bbva-reading-style,.formula-hint,.reading-route'):
        elem.decompose()
    math_nodes=soup.find_all('math')
    original_math=[str(m) for m in math_nodes]
    requests=[(str(m),m.get('display')=='block') for m in math_nodes]
    rendered=render_math(requests)
    wraps=0; scrolls=0
    for math,result in zip(math_nodes,rendered,strict=True):
        display=math.get('display')=='block'
        wrapper=soup.new_tag('span',attrs={'class':'math-render'+(' block' if display else '')})
        math.wrap(wrapper)
        # MathML remains available to assistive technology; SVG is the visual layer.
        math['class']='math-source'
        pieces=lines_for(math,result) if display else [result]
        if len(pieces)>1: wraps+=1
        for piece in pieces:
            svg=svg_tag(piece,soup)
            if display:
                line=soup.new_tag('span',attrs={'class':'math-line'})
                line.append(svg);wrapper.insert(len(wrapper.contents)-1,line)
            else: wrapper.insert(0,svg)
        if display:
            parent=wrapper.find_parent(class_=lambda v:v and ('formula' in v.split() or 'math-scroll' in v.split()))
            if parent is None:
                parent=soup.new_tag('div',attrs={'class':'formula','tabindex':'0'});wrapper.wrap(parent)
            if math.find('menclose'):
                parent['class']=list(dict.fromkeys(parent.get('class',[])+['math-result']))
            if max(p['widthEx'] for p in pieces)>37:
                hint=soup.new_tag('p',attrs={'class':'formula-hint'});hint.string='Fórmula completa · desliza →';parent.insert_before(hint);scrolls+=1
    # Fuentes reales incluidas en el HTML, sin peticiones al servidor de BBVA.
    fonts=[]
    for label,weight in [('Book',400),('Medium',500),('Bold',700)]:
        data=base64.b64encode((TOOLS/'assets'/f'BentonSansBBVA-{label}.woff2').read_bytes()).decode()
        fonts.append("@font-face{font-family:'Benton Sans BBVA';font-style:normal;font-weight:"+str(weight)+";font-display:swap;src:url(data:font/woff2;base64,"+data+") format('woff2')}")
    style=soup.new_tag('style',id='bbva-reading-style')
    style.string='\n'.join(fonts)+'\n'+(TOOLS/'html_reading.css').read_text()
    soup.head.append(style)
    if soup.select('.jp-Cell'):
        soup.body['class']=list(dict.fromkeys(soup.body.get('class',[])+['notebook-report']))
        for code in soup.select('.jp-CodeCell > .jp-Cell-inputWrapper'):
            if code.find_parent('details'):continue
            details=soup.new_tag('details',attrs={'class':'code-details'})
            summary=soup.new_tag('summary');summary.string='Ver código de la comprobación'
            code.wrap(details);details.insert(0,summary)
    else:
        main=soup.find('main')
        nav=soup.select_one('nav')
        if main and nav:
            route=soup.new_tag('nav',attrs={'class':'reading-route','aria-label':'Ejercicios'})
            for href,label in [('#seccion-1','01 · Ratings'),('#seccion-5','02 · Itô'),('#seccion-9','03 · Opciones')]:
                a=soup.new_tag('a',href=href);a.string=label;route.append(a)
            nav.insert_before(route)
        for table in soup.select('table.wide'):
            if table.find_parent('details'):continue
            container=table.find_parent(class_='table-scroll')
            if container:
                details=soup.new_tag('details');summary=soup.new_tag('summary')
                summary.string='Ver tabla completa · todos los ratings'
                container.wrap(details);details.insert(0,summary)
    # Verificar que la capa visual conserva todos los árboles semánticos originales.
    after=[]
    for m in soup.find_all('math'):
        clone=deepcopy(m);clone.attrs.pop('class',None);after.append(str(clone))
    assert original_math==after, 'El render no debe alterar ninguna fórmula'
    path.write_text(str(soup),encoding='utf-8')
    return {'file':str(path),'formulas':len(math_nodes),'formulas_en_varias_lineas':wraps,'formulas_con_scroll_local':scrolls,'bytes':path.stat().st_size}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('files',nargs='+',type=Path)
    args=parser.parse_args()
    for path in args.files:print(json.dumps(apply_style(path),ensure_ascii=False))
