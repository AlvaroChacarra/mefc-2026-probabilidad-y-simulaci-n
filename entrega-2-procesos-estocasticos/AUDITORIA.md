# Auditoría final · Entrega de tres notebooks

**VERDE · PASS · confianza alta.** Revisión del 13/09/2026.

Base: `main` en `0e40912b08ede6d10c65b44a32d4f8a96ac6f00a`.

Si el alumno entrega únicamente estos tres Jupyter notebooks, el profesor dispone
de toda la resolución exigida por el enunciado, incluyendo teoría, cálculos,
simulaciones, resultados, gráficas, interpretación y justificación, sin necesitar
ningún Excel u otro entregable complementario.

## Fuente y autorización de formato

Se leyó el PDF original completo y se inspeccionó su página 2. SHA-256:
`ca6f567bad241a4de3a5eefb764e9bf4bdf3313753d7cbfa18bb89e7e537f3f5`.
El original solicita memoria explicativa y hojas de cálculo; 2.c.3 dice
«Simular en Excel la trayectoria de ese proceso». El alumno confirmó durante esta
sesión que la profesora permite Jupyter para la simulación. El veredicto incorpora
esa autorización; no presupone que el PDF original admita por sí mismo el cambio.

## Cobertura apartado por apartado

Los IDs corresponden a las celdas guardadas dentro de cada notebook.

| Apartado del enunciado | Notebook / celdas que responden | Estado |
|---|---|---|
| 1.a · PD acumulada por rating, años 1–25 | Ejercicio 1: `bfe59764; 6ad27b3f` | PASS |
| 1.a · Primer default por año, gráfica y explicación por rating | Ejercicio 1: `6ad27b3f; 0b705372; 659c831b` | PASS |
| 1.b · Proporción anual de default de la cohorte de 5.002 compañías | Ejercicio 1: `48762b4d; 5ce5ccfc; 5b32b261` | PASS |
| 1.c · Distribución de todos los ratings a 25 años según estado inicial | Ejercicio 1: `c1fc6653; bdf0a249` | PASS |
| 1.c · Compañía aleatoria de la cohorte y comprobación por simulación | Ejercicio 1: `88a7ad97; b74c1768` | PASS |
| Dato original y convención de ocho estados | Ejercicio 1: `d570be1e; 5727c866; 0e2dbc24` | PASS |
| 2.a · Deriva del cociente y martingala verdadera | Ejercicio 2: `be851f40; bc48b4fc` | PASS |
| 2.b · Integral de Itô resuelta y comprobada | Ejercicio 2: `38b17728; 8f33c00a; 279a5458` | PASS |
| 2.c.1 · Dos métodos y demostración de martingala verdadera | Ejercicio 2: `26362b59` | PASS |
| 2.c.2 · Ley, esperanza, varianza y soporte | Ejercicio 2: `d443c12b` | PASS |
| 2.c.3 · Algoritmo y trayectoria simulada | Ejercicio 2: `simulacion-algoritmo; simulacion-trayectoria` | PASS |
| 2.c.3 · Verificación empírica en t=1: momentos y distribución | Ejercicio 2: `simulacion-momentos; simulacion-ley` | PASS |
| Comprobación adicional · Esperanza condicional | Ejercicio 2: `simulacion-condicional-teoria; simulacion-condicional` | PASS |
| 3.1 · Verificar SDE y condición inicial | Ejercicio 3: `b5e82c91` | PASS |
| 3.2 · Derivar precio analítico de la call | Ejercicio 3: `357f8281` | PASS |
| 3.3 · Calibrar a, b, c y reproducir las tres cotizaciones | Ejercicio 3: `09ef3b8a; 0910f481; a57e850c` | PASS |
| 3.4 · Simular fijaciones conjuntas, payoff y pago a 2 años | Ejercicio 3: `18fb481d; bca49e0d` | PASS |
| 3.4 · Resultado e incertidumbre; contraste independiente | Ejercicio 3: `761e3779; a0e09722; 53099190` | PASS |

## Ejecución limpia y autosuficiencia

Cada notebook se copió, sin outputs ni contadores, a una carpeta temporal distinta
que contenía únicamente ese `.ipynb`. Se ejecutaron en orden 1, 2, 3, cada uno en
un proceso nuevo con kernel real `ipykernel.inprocess.InProcessKernel`. Se recogieron
sus mensajes estándar de ejecución y sus contadores reales. TCP e IPC no están
permitidos en este entorno; el kernel en proceso evita necesitar esos transportes,
sin modificar el código de las celdas ni sustituir las gráficas por archivos externos.

| Notebook | Celdas de código | Contadores | Figuras embebidas | Resultado |
|---|---:|---|---:|---|
| Ejercicio 1 | 11 | 1–11 | 3 | PASS |
| Ejercicio 2 | 9 | 1–9 | 5 | PASS |
| Ejercicio 3 | 9 | 1–9 | 2 | PASS |

- Ningún error de ejecución; estructura `nbformat` válida.
- Todos los contadores consecutivos. No se fabricaron los contadores de ejecución.
- Cada carpeta siguió conteniendo solo su notebook al finalizar.
- Cero lecturas de Excel, outputs, HTML/PDF o PNG; cero escrituras de ficheros auxiliares.
- Revisión de las explicaciones, hipótesis y cobertura por notebook; gráficas inspeccionadas.
- Las tablas y las figuras necesarias están guardadas dentro de los `.ipynb`.

## Conservación del ejercicio 1

La única adaptación del dato es su incorporación al notebook. Se compararon las
72 probabilidades originales bit a bit contra Hoja1/C3:J11 del archivo cuyo SHA-256
es `eba5c1016fe9a17c25226a83cfe99e303a8801e6d1f21b814a44903b608289e3`.
No se cambia ningún valor, normalización ni redondeo. Se conserva la matriz 8×8
con Caa como Caa-C y Ca-C descartada, así como todas las explicaciones y cálculos.

Se compararon las tablas y salidas numéricas guardadas contra la base de main:
**igualdad de toda la evidencia numérica del ejercicio 1**, salvo los mensajes
que describen la procedencia del dato. También se verificó igualdad de todas las
tablas y salidas numéricas del ejercicio 3.

## Simulación 2.c: sustitución completa del Excel

- 2.c.1 conserva su derivación y las dos demostraciones de martingala verdadera.
- 2.c.2 conserva el desarrollo analítico de la ley, momentos, soporte y CDF.
- 2.c.3 genera una trayectoria exacta en 101 fechas, muestra sus ocho primeros
  pasos y dibuja M junto a su cota inferior.
- Se conservan los 400.000 pares de la antigua comprobación condicional (semilla
  20260206), y su muestra terminal se reutiliza para todos los contrastes de la ley.
  Desaparecen las 500.000 marginales independientes, la lectura de las 5.000
  réplicas del Excel y el ensemble redundante de 100.000 trayectorias.
- Los prefijos de la misma muestra permiten ver convergencia sin nuevas réplicas.
- Se mantienen cuantiles y CDF; el histograma se normaliza con toda la muestra,
  aunque se limite la vista al percentil 99,5 %.
- Regresión con errores robustos HC1 y diagnóstico por quintiles; se explica por
  qué una media constante o una regresión no prueban por sí solas una martingala.

| Contraste de M₁ | Resultado |
|---|---:|
| Media teórica | 0 |
| Media simulada | -0,000607552 |
| Varianza teórica | 0,222222222 |
| Varianza simulada | 0,222352075 |
| IC 95 % de la media | [-0,002069; 0,000854] |
| Distancia del mínimo a -1/3 | 9,359e-12 |
| KS, valor p | 0,2666 |
| Intercepto / pendiente condicional | -0,000556 / 1,001494 |
| Máximo desvío por quintil | 1,99 SE |

El tercer IC puntual por quintil queda ligeramente fuera de cero; se declara en
el notebook. Los intervalos son puntuales, no simultáneos; no se interpreta su
cobertura como una demostración del proceso.

### Evidencia antes alojada en los Excel

| Evidencia anterior | Ubicación vigente | Estado |
|---|---|---|
| E1: matriz, PD 1–25, primeros defaults, cohorte, P²⁵ y simulación | Notebook 1, tablas completas | PASS |
| E2: hoja Trayectoria | Notebook 2, algoritmo, tabla de pasos y figura | PASS |
| E2: Replica_t1 / Resumen | Notebook 2, código que genera réplicas y contrasta momentos/CDF | PASS |
| E3: cotizaciones, parámetros, fijaciones y valoración | Notebook 3, cálculo y resultados íntegros | PASS |

No se exige adjuntar las antiguas realizaciones aleatorias: la implementación
reproducible y todas las verificaciones necesarias se generan dentro del notebook.

## Verificación numérica con implementaciones independientes

Los contrastes siguientes se calcularon con código distinto del de la solución;
no son una revisión por otro agente.

1. **Ratings:** recurrencia de supervivencia con la submatriz transitoria,
   sin usar potencias de la matriz completa. PD 1Y = 0,022614473918421304;
   PD 25Y = 0,5413420478326217; 2.707,792923 compañías esperadas.
   Años modales: [25, 24, 11, 8, 5, 2, 1]. Coinciden con la resolución.
2. **Itô:** integración numérica de los polinomios contra la densidad normal:
   E[M₁] = 1,04e-17, Var(M₁) = 0,22222222222222227 y
   Var(I₁) = 0,6666666666666667. Verificación algebraica de las derivas y
   revisión de integrabilidad y de las dos demostraciones de martingala.
3. **Calibración:** integración numérica de σ², integración directa del payoff
   lognormal y optimizador `least_squares`, sin reutilizar la fórmula de varianza
   polinómica ni la función de precio del notebook. Coeficientes:
   [0,04995871687243516; 0,2000947516196639; 0,09988128043410571].
   Error máximo de precio: 7,11e-15.
4. **Asiática:** normales conjuntas mediante Cholesky, semilla independiente
   9132026, 500.000 parejas y control geométrico de coeficiente fijo uno;
   su esperanza se calcula por cuadratura. Precio 13,6233540831, SE 0,0016874013;
   diferencia de 0,92 SE frente al precio principal 13,621805.

El notebook 3 conserva su precio principal 13,621805 e IC RQMC
[13,621644; 13,621966]. No se modificaron payoff, fijaciones, calibración, semillas
de valoración, selección de curva ni método numérico. El histograma reutiliza
parejas del contraste ya calculado, en vez de generar otra muestra para dibujarlo.

## Conclusión de aceptación

**PASS en los diez controles solicitados.** Los tres notebooks son la única
entrega vigente. El material de `output/` es histórico y no se utiliza como input.
Los riesgos de modelización ya existentes siguen declarados: convención Caa-C,
cotizaciones redondeadas y selección de la curva de volatilidad no negativa.
