# Auditoría independiente — Procesos estocásticos

## Veredicto

**APROBADO — confianza alta.**

**Modo:** exhaustivo, con reejecución limpia y contrastes independientes.

**Cumplimiento del enunciado:** completo.

Los tres ejercicios están resueltos y son reproducibles. No quedan errores
materiales ni hallazgos bloqueantes. La única limitación sustantiva es la
convención del estado `Caa-C`, autorizada expresamente por la profesora y
documentada en todos los entregables.

## Integridad de fuentes

| Fichero | SHA-256 |
|---|---|
| `MEFC_2026_examen_procesos.pdf` | `ca6f567bad241a4de3a5eefb764e9bf4bdf3313753d7cbfa18bb89e7e537f3f5` |
| `matriz-ratings.xlsx` | `eba5c1016fe9a17c25226a83cfe99e303a8801e6d1f21b814a44903b608289e3` |

Los binarios originales se mantienen fuera del historial porque el repositorio
es público. Se usaron copias exactas para la reejecución final.

## Convención de la matriz 9×8

El PDF trabaja con ocho estados, pero el Excel trae nueve filas de origen y ocho
columnas de destino. La profesora aclaró que las transiciones desde `Caa-C`
quedaron desdobladas en `Caa` y `Ca-C`, sin pesos que permitan agregarlas, y
autorizó eliminar una fila.

La resolución:

1. elimina `Ca-C`;
2. conserva `Caa`;
3. renombra la fila conservada como `Caa-C`;
4. no promedia ni inventa ponderaciones.

Esta decisión produce una matriz 8×8 coherente con la distribución inicial del
enunciado.

## Cobertura

| Apartado | Evidencia | Estado |
|---|---|---|
| 1.a | PD acumulada y primer default 1–25Y; tres regímenes gráficos | PASS |
| 1.b | Cohorte de 5.002 compañías bajo la convención autorizada | PASS |
| 1.c | P²⁵ analítica y simulación por rating inicial | PASS |
| 2.a | Itô del cociente, covariación y martingala verdadera | PASS |
| 2.b | Integral cerrada, isometría y convergencia discreta | PASS |
| 2.c.1 | Dos demostraciones de martingala | PASS |
| 2.c.2 | Ley exacta, soporte, esperanza y varianza | PASS |
| 2.c.3 | Trayectorias, 5.000 réplicas y Excel formula-driven | PASS |
| 3.1 | Verificación de la solución de la SDE | PASS |
| 3.2 | Fórmula europea mediante varianza acumulada | PASS |
| 3.3 | Inversión, búsqueda multistart, selección y repricing | PASS |
| 3.4 | Simulación exacta, descuento y doble estimador | PASS |

## Controles cuantitativos

### Ejercicio 1

- Las nueve filas originales suman uno, con error máximo `2,22e-16`.
- Todos los elementos están en `[0,1]` y `Default` es absorbente.
- La matriz operativa conserva exactamente `Caa`, elimina `Ca-C` y la etiqueta
  como `Caa-C`.
- Las PD acumuladas son monótonas; los primeros defaults son no negativos y su
  suma 1–25Y coincide con la PD 25Y.
- Años modales por rating: `[25, 24, 11, 8, 5, 2, 1]`.
- Cohorte: default exacto 1Y `2,2614%`; PD acumulada 25Y `54,1342%`.
- Simulación principal: error máximo `0,001486`; máximo `|z|=2,41`.
- Contraste separado por evolución multinomial de dos millones de compañías por
  rating: error máximo `0,000453`; máximo `|z|=3,05`.

### Ejercicio 2

- La condición correcta del cociente incluye
  `d⟨W¹,W²⟩ₜ=ρdt`; omitirla cambia el drift.
- La integral satisface `Iₜ=Wₜ³/3-tWₜ` y
  `Var(Iₜ)=2t³/3`.
- El notebook, con su propia muestra, obtiene para `M₁` media `-0,000153`,
  varianza `0,221344` y contraste KS `p=0,9292`.
- La regresión condicional de `M₁` sobre `M₀.₅` da intercepto `-0,00056` y
  pendiente `1,00149`.
- Contraste independiente con dos millones de normales: media `0,000286`,
  varianza `0,223597`, error estándar `0,000334` y mínimo superior a `-1/3`.
- Una suma de Itô independiente con 20.000 caminos y 400 pasos presenta RMSE
  `0,0497` frente a la fórmula cerrada, magnitud compatible con esa malla.

### Excel del ejercicio 2.c

El libro `ejercicio2_simulacion_Mt.xlsx` contiene `Resumen`, `Trayectoria` y
`Replica_t1`. Usa incrementos exactos
`ΔAⱼ=√(Δqⱼ)Zⱼ`, con `q(t)=t³/3`, semillas fijas y normales visibles.

| Control | Resultado |
|---|---:|
| Réplicas | 5.000 |
| Media de M₁ | 0,008261710 |
| Varianza muestral | 0,224583814 |
| Error estándar | 0,006701997 |
| IC 95% | [-0,004874204; 0,021397624] |
| Sesgo estandarizado | 1,2327 SE |
| Error absoluto de varianza | 0,002361592 |
| Mínimo | -0,333333301 |
| Holgura sobre la cota | 3,26e-08 |

No aparecen `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` ni `#N/A`. Las tres hojas
se renderizaron e inspeccionaron; el histograma incluye las 5.000 observaciones.

### Ejercicio 3

- Varianzas acumuladas implícitas: `0,0521320003`, `0,0899877821` y
  `0,3292216020`.
- Volatilidades efectivas: `22,8324%`, `26,8310%` y `40,5723%`.
- Se encuentran cuatro raíces reales; solo una es no negativa en `[0,2]`.
- Error máximo de repricing europeo: `2,13e-14`.
- Precio principal: `13,621805`, IC 95% por 32 scrambles Sobol
  `[13,621644; 13,621966]`.
- PRNG del notebook: `13,622091`, diferencia estandarizada `+0,27`.
- Contraste independiente con 100.000 pares piloto y 500.000 pares de
  valoración, antitéticos y control geométrico: `13,622332`, error estándar
  `0,001489`, IC 95% `[13,619414; 13,625250]`; diferencia `0,35 SE` frente al
  principal.
- La raíz con cruce por cero daría `13,740158` (`+0,869%`) y se rechaza por no
  ser una volatilidad no negativa.

## Controles de entrega

- Se ejecutaron las 28 celdas de código en orden, en namespaces limpios.
- Todos los contadores son consecutivos y no existe ningún output de error.
- Los notebooks contienen 9 figuras embebidas y sus copias PNG deterministas.
- Los tres HTML contienen MathML nativo, tablas y gráficos embebidos.
- Los HTML no hacen peticiones de red y pasan el validador de iPhone con
  **0 errores y 0 avisos**.
- La memoria tiene 22 páginas A4, índice y marcadores; sus 22 páginas se
  renderizaron e inspeccionaron sin recortes, solapes ni páginas en blanco.
- No había un navegador headless disponible para medir dinámicamente los tres
  viewports HTML; esta limitación visual no afecta a la validación estática ni
  a la autosuficiencia comprobada.

## Correcciones realizadas durante la auditoría

1. Se explicitó que un máximo en el año 25 es solo el máximo observado dentro
   de la ventana, no un máximo global.
2. El mapa de P²⁵ muestra error estandarizado y su etiqueta coincide con el
   dato representado.
3. Se repuso el signo `+` omitido en la presentación de la dinámica del
   cociente.
4. El intervalo de la sensibilidad del ejercicio 3 se presenta con límites
   inferior y superior, no con un `±` ambiguo.
5. Se preservaron las correcciones previas sobre la densidad singular de `M₁`
   y el descuento de la call asiática.
6. El histograma del Excel se amplió para no truncar 13 observaciones de cola.

## Supuestos y riesgo residual

1. **Bucket Caa-C.** Los resultados del ejercicio 1 son condicionales a la fila
   `Caa` conservada, por autorización docente.
2. **Precios redondeados.** Las calls se facilitan con dos decimales; los
   últimos dígitos de `a`, `b` y `c` son precisión numérica, no económica.
3. **Riesgo de modelo.** El IC Monte Carlo mide error de simulación, no la
   incertidumbre de especificación de `σ(t)`.

## Hallazgos materiales

**Ninguno.** La entrega es coherente, trazable y suficientemente precisa para
el enunciado. El riesgo residual relevante está declarado y no se oculta bajo
una agregación inventada.
