# Entrega 2 · Procesos Estocásticos

Tres ejercicios separados; todos los entregables están en [output/](output/README.md).

| Carpeta | Pregunta | Notebook | Reporte |
|---|---|---|---|
| [0-enunciado](0-enunciado/README.md) | Fuentes y aclaración de la matriz de ratings | Adjuntos locales | Nombres y checksums |
| [1-cadenas-markov-ratings](1-cadenas-markov-ratings/) | Empresa por rating → cohorte → empresa aleatoria y simulación | [Ejercicio 1](1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb) | [HTML](output/ejercicio-1/ejercicio1_reporte.html) |
| [2-ito-martingalas](2-ito-martingalas/) | Itô, integral browniana y martingala cuadrática | [Ejercicio 2](2-ito-martingalas/ejercicio2_ito_martingalas.ipynb) | [HTML](output/ejercicio-2/ejercicio2_reporte.html) |
| [3-volatilidad-determinista-asiatica](3-volatilidad-determinista-asiatica/) | Calibración de volatilidad y valoración asiática | [Ejercicio 3](3-volatilidad-determinista-asiatica/ejercicio3_volatilidad_determinista_asiatica.ipynb) | [HTML](output/ejercicio-3/ejercicio3_reporte.html) |

## Qué entregar

La [memoria unificada HTML](output/main.html) reproduce los tres notebooks completos: explicaciones, tablas y diez figuras, sin omitir sus salidas. Añade el [Excel de resultados](output/procesos_estocasticos.xlsx) y el [Excel de simulación del apartado 2.c](output/ejercicio-2/ejercicio2_simulacion_Mt.xlsx). Los dos PDF se exportan ahora desde esa misma memoria HTML completa; `memoria_detallada.pdf` se conserva como alias de `procesos_estocasticos.pdf`.

## Resultados y convenciones

- **Ratings:** ocho estados; por aclaración docente se conserva `Caa` como representante de `Caa-C` y se descarta `Ca-C`. PD de la cohorte: 2,2614 % en el año 1 y 54,1342 % acumulada a 25 años (2.707,79 compañías esperadas).
- **Simulación de ratings:** 300.000 trayectorias por rating inicial; discrepancia máxima de 2,41 errores estándar. La empresa aleatoria se representa con `p₀P²⁵`; la estimación Monte Carlo mezcla las frecuencias condicionadas con los pesos de la cohorte.
- **Itô:** μ = σρ − 1/2; Iₜ = Wₜ³/3 − tWₜ; E[Mₜ] = 0 y Var(Mₜ) = 2t⁶/9. El Excel obtiene media 0,008262, varianza 0,224584 e IC 95 % [−0,004874; 0,021398].
- **Opciones:** volatilidad no negativa en [0,2], con a = 0,049958717, b = 0,200094752 y c = 0,099881280. Asiática: 13,621805; IC 95 % RQMC [13,621644; 13,621966]. La raíz que cruza por cero queda excluida.

La [auditoría](AUDITORIA.md) conserva la revisión numérica original. La edición pedagógica mantiene cálculos y semillas; la reejecución reproduce las tablas y salidas de texto previas. Cambian el Markdown y las gráficas, y se añade la lectura de las 5.000 réplicas del Excel para contrastar esa misma muestra.

## Reproducir

Desde la raíz del repositorio, con `requirements.txt` instalado:

```bash
jupyter nbconvert --to notebook --execute --inplace \
  entrega-2-procesos-estocasticos/1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb

python tools/nb_to_html.py \
  entrega-2-procesos-estocasticos/1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb \
  entrega-2-procesos-estocasticos/output/ejercicio-1/ejercicio1_reporte.html
```

Cada notebook guarda sus resultados en `../output/ejercicio-N/`. Las semillas están fijadas. Si Jupyter no puede abrir sockets, puede utilizarse `tools/execute_notebook_inprocess.py`.

Después de ejecutar los tres notebooks, reconstruir y comprobar todos los HTML:

```bash
npm ci --prefix tools
python tools/build_notebooks_procesos.py
python tools/build_notebooks_procesos.py --check
```

Los notebooks son la única fuente del texto, las tablas y las figuras del HTML.
El control impide publicar una exportación que omita celdas o gráficas. El código
queda plegado para la lectura, sin ocultar los resultados.

Para regenerar también los PDF completos desde los notebooks ya ejecutados:

```bash
npx --prefix tools playwright install chromium
python tools/build_notebooks_procesos.py --pdf
```

Puede indicarse un Chromium existente mediante `CHROMIUM_EXECUTABLE`. La
exportación conserva la tipografía, los colores, las fórmulas y las figuras del
HTML; adapta únicamente la paginación A4 y omite el código plegado. Los dos
nombres históricos de PDF contienen la misma memoria para evitar divergencias.

`build_output_procesos.py` y `build_memoria_procesos.py` son generadores de la
edición resumida histórica: no deben usarse para publicar la edición actual.
El flujo vigente es `build_notebooks_procesos.py --pdf`, cuya fuente son los
notebooks, sin transcribir explicaciones ni resultados a otra plantilla.

La [auditoría de 3.2–3.4](AUDITORIA_3_2_4.md) documenta el enunciado verificado,
el trabajo paralelo de 3.1, las comprobaciones y la igualdad de resultados.

Los originales de esta entrega no están versionados. [0-enunciado/README.md](0-enunciado/README.md) indica cuáles son y sus checksums. Los HTML, PDF y Excel se pueden consultar sin esos adjuntos.

[Volver al índice](../README.md)
