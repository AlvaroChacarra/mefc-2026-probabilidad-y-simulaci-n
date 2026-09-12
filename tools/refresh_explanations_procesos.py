#!/usr/bin/env python3
"""Sincroniza la explicación del HTML conjunto con los notebooks de ejercicios 2 y 3.

Uso: python tools/refresh_explanations_procesos.py
También lo invoca build_output_procesos.py después de generar su HTML base.
Los PDF mantienen su edición resumida; este paso actualiza exclusivamente HTML.
"""
from pathlib import Path
import re

import nbformat
from bs4 import BeautifulSoup
from nbconvert.filters.markdown import markdown2html
from nb_to_html import tex_a_mathml

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / 'entrega-2-procesos-estocasticos'
MATH = re.compile(r'\$\$(.+?)\$\$|\$(.+?)\$', re.S)


def markdown_offline(source):
    """Protege las fórmulas antes de Markdown para conservar índices y signos <."""
    equations = []

    def protect(match):
        display = match.group(1) is not None
        tex = match.group(1) if display else match.group(2)
        math = BeautifulSoup(tex_a_mathml(tex, display), 'html.parser').math
        math['aria-label'] = tex.strip()
        math['role'] = 'math'
        rendered = str(math)
        if display:
            rendered = '<div class="formula" tabindex="0">' + rendered + '</div>'
        equations.append(rendered)
        return f'EQUATIONPLACEHOLDER{len(equations)-1}END'

    rendered = markdown2html(MATH.sub(protect, source))
    for index, equation in enumerate(equations):
        token = f'EQUATIONPLACEHOLDER{index}END'
        if equation.startswith('<div'):
            rendered = rendered.replace('<p>' + token + '</p>', equation)
        rendered = rendered.replace(token, equation)
    soup = BeautifulSoup(rendered, 'html.parser')
    for anchor in soup.select('.anchor-link'):
        anchor.decompose()
    for table in soup.find_all('table'):
        wrapper = soup.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0'})
        table.wrap(wrapper)
    for link in soup.find_all('a', href=True):
        link['href'] = link['href'].replace('../output/', '')
    return str(soup)


def refresh(path=None):
    path = Path(path) if path else PROC / 'output/main.html'
    n2 = nbformat.read(next((PROC / '2-ito-martingalas').glob('*.ipynb')), as_version=4)
    n3 = nbformat.read(next((PROC / '3-volatilidad-determinista-asiatica').glob('*.ipynb')), as_version=4)
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    mapping = {
        'seccion-5': (n2, [3]), 'seccion-6': (n2, [5]),
        'seccion-7': (n2, [8, 9]), 'seccion-8': (n2, [11]),
        'seccion-9': (n3, [0, 3, 4]), 'seccion-10': (n3, [6]),
        'seccion-11': (n3, [9, 12]),
    }
    for section_id, (notebook, indices) in mapping.items():
        section = soup.find('section', id=section_id)
        if section is None:
            raise ValueError(f'Falta la sección {section_id}')
        header = section.header.extract()
        # Mantener el contraste numérico y figura de las 5.000 réplicas de Excel.
        extras = []
        if section_id == 'seccion-8':
            for node in section.select('.table-scroll, figure'):
                if node.find('table') and 'Magnitud' not in node.get_text():
                    continue
                extras.append(str(node))
        if section_id == 'seccion-10':
            extras = [str(node) for node in section.find_all('figure')]
        fragments = []
        for index in indices:
            content = notebook.cells[index].source
            if section_id == 'seccion-9' and index == 0:
                content = content[content.index('## Datos'):]
            content = re.sub(r'^---\s*', '', content)
            if section_id not in ('seccion-7', 'seccion-9'):
                content = re.sub(r'^## Apartado[^\n]*\n', '', content)
            else:
                content = re.sub(r'^### ', '#### ', content, flags=re.M)
            # La página conjunta ya tiene un h2; los pasos pasan a h3.
            content = re.sub(r'^## ', '### ', content, flags=re.M)
            content = content.replace('La celda siguiente', 'El notebook')
            content = content.replace('la siguiente celda', 'el notebook')
            content = content.replace('La tabla siguiente', 'La tabla de resultados')
            fragments.append(markdown_offline(content))
        # Tablas calculadas en los notebooks; conservar las cifras sin transcribirlas.
        numeric_cells = {'seccion-10': [8], 'seccion-11': [10]}.get(section_id, [])
        for index in numeric_cells:
            for output in notebook.cells[index].get('outputs', []):
                rendered = output.get('data', {}).get('text/html')
                if rendered:
                    fragment = BeautifulSoup(rendered, 'html.parser')
                    for table in fragment.find_all('table'):
                        extras.append('<div class="table-scroll" tabindex="0">' + str(table) + '</div>')
        section.clear()
        section.append(header)
        body = BeautifulSoup('\n'.join(fragments + extras), 'html.parser')
        for child in list(body.contents):
            section.append(child)
    path.write_text(str(soup), encoding='utf-8')
    print(f'Explicaciones sincronizadas: {path}')


if __name__ == '__main__':
    refresh()
