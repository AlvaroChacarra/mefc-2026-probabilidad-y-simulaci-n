# MEFC 2026 — Probabilidad y Simulación

Resolución del examen de **Fundamentos Matemáticos · Probabilidad y Simulación** del
**Máster Executive en Finanzas Cuantitativas 2026** (AFI Global Education).

El entregable consta de **tres ejercicios**, cada uno resuelto en un **Jupyter notebook**
explicado (teoría en *markdown* + código *Python* comentado) y acompañado de un
**reporte HTML autocontenido** que se visualiza en cualquier navegador **sin conexión**.

---

## Qué encontrarás en este repositorio

Cada ejercicio vive en su propia carpeta y contiene:

- `ejercicioN_*.ipynb` — el notebook con la resolución completa (matemática + simulación).
- `resultados/ejercicioN_reporte.html` — el mismo contenido como reporte navegable y offline.
- `resultados/grafico_*.png` — las figuras que sirven de evidencia visual.

Todos los notebooks comparten el mismo estilo: **desarrollo analítico riguroso**,
**verificación cruzada** (resultado analítico ↔ simulación), **reproducibilidad** (semillas
fijas; las cifras del texto coinciden con las celdas ejecutadas) y **gráficas explicativas**.

---

## Los tres ejercicios

### 1 · Monte Carlo e Importance Sampling — [`1-monte-carlo-importance-sampling/`](1-monte-carlo-importance-sampling/)

Estimación de $I = \int_0^1 \cos(\pi x/2)\,dx = 2/\pi$ por tres vías: analítica, Monte Carlo
directo e **importance sampling** con la densidad auxiliar $\tilde f(x)=\tfrac32(1-x^2)$.
Incluye la inversión de la CDF resolviendo una **cúbica con la fórmula de Cardano** (elección
de rama) y el análisis de **reducción de varianza**.

> **Resultado clave:** el importance sampling reduce la varianza ≈ **95.6×** frente al Monte
> Carlo directo, porque los pesos $g/\tilde f$ apenas varían.

### 2 · Transformaciones de variables normales — [`2-transformaciones-normales/`](2-transformaciones-normales/)

Con $X\sim N(0,1)$ se estudian $Y=g(X)$ y $Z=h(X)$ definidas a tramos: densidad de $Y$ por
simulación según $\alpha$, derivación analítica de $f_Y$ para $\alpha>0$ vía $P(Y<y)$, y
demostración de $f_Z(z)=\tfrac{1}{\sqrt{2\pi}}(2z\,e^{-z^4/2}+e^{-z^2/2})$ con comprobación
por simulación (tests de Kolmogórov–Smirnov).

> **Resultado clave:** $Y$ es continua salvo en $\alpha=0$, donde aparece un **átomo**
> $P(Y=0)=\tfrac12$; en $\alpha=-1$ resulta $Y=-X\sim N(0,1)$ y en $\alpha=1$, $Y=|X|$.

### 3 · Capital económico con cópulas — [`3-capital-economico-copulas/`](3-capital-economico-copulas/)

Capital económico (percentil 95%) de un banco con exposición en 5 países. Pipeline:
**PCA por país** sobre las series macro (`series_macro.xlsx`) → **matriz de correlaciones 5×5**
→ simulación de pérdidas con **cópula gaussiana** y con **cópula t de Student** → comparación
del capital diversificado y discusión.

> **Resultado clave:** la diversificación reduce el capital de **92.2** (stand-alone) a
> **85.1**; la cópula t es casi idéntica a la gaussiana al 95% pero exige bastante más capital
> en la cola profunda (99.9%), por su **dependencia de colas**.

---

## Estructura del repositorio

```
.
├── 0-enunciado/                     # Enunciado (PDF) y datos (series_macro.xlsx)
├── 1-monte-carlo-importance-sampling/
│   ├── ejercicio1_*.ipynb
│   └── resultados/                  # reporte HTML + gráficos
├── 2-transformaciones-normales/
│   ├── ejercicio2_*.ipynb
│   └── resultados/
├── 3-capital-economico-copulas/
│   ├── ejercicio3_*.ipynb
│   └── resultados/
├── tools/
│   └── nb_to_html.py                # genera el reporte HTML offline (MathML)
├── GUIA_RESOLUCION.md               # formato y convenciones comunes
├── CLAUDE.md                        # contexto del proyecto
└── README.md
```

---

## Cómo usar el repositorio

**Ver los resultados (sin instalar nada):** abre cualquier
`resultados/ejercicioN_reporte.html` en el navegador. Es autocontenido —fórmulas y gráficos
incluidos— y no requiere conexión a internet.

**Reproducir desde cero:**

```bash
# Dependencias
pip install numpy scipy pandas matplotlib openpyxl jupyter latex2mathml beautifulsoup4

# Ejecutar un notebook de principio a fin
jupyter nbconvert --to notebook --execute --inplace \
    1-monte-carlo-importance-sampling/ejercicio1_*.ipynb

# Regenerar el reporte HTML offline
python tools/nb_to_html.py \
    1-monte-carlo-importance-sampling/ejercicio1_*.ipynb \
    1-monte-carlo-importance-sampling/resultados/ejercicio1_reporte.html
```

El detalle del formato, las convenciones de código y el flujo de generación del HTML están
documentados en [`GUIA_RESOLUCION.md`](GUIA_RESOLUCION.md).

---

## Notas

- **Trabajo en grupo**, un único entregable.
- Datos macro: World Bank / OECD / ILO / IMF-IFS (licencia CC BY-4.0).
- Para France, Italia y Alemania la fuente no publica el *tipo de interés de depósito*, por lo
  que disponen de 3 series macro en lugar de 4; la PCA del Ejercicio 3 usa las series
  realmente disponibles de cada país.
