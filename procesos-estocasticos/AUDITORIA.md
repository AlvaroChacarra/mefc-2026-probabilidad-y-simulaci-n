# Auditoría de la resolución — Procesos estocásticos

## Veredicto

**APROBADO CON SALVEDAD DE DATO.**

Los tres ejercicios están completos, son reproducibles y superan los controles
analíticos, numéricos, estadísticos y visuales. La salvedad no procede de la
resolución: el Excel de ratings no es cuadrado y no identifica la composición
del bucket Caa-C. La entrega evita ocultarlo mediante un caso base explícito y
un rango completo de sensibilidad.

## Integridad de fuentes

| Fichero | SHA-256 |
|---|---|
| MEFC_2026_examen_procesos.pdf | ca6f567bad241a4de3a5eefb764e9bf4bdf3313753d7cbfa18bb89e7e537f3f5 |
| matriz-ratings.xlsx | eba5c1016fe9a17c25226a83cfe99e303a8801e6d1f21b814a44903b608289e3 |

Los checksums se verificaron contra los adjuntos recibidos. Los binarios
originales se mantienen fuera del historial porque el repositorio es público.

## Cobertura del enunciado

| Apartado | Evidencia | Estado |
|---|---|---|
| 1.a | PD acumulada y primer default 1–25Y para cada rating; tres regímenes gráficos | PASS |
| 1.b | Agregación exacta de la cohorte de 5.002 compañías y sensibilidad Caa-C | PASS |
| 1.c | P^25, distribución por rating inicial y simulación de 300.000 compañías por rating | PASS |
| 2.a | Itô del cociente, término de covariación y condición de martingala verdadera | PASS |
| 2.b | Derivación cerrada, isometría y convergencia de sumas de Itô | PASS |
| 2.c.1 | Dos demostraciones: Itô y esperanza condicional | PASS |
| 2.c.2 | Ley exacta, soporte, esperanza y varianza | PASS |
| 2.c.3 | Trayectorias exactas, fórmulas replicables en Excel y contraste condicional | PASS |
| 3.1 | Verificación completa de la solución mediante Itô | PASS |
| 3.2 | Fórmula europea en función de la varianza acumulada | PASS |
| 3.3 | Inversión de precios, búsqueda multistart, selección no negativa y repricing | PASS |
| 3.4 | Simulación exacta en fijaciones, descuento a 2Y y doble estimador | PASS |

## Controles cuantitativos

### Ejercicio 1

- Las nueve filas del Excel suman uno; error máximo: 2,22e-16.
- Todos los elementos están en [0,1] y Default es absorbente.
- La PD acumulada es monótona y las probabilidades de primer default son no negativas.
- La suma de probabilidades de primer default 1–25Y coincide con la PD 25Y.
- En la validación de P^25, error absoluto máximo 0,001457 y error
  estandarizado máximo 2,16 SE; el gate era 4 SE más tolerancia discreta.
- Sensibilidad de la PD de cohorte a 25Y:
  - w=1 — 100% Caa: 54,1342%;
  - w=0,5: 56,4780%;
  - w=0 — 100% Ca-C: 57,4853%.

### Ejercicio 2

- El drift del cociente se obtiene incluyendo
  d<W1,W2>_t = rho dt; omitirlo produciría un resultado incorrecto.
- La suma de Itô converge a W_t^3/3-tW_t al refinar la malla.
- Para M_1:
  - media teórica 0; simulada -0,000153;
  - varianza teórica 0,222222; simulada 0,221344;
  - contraste KS tras deshacer escala y desplazamiento: p=0,9292.
- Contraste condicional s=0,5, t=1:
  intercepto -0,00056, pendiente 1,00149, sin desvíos materiales por
  quintil del estado inicial.

### Ejercicio 3

- Varianzas acumuladas implícitas:
  0,0521320003, 0,0899877821, 0,3292216020.
- Volatilidades efectivas:
  22,8324%, 26,8310%, 40,5723%.
- Se encuentran cuatro raíces reales del sistema; solo una es no negativa
  en todo [0,2].
- Error máximo de repricing europeo: 2,13e-14.
- Precio asiático principal:
  13,621805, IC 95% por 32 scrambles Sobol
  [13,621644; 13,621966].
- Contraste PRNG independiente:
  13,622091 ± 0,002065; diferencia estandarizada 0,27.
- La raíz con cruce por cero cambia el precio a 13,740158
  (+0,869%), confirmando que la restricción de no negatividad es material.

## Controles de entrega

- Los tres notebooks terminan sin outputs de error.
- Las celdas de código tienen contador de ejecución consecutivo.
- Los HTML contienen tablas, gráficos embebidos y MathML nativo.
- Los HTML no requieren MathJax, CDN ni otros recursos de red.
- Todas las figuras PNG fueron inspeccionadas visualmente.
- Se corrigieron dos incidencias de presentación durante la revisión:
  densidad singular de M_1 y notación con offset del precio asiático.

## Salvedades y alcance

1. **Bucket Caa-C.** Sin el desglose de las 304 compañías o una fila agregada
   suministrada por la fuente, no existe una única matriz multi-periodo. El
   parámetro w queda visible y la sensibilidad cubre todos sus valores extremos.
2. **Precios redondeados.** Las calls se facilitan con dos decimales. Los
   coeficientes calibrados reproducen exactamente esas cotizaciones, pero sus
   últimos dígitos no deben interpretarse como precisión económica.
3. **Modelo.** El intervalo Monte Carlo es mucho más estrecho que la incertidumbre
   de especificación. El precio exótico es condicional a la volatilidad
   cuadrática no negativa elegida.
