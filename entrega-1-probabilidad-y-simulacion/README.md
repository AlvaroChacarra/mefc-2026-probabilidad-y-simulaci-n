# Entrega 1 · Probabilidad y Simulación

Los tres ejercicios originales se conservan con sus notebooks, resultados y datos.

| Carpeta | Contenido | Reporte |
|---|---|---|
| [0-enunciado](0-enunciado/) | [Enunciado PDF](0-enunciado/MEFC_2026_examen_probabilidad_y_simulacion.pdf) y [series macro](0-enunciado/series_macro.xlsx) | Fuentes originales |
| [1-monte-carlo-importance-sampling](1-monte-carlo-importance-sampling/) | Integral por vía analítica, Monte Carlo e importance sampling; inversión de CDF y reducción de varianza | [Ejercicio 1 · HTML](1-monte-carlo-importance-sampling/resultados/ejercicio1_reporte.html) |
| [2-transformaciones-normales](2-transformaciones-normales/) | Densidades de transformaciones de una normal, continuidad y validación por simulación | [Ejercicio 2 · HTML](2-transformaciones-normales/resultados/ejercicio2_reporte.html) |
| [3-capital-economico-copulas](3-capital-economico-copulas/) | PCA por país, correlaciones y capital económico con cópula gaussiana y t de Student | [Ejercicio 3 · HTML](3-capital-economico-copulas/resultados/ejercicio3_reporte.html) |

Cada ejercicio contiene su notebook ejecutado y una carpeta `resultados/` con HTML y gráficos. Los reportes son autocontenidos y funcionan offline. La [guía de resolución](GUIA_RESOLUCION.md) recoge el criterio pedagógico y de presentación.

## Resultados de referencia

- Importance sampling reduce la varianza aproximadamente 95 veces.
- La transformación Y es continua salvo para α = 0, donde aparece un átomo de probabilidad 1/2.
- La diversificación reduce el capital de 92 a 85; la cópula t refleja una mayor dependencia de colas.

Los datos macro (World Bank / OECD / ILO / IMF-IFS, CC BY-4.0) cubren 1991–2024. Francia, Italia y Alemania tienen tres series disponibles por carecer de tipo de interés de depósito; la PCA utiliza las series disponibles.

## Reproducir

Instala las dependencias del repositorio y ejecuta cada notebook desde su carpeta. Por ejemplo, desde la raíz del repo:

```bash
jupyter nbconvert --to notebook --execute --inplace \
  entrega-1-probabilidad-y-simulacion/1-monte-carlo-importance-sampling/ejercicio1_monte_carlo_importance_sampling.ipynb

python tools/nb_to_html.py \
  entrega-1-probabilidad-y-simulacion/1-monte-carlo-importance-sampling/ejercicio1_monte_carlo_importance_sampling.ipynb \
  entrega-1-probabilidad-y-simulacion/1-monte-carlo-importance-sampling/resultados/ejercicio1_reporte.html
```

[Volver al índice](../README.md)
