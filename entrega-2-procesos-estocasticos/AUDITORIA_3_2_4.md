# Auditoría de la edición pedagógica 3.2–3.4

Fecha: 13 de septiembre de 2026. Estado: **PASS**.
Rama: `docs/ejercicio-3-2-4-pedagogia`. Sin merge a `main`.

## Fuente, alcance y trabajo paralelo

- Base: `origin/main` en `0fd0d9db72724c591c342575e1648b6c01cc9643`, verificada nuevamente antes de publicar.
- Enunciado original recuperado y leído: `MEFC_2026_examen_procesos.pdf`, SHA-256 `ca6f567bad241a4de3a5eefb764e9bf4bdf3313753d7cbfa18bb89e7e537f3f5`, idéntico al registrado en `0-enunciado/README.md`. El original permanece fuera del repositorio público.
- Apartados confirmados: verificar solución; obtener fórmula europea; calibrar volatilidad cuadrática; simular asiática con fijaciones 1.15, 1.30, 1.60 y 1.70 y pago en 2 años.
- Rama paralela revisada: `docs/ejercicio-3-1-ito-exponencial`, commit `5fae480e20f7ebcd8076fbb2026909099ef28934`. Se leyó su explicación para mantener la filosofía pedagógica, sin incorporar ni modificar esa rama.
- La celda 3.1 permanece exactamente igual a la base. Se usa `Y_i=I_{t_i}` para los shocks de 3.4, evitando colisionar con el exponente `X_t` de la edición paralela de 3.1.

## Cambios pedagógicos

**3.2:** pregunta y payoff; separación determinista/aleatoria; integral como límite de shocks; esperanza frente a realización; varianza mediante independencia e isometría; justificación de gaussianidad e igualdad en distribución; lognormalidad y dispersión; valoración neutral al riesgo; despeje de d₂; indicador y ponderación por el activo para obtener d₁; fórmula final, volatilidad efectiva y caso constante. Se mantiene el límite de varianza nula.

**3.3:** precios → varianzas → ecuaciones → parámetros → selección → repricing. La explicación de la inversión se sitúa antes de su celda. Se desarrolla la derivada positiva de la call respecto a la varianza y la expansión e integración del cuadrado. Se conserva la búsqueda de 2.100 inicializaciones, las cuatro raíces, la convención no negativa y su límite de identificación.

**3.4:** payoff y fecha de cobro → necesidad de distribución conjunta → shocks compartidos y covarianza → incrementos independientes que se acumulan → precios → media y payoff → estimador básico → antitéticos, control geométrico y RQMC → intervalo y contraste PRNG. Se define el papel de cada variable auxiliar y se diferencia error numérico de riesgo de modelo.

La lectura completa 3.1–3.4 se revisó para que cada objeto auxiliar responda a una necesidad del apartado siguiente. No se cambia metodología ni se incorporan resultados nuevos a las celdas de cálculo.

## Resultados antes y después

Los nueve bloques de código son idénticos a la base. Se ejecutó el notebook completo y se compararon todas sus salidas de texto y el contenido de todas sus tablas: coincidencia exacta. Tras esa comprobación se conservaron los outputs originales, incluidos sus identificadores de presentación y figuras, evitando cambios irrelevantes de serialización.

| Resultado | Antes | Después |
|---|---:|---:|
| a | 0.049958716872 | 0.049958716872 |
| b | 0.200094751620 | 0.200094751620 |
| c | 0.099881280434 | 0.099881280434 |
| V(1) | 0.0521320003 | 0.0521320003 |
| V(1.25) | 0.0899877821 | 0.0899877821 |
| V(2) | 0.3292216020 | 0.3292216020 |
| Call 1 año | 9.5500000000 | 9.5500000000 |
| Call 1.25 años | 12.4800000000 | 12.4800000000 |
| Call 2 años | 23.3600000000 | 23.3600000000 |
| Error máximo de repricing | 2.13e-14 | 2.13e-14 |
| Control geométrico | 12.79677073 | 12.79677073 |
| Asiática RQMC + control | 13.62180500 | 13.62180500 |
| Error estándar RQMC | 0.00007890 | 0.00007890 |
| IC 95 % RQMC | [13.62164409; 13.62196591] | [13.62164409; 13.62196591] |
| Contraste PRNG | 13.62209062 | 13.62209062 |
| IC 95 % PRNG | [13.62002576; 13.62415548] | [13.62002576; 13.62415548] |
| Raíz alternativa excluida: asiática | 13.740158 | 13.740158 |

## Comprobaciones realizadas

- Verificación algebraica de 3.1, cancelación de Itô y condición inicial; lectura sin modificación de su celda.
- Revisión del límite en media cuadrática, paso de momentos y ley gaussiana; distinción explícita entre integral, varianza acumulada y varianza del precio.
- Revisión de d₁, d₂, identidad de densidades, descuento, volatilidad efectiva y límite de volatilidad constante.
- Integración numérica independiente del payoff lognormal para los tres vencimientos: diferencias inferiores a 1e-10 respecto al mercado.
- Derivada analítica de la call contrastada por diferencias finitas; cotizaciones estrictamente dentro de sus cotas de no arbitraje.
- Integración numérica independiente del cuadrado del polinomio, positividad analítica por a,b,c > 0 y varianzas crecientes.
- Verificación de que la matriz triangular de incrementos satisface `L @ L.T = min(V_i,V_j)`; reconstrucción del control geométrico con descuento a 2 años.
- Reejecución de todos los controles existentes: raíces, repricing, RQMC, piloto independiente, antitéticos, PRNG y sensibilidad a raíz alternativa.
- Validación del exportador: 23/19/22 celdas, 3/5/2 figuras y 64/174/354 fórmulas en ejercicios 1/2/3; igualdad de contenido entre reportes individuales y `main.html`, sin fórmulas erróneas ni enlaces internos rotos.
- HTML a 390 y 1.100 px: anchura de documento igual a viewport, imágenes cargadas, revisión visual de transiciones, ecuaciones y explicaciones. Las expresiones anchas conservan el desplazamiento local del diseño existente.
- PDF: revisión visual de páginas renderizadas, texto visible de los cuatro apartados, fórmulas, tablas completas y cifras sin superposición. 44 páginas para los tres ejercicios; dos PDF idénticos.
- `git diff --check` y comparación estructural final de todas las celdas de código, outputs y 3.1 con la base.

## Fuentes y regeneración

Los notebooks siguen siendo la única fuente de texto, tablas y figuras de los HTML. Se añade `tools/build_notebooks_pdf.cjs`, llamado mediante `python tools/build_notebooks_procesos.py --pdf`, para exportar el HTML completo a A4. Playwright se fija en `1.62.1`; Chromium puede instalarse con `npx --prefix tools playwright install chromium` o indicarse con `CHROMIUM_EXECUTABLE`.

Los PDF anteriores no estaban sincronizados con los notebooks: eran resúmenes de 16 y 22 páginas. Se sustituyen por una única memoria completa, conservando ambos nombres como alias para no romper enlaces. La tipografía, los colores y las fórmulas proceden del HTML; solo cambian las reglas necesarias para impresión. Los generadores históricos de resúmenes quedan documentados como no vigentes para publicar esta edición.

No se editan a mano HTML ni PDF generados. Los notebooks, HTML individuales y PNG de ejercicios 1 y 2 no cambian. Los Excel no cambian.

## Archivos de esta revisión

- `entrega-2-procesos-estocasticos/3-volatilidad-determinista-asiatica/ejercicio3_volatilidad_determinista_asiatica.ipynb`
- `entrega-2-procesos-estocasticos/output/ejercicio-3/ejercicio3_reporte.html`
- `entrega-2-procesos-estocasticos/output/main.html`
- `entrega-2-procesos-estocasticos/output/procesos_estocasticos.pdf`
- `entrega-2-procesos-estocasticos/output/memoria_detallada.pdf`
- `entrega-2-procesos-estocasticos/README.md`
- `entrega-2-procesos-estocasticos/output/README.md`
- `entrega-2-procesos-estocasticos/AUDITORIA_3_2_4.md`
- `tools/build_notebooks_procesos.py`
- `tools/build_notebooks_pdf.cjs`
- `tools/package.json`
- `tools/package-lock.json`
- `.gitignore`

## Límites y coordinación

No se detecta un error matemático o numérico que requiera cambiar la metodología. La no negatividad sigue siendo un criterio de selección adicional; la búsqueda multiorigen no demuestra unicidad global. El intervalo RQMC es aproximado y no mide riesgo de modelo. Las advertencias de nbconvert sobre texto alternativo de figuras ya existían; las figuras se conservan.

La rama de 3.1 sigue separada. Al integrar ambas revisiones se deben combinar las celdas fuente y regenerar los outputs; no resolver un conflicto de HTML eligiendo ciegamente una de las dos versiones completas. Esta revisión no realiza ese merge.
