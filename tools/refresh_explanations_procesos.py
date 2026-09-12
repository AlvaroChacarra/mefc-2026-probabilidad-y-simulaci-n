#!/usr/bin/env python3
"""Compatibilidad: reconstruye todos los HTML desde los tres notebooks.

Ya no copia una selección de Markdown: también incorpora todas las tablas
y figuras. El nombre se mantiene para los flujos de construcción existentes.
"""
from build_notebooks_procesos import build


def refresh(path=None):
    build(path)


if __name__ == "__main__":
    refresh()
