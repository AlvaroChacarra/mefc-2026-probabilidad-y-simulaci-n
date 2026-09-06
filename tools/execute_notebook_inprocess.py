#!/usr/bin/env python3
"""Ejecuta un notebook sin abrir sockets y actualiza sus outputs.

Es una alternativa determinista para entornos aislados donde el kernel de
Jupyter no puede enlazar puertos TCP ni IPC. Las celdas se ejecutan en orden en
un único namespace IPython y se capturan texto, HTML y figuras del backend
inline. En un entorno ordinario se puede seguir usando ``jupyter nbconvert``.
"""

from __future__ import annotations

import argparse
import io
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import Image as IPythonImage, display
from IPython.utils.capture import capture_output


def execute(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    shell = InteractiveShell.instance()
    shell.reset(new_session=True)
    shell.display_formatter.formatters["text/html"].enabled = True
    import matplotlib.pyplot as plt

    def capture_figures():
        for number in plt.get_fignums():
            fig = plt.figure(number)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
            display(IPythonImage(data=buffer.getvalue()))
        plt.close("all")

    shell.user_ns["__capture_figures__"] = capture_figures
    old_cwd = Path.cwd()
    os.chdir(path.parent)
    count = 0
    try:
        for index, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            count += 1
            with capture_output(stdout=True, stderr=True, display=True) as captured:
                executable = cell.source.replace("plt.show()", "__capture_figures__()")
                result = shell.run_cell(executable, store_history=False, silent=False)
            if result.error_before_exec is not None:
                raise RuntimeError(f"Error previo en celda {index}") from result.error_before_exec
            if result.error_in_exec is not None:
                raise RuntimeError(f"Error de ejecución en celda {index}") from result.error_in_exec

            outputs = []
            if captured.stdout:
                outputs.append(nbformat.v4.new_output("stream", name="stdout", text=captured.stdout))
            if captured.stderr:
                outputs.append(nbformat.v4.new_output("stream", name="stderr", text=captured.stderr))
            for rich in captured.outputs:
                outputs.append(nbformat.v4.new_output(
                    "display_data", data=dict(rich.data), metadata=dict(rich.metadata or {})
                ))
            cell.outputs = outputs
            cell.execution_count = count
    finally:
        os.chdir(old_cwd)
        shell.reset(new_session=True)
    nbformat.write(nb, path)
    print(f"✓ {path}: {count} celdas")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebooks", nargs="+", type=Path)
    args = parser.parse_args()
    for notebook in args.notebooks:
        execute(notebook.resolve())


if __name__ == "__main__":
    main()
