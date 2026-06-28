# MEFC 2026 — Probabilidad y Simulación

Resolución del examen de **Fundamentos Matemáticos · Probabilidad y Simulación** del
**Máster Executive en Finanzas Cuantitativas 2026** (AFI Global Education).

Cada uno de los **tres ejercicios** está resuelto en un **Jupyter notebook** (teoría explicada
+ código comentado) y acompañado de un **reporte HTML** que se abre en cualquier navegador,
**sin conexión a internet**: las fórmulas y los gráficos van incrustados.

---

## Los tres ejercicios

| # | Carpeta | Tema | Qué encontrarás |
|---|---------|------|-----------------|
| **1** | [`1-monte-carlo-importance-sampling/`](1-monte-carlo-importance-sampling/) | Monte Carlo e Importance Sampling | Estimación de la integral `I = ∫₀¹ cos(πx/2) dx = 2/π` por tres vías (analítica, Monte Carlo directo e importance sampling), inversión de la CDF con la **fórmula de Cardano** y análisis de **reducción de varianza**. |
| **2** | [`2-transformaciones-normales/`](2-transformaciones-normales/) | Transformaciones de una normal | Con `X ~ N(0,1)`, densidad de `Y = g(X)` por simulación según el parámetro α (con análisis de continuidad), derivación analítica de la densidad y demostración de la densidad de `Z = h(X)`, todo verificado por simulación. |
| **3** | [`3-capital-economico-copulas/`](3-capital-economico-copulas/) | Capital económico con cópulas | Capital económico (percentil 95 %) de un banco: **PCA por país** sobre series macro → **matriz de correlaciones 5×5** → simulación de pérdidas con **cópula gaussiana** y **cópula t de Student** → comparación del capital diversificado. |

**Resultados clave:** (1) el importance sampling reduce la varianza ≈ **95×**; (2) `Y` es continua
salvo en α = 0, donde aparece un átomo de probabilidad ½; (3) la diversificación baja el capital de
**92 → 85**, y la cópula t exige mucho más capital en la cola (dependencia de colas).

---

## Ver los reportes (rápido, sin instalar nada)

Abre en tu navegador cualquiera de los reportes — son autocontenidos:

```
1-monte-carlo-importance-sampling/resultados/ejercicio1_reporte.html
2-transformaciones-normales/resultados/ejercicio2_reporte.html
3-capital-economico-copulas/resultados/ejercicio3_reporte.html
```

Esto es suficiente para **leer y revisar** los ejercicios. Si además quieres **ejecutar** el
código, sigue los pasos de abajo.

---

## Reproducir los ejercicios paso a paso

### 1. Descargar el repositorio

```bash
git clone <URL-del-repositorio>
cd mefc-2026-probabilidad-y-simulaci-n
```

### 2. Crear un entorno virtual (recomendado)

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar las librerías

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Abrir y ejecutar los notebooks

```bash
jupyter notebook
```

Navega a la carpeta del ejercicio y abre su `.ipynb`. Para ejecutarlo entero desde la terminal:

```bash
jupyter nbconvert --to notebook --execute --inplace \
    1-monte-carlo-importance-sampling/ejercicio1_monte_carlo_importance_sampling.ipynb
```

### 5. (Opcional) Regenerar el reporte HTML offline

```bash
python tools/nb_to_html.py \
    1-monte-carlo-importance-sampling/ejercicio1_monte_carlo_importance_sampling.ipynb \
    1-monte-carlo-importance-sampling/resultados/ejercicio1_reporte.html
```

El script ejecuta `nbconvert`, convierte el LaTeX a **MathML** e incrusta todo, de modo que el
HTML resultante se ve correctamente sin conexión.

---

## Estructura del repositorio

```
.
├── 0-enunciado/                       # Enunciado (PDF) y datos (series_macro.xlsx)
├── 1-monte-carlo-importance-sampling/
│   ├── ejercicio1_*.ipynb             # notebook con la resolución
│   └── resultados/                    # reporte HTML + gráficos
├── 2-transformaciones-normales/
│   ├── ejercicio2_*.ipynb
│   └── resultados/
├── 3-capital-economico-copulas/
│   ├── ejercicio3_*.ipynb
│   └── resultados/
├── tools/
│   └── nb_to_html.py                  # genera el reporte HTML offline
├── requirements.txt
└── README.md
```

Cada carpeta de ejercicio contiene siempre lo mismo: el **notebook** con la resolución y una
subcarpeta **`resultados/`** con el **reporte HTML** y las **figuras** en PNG.

---

## Notas

- Los datos macro del Ejercicio 3 (World Bank / OECD / ILO / IMF-IFS, licencia CC BY-4.0) cubren
  1991–2024. Para Francia, Italia y Alemania la fuente no publica el *tipo de interés de depósito*,
  por lo que esos países tienen 3 series macro en lugar de 4; la PCA usa las series disponibles.
- Los notebooks fijan las semillas aleatorias: las cifras del texto coinciden con las que produce
  el código al ejecutarse.
