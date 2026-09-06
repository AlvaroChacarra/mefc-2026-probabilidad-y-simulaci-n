# MEFC 2026 — Procesos estocásticos

Resolución completa del examen de **Fundamentos matemáticos · Procesos estocásticos**
del Máster Executive en Finanzas Cuantitativas 2026.

Cada ejercicio incluye:

- notebook ejecutado con teoría, código, aserciones y simulación;
- reporte HTML autocontenido y utilizable sin conexión;
- gráficos de validación guardados en PNG.

El conjunto se completa con una memoria PDF de 22 páginas y el libro Excel
solicitado expresamente en el apartado 2.c.

## Entregables

| # | Tema | Notebook | HTML | Hoja de cálculo |
|---|---|---|---|---|
| 1 | Cadenas de Markov y migración de ratings | [ejercicio1_cadenas_markov_ratings.ipynb](1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb) | [ejercicio1_reporte.html](1-cadenas-markov-ratings/resultados/ejercicio1_reporte.html) | Cálculos reproducibles en el notebook |
| 2 | Cálculo de Itô y martingalas | [ejercicio2_ito_martingalas.ipynb](2-ito-martingalas/ejercicio2_ito_martingalas.ipynb) | [ejercicio2_reporte.html](2-ito-martingalas/resultados/ejercicio2_reporte.html) | [ejercicio2_simulacion_Mt.xlsx](2-ito-martingalas/resultados/ejercicio2_simulacion_Mt.xlsx) |
| 3 | Volatilidad determinista y opción asiática | [ejercicio3_volatilidad_determinista_asiatica.ipynb](3-volatilidad-determinista-asiatica/ejercicio3_volatilidad_determinista_asiatica.ipynb) | [ejercicio3_reporte.html](3-volatilidad-determinista-asiatica/resultados/ejercicio3_reporte.html) | Cálculos reproducibles en el notebook |

La explicación integrada para entregar está en
[MEFC_2026_memoria_procesos_estocasticos.pdf](memoria/MEFC_2026_memoria_procesos_estocasticos.pdf).

Los adjuntos originales no se publican en el repositorio. En
[0-enunciado/](0-enunciado/README.md) están los nombres, checksums e instrucciones
para colocarlos localmente. La revisión independiente queda documentada en
[AUDITORIA.md](AUDITORIA.md).

## Resultados principales

### Ejercicio 1

- El enunciado trabaja con ocho estados. Conforme a la aclaración docente, se
  elimina la fila `Ca-C` del Excel y la fila `Caa` representa el estado `Caa-C`.
- Cohorte: default exacto en 1Y de **2,2614%**; PD acumulada a 25Y de
  **54,1342%**, equivalente a **2.707,79** compañías esperadas.
- La simulación de P^25 queda dentro de **2,41 errores estándar** en las
  56 celdas contrastadas.

### Ejercicio 2

- Para que X_t/N_t sea martingala: mu = sigma·rho - 1/2.
- I_t = W_t^3/3 - tW_t, con Var(I_t)=2t^3/3.
- M_t = (t^3/3)(chi-cuadrado(1)-1), por lo que
  E[M_t]=0 y Var(M_t)=2t^6/9.
- La propiedad de martingala se contrasta también de forma condicional:
  la regresión simulada de M_1 sobre M_0.5 da intercepto -0,00056
  y pendiente 1,00149.
- El Excel de 5.000 réplicas obtiene media **0,008262**, varianza
  **0,224584** e IC 95% para la media **[-0,004874; 0,021398]**; respeta
  además la cota teórica M_1 ≥ -1/3.

### Ejercicio 3

- Volatilidad no negativa calibrada en [0,2]:
  a=0,049958717, b=0,200094752, c=0,099881280.
- Error máximo de repricing de las tres calls: **2,13e-14**.
- Call asiática aritmética: **13,621805**, con IC 95% RQMC
  **[13,621644; 13,621966]**.
- Un Monte Carlo pseudoaleatorio independiente obtiene **13,622091**.
- La raíz algebraica que cruza por cero reproduce las calls, pero daría
  **13,740158** para la asiática; se excluye porque una volatilidad debe ser
  no negativa.

## Reproducibilidad

Desde la raíz del repositorio:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Ejecutar un notebook:

    jupyter nbconvert --to notebook --execute --inplace \
      procesos-estocasticos/1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb

Regenerar un HTML offline:

    python tools/nb_to_html.py \
      procesos-estocasticos/1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb \
      procesos-estocasticos/1-cadenas-markov-ratings/resultados/ejercicio1_reporte.html

Las semillas están fijadas. Los números del README proceden de los notebooks
ejecutados y están cubiertos por aserciones.

En entornos que bloqueen los sockets de Jupyter puede usarse el ejecutor
equivalente `tools/execute_notebook_inprocess.py`, que conserva el orden de las
celdas y actualiza texto, tablas y figuras embebidas.
