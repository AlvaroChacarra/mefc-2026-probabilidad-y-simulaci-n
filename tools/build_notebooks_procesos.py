#!/usr/bin/env python3
"""Construye los tres reportes y main.html desde los tres notebooks ejecutados.

No ejecuta ni transcribe cálculos: conserva cada celda Markdown y cada output.
El código queda plegado; las tablas y figuras permanecen visibles.
Uso: python tools/build_notebooks_procesos.py
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from bs4 import BeautifulSoup
import nbformat
from style_mobile_html import apply_style

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / 'entrega-2-procesos-estocasticos'
OUT = PROC / 'output'
NOTEBOOKS = [
    PROC / '1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb',
    PROC / '2-ito-martingalas/ejercicio2_ito_martingalas.ipynb',
    PROC / '3-volatilidad-determinista-asiatica/ejercicio3_volatilidad_determinista_asiatica.ipynb',
]


def image_hashes(node):
    return [hashlib.sha256(img['src'].encode()).hexdigest()
            for img in node.select('img')]


def fingerprint(node):
    """Contenido de una celda, sin los identificadores propios de presentación."""
    copy = deepcopy(node)
    for el in copy.select('style,script,svg,.anchor-link,.formula-hint'):
        el.decompose()
    for math in copy.select('math'):
        math.replace_with(math.get('aria-label', math.get_text()))
    text = re.sub(r'\s+', ' ', copy.get_text(' ', strip=True))
    return text, image_hashes(copy)


def validate(main_path=None):
    main_path = Path(main_path) if main_path else OUT / 'main.html'
    combined = BeautifulSoup(main_path.read_text(), 'html.parser')
    summary = []
    actual_paths = sorted(PROC.glob('[123]-*/*.ipynb'))
    assert actual_paths == NOTEBOOKS, 'Deben existir exactamente tres notebooks canónicos'
    all_ids = [el['id'] for el in combined.select('[id]')]
    assert len(all_ids) == len(set(all_ids)), 'Identificadores HTML duplicados'
    for n, path in enumerate(NOTEBOOKS, 1):
        nb = nbformat.read(path, as_version=4)
        report = BeautifulSoup((OUT / f'ejercicio-{n}/ejercicio{n}_reporte.html').read_text(), 'html.parser')
        a = report.select('.jp-Cell')
        b = combined.select(f'#ejercicio-{n} .jp-Cell')
        assert len(a) == len(b) == len(nb.cells), f'Faltan celdas en ejercicio {n}'
        for cell, single, joined in zip(nb.cells, a, b, strict=True):
            assert fingerprint(single) == fingerprint(joined), f'Contenido distinto: {n}/{cell.id}'
            if cell.cell_type == 'markdown':
                expected = [(x or y).strip() for x, y in re.findall(
                    r'\$\$(.+?)\$\$|\$(.+?)\$', cell.source, re.S)]
                actual = [m['aria-label'] for m in single.select('math')]
                assert expected == actual, f'Fórmulas distintas: {n}/{cell.id}'
            else:
                expected = sum('image/png' in o.get('data', {}) for o in cell.outputs)
                assert len(single.select('img')) == expected, f'Faltan figuras: {n}/{cell.id}'
                expected_tables = []
                for output in cell.outputs:
                    assert output.output_type != 'error', f'Notebook con error: {n}/{cell.id}'
                    if output.output_type == 'stream':
                        assert output.text.strip() in single.get_text(), f'Falta salida: {n}/{cell.id}'
                    table_html = output.get('data', {}).get('text/html', '')
                    if table_html:
                        expected_tables.extend(BeautifulSoup(table_html, 'html.parser').select('table'))
                actual_tables = single.select('table')
                assert [t.get_text(' ',strip=True) for t in expected_tables] == [t.get_text(' ',strip=True) for t in actual_tables], f'Tablas distintas: {n}/{cell.id}'
        summary.append({'ejercicio': n, 'celdas': len(a), 'figuras': len(report.select('img')),
                        'formulas': len(report.select('math'))})
    assert not combined.select('merror,[data-mml-node="merror"]')
    for link in combined.select('a[href^="#"]'):
        assert combined.find(id=link['href'][1:]), f'Enlace roto: {link["href"]}'
    print(json.dumps({'consistencia': 'PASS', 'notebooks': summary}, ensure_ascii=False))
    return summary


def build(main_path=None):
    main_path = Path(main_path) if main_path else OUT / 'main.html'
    reports = []
    for n, notebook in enumerate(NOTEBOOKS, 1):
        report_path = OUT / f'ejercicio-{n}/ejercicio{n}_reporte.html'
        subprocess.run([sys.executable, str(ROOT / 'tools/nb_to_html.py'),
                        str(notebook), str(report_path)], check=True)
        reports.append(BeautifulSoup(report_path.read_text(), 'html.parser'))
    soup = BeautifulSoup('<!doctype html><html lang="es"><head></head><body class="notebook-report unified-report"><main><header><h1>Procesos estocásticos</h1><p>Tres ejercicios · explicaciones, resultados y gráficas de los notebooks.</p></header><nav aria-label="Contenido"><details open><summary>Ir a un ejercicio</summary></details></nav></main></body></html>', 'html.parser')
    soup.head.replace_with(deepcopy(reports[0].head))
    soup.title.string = 'MEFC 2026 · Procesos estocásticos'
    menu = soup.nav.details
    for n, (path, report) in enumerate(zip(NOTEBOOKS, reports, strict=True), 1):
        label = ['Cadenas de Markov', 'Itô y martingalas', 'Volatilidad y opciones'][n-1]
        link = soup.new_tag('a', href=f'#ejercicio-{n}')
        link.string = f'{n}. {label}'
        menu.append(link)
        section = soup.new_tag('section', id=f'ejercicio-{n}')
        section['data-notebook'] = path.relative_to(PROC).as_posix()
        content = deepcopy(report.select_one('.jp-Notebook'))
        if content is None:
            raise ValueError(f'No se encontró el contenido de {path.name}')
        # nbconvert coloca jp-Notebook en body: no anidar body/main al unirlo.
        content.name = 'div'
        content['class'] = ['jp-Notebook']
        for inner_main in content.select('main'):
            inner_main.name = 'div'
        # Prefijos por ejercicio: títulos repetidos y estilos de tablas siguen
        # apuntando a sus propios elementos, sin colisiones en el documento unido.
        ids = {el['id']: f'e{n}-{el["id"]}' for el in content.select('[id]')}
        for el in content.select('[id]'):
            el['id'] = ids[el['id']]
        for style in content.select('style'):
            css = style.get_text()
            for old, new in sorted(ids.items(), key=lambda pair: -len(pair[0])):
                css = css.replace('#'+old, '#'+new)
            style.string = css
        for link in content.select('a[href]'):
            href = link['href']
            if href.startswith('#'):
                link['href'] = '#' + ids.get(href[1:], href[1:])
            elif not re.match(r'\w+:', href):
                target = (OUT / f'ejercicio-{n}' / href).resolve()
                link['href'] = os.path.relpath(target, main_path.parent)
        section.append(content)
        soup.main.append(section)
    main_path.write_text(str(soup), encoding='utf-8')
    apply_style(main_path)
    validate(main_path)
    print(main_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Solo verificar la consistencia de salidas existentes')
    args = parser.parse_args()
    validate() if args.check else build()
