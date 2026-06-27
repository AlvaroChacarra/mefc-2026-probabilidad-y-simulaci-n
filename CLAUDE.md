# CLAUDE.md — Contexto del Proyecto

## Ficheros disponibles

### 1. `series_macro.xlsx` — Series macroeconómicas (World Bank)

**Estructura:**
- Sheet `Data`: 17 filas × 36 columnas
- Sheet `Series - Metadata`: definiciones y fuentes de cada indicador

**Cobertura:**
- **Países**: Brazil, Chile, France, Italy, Germany
- **Horizonte temporal**: 1991–2024 (34 años anuales)
- **Sin NaNs** en ningún país/serie

**Variables (4 series por país):**

| Serie | Código WB | Fuente |
|---|---|---|
| GDP growth (annual %) | NY.GDP.MKTP.KD.ZG | World Bank / OECD |
| Inflation, GDP deflator (annual %) | NY.GDP.DEFL.KD.ZG | World Bank / OECD |
| Unemployment, total (% of total labor force) | SL.UEM.TOTL.ZS | ILO modelled estimates |
| Deposit interest rate (%) | FR.INR.DPST | IMF / IFS |

**Pivot natural para modelado:**
```
País → 4 series temporales (1991-2024) → matriz 5×4×34
```
→ Listo para PCA por país → índice sintético macroeconómico → matriz de correlaciones 5×5

---

### 2. `MEFC_2026_examen_probabilidad_y_simulacion.pdf` — Examen del Máster

**Asignatura:** Fundamentos Matemáticos — Probabilidad y Simulación  
**Programa:** Máster Executive en Finanzas Cuantitativas 2026 (AFI Global Education)

**Estructura del examen (3 ejercicios, 10 puntos total):**

#### Ejercicio 1 (4 pts) — Monte Carlo e Importance Sampling
Estimar $I = \int_0^1 \cos(\pi x / 2)\, dx$

- **1a.** Determinar $\lambda$ para que $\tilde{f}(x) = \lambda(1-x^2)$ sea densidad en $(0,1)$
- **1b.** Calcular analíticamente, por simulación directa e importance sampling con $\tilde{f}$ (n=200). Requiere resolver ecuación cúbica → **fórmula de Cardano**
- **1c.** Comparar varianza de estimadores (Monte Carlo crudo vs IS) — reducción de varianza

#### Ejercicio 2 (2 pts) — Transformaciones de variables normales
$X \sim N(0,1)$, con $Y = g(X)$ y $Z = h(X)$ definidas a tramos

- **2a.** Simular $f_Y(y)$ para $\alpha \in \{-1, -0.5, 0, 0.5, 1\}$; analizar continuidad
- **2b.** Derivar $f_Y(y)$ analíticamente para $\alpha > 0$ vía $P(Y < y)$
- **2c.** Demostrar y verificar por simulación: $f_Z(z) = \frac{1}{\sqrt{2\pi}}(2ze^{-z^4/2} + e^{-z^2/2})$

#### Ejercicio 3 (4 pts) — Capital Económico con Cópulas ← **usa `series_macro.xlsx`**
Banco con exposición crediticia en Brazil, Chile, France, Italy, Germany

**Parámetros de pérdidas por país (distribución Normal):**

| País | Media | Std |
|---|---|---|
| Brazil | 10 | 0.75 |
| Chile | 15 | 1.00 |
| France | 18 | 3.00 |
| Italy | 12 | 2.30 |
| Germany | 19 | 4.00 |

**Pipeline completo:**
1. **Capital stand-alone**: percentil 95% por país → suma (capital sin diversificación)
2. **PCA por país** sobre las 4 series macro → 1er componente principal = índice sintético
3. **Matriz de correlaciones 5×5** entre índices sintéticos
4. **Simulación Normal Multivariante** con esa matriz → capital diversificado (percentil 95%)
5. **Cópula t-Student** → capital diversificado alternativo
6. **Comparación y discusión**: diversificación + impacto del tipo de cópula

---

## Relación entre ficheros

**`series_macro.xlsx` es el input de datos del Ejercicio 3 del examen.** El enunciado lo referencia explícitamente: *"ver Excel adjunto series_macro.xlsx"*.

El pdf define el problema y los parámetros de pérdidas; el xlsx proporciona los datos históricos para estimar la estructura de correlación entre países. Sin el xlsx, el Ejercicio 3 no se puede resolver.

Flujo de dependencia:

```
series_macro.xlsx
  └─► PCA por país (4 series × 34 años)
        └─► Índice sintético macroeconómico por país
              └─► Matriz de correlaciones 5×5 (Brazil, Chile, France, Italy, Germany)
                    ├─► Simulación Normal Multivariante  ──► Capital diversificado (Cópula Gaussiana)
                    └─► Simulación Cópula t-Student      ──► Capital diversificado (Cópula t)

PDF (Ejercicio 3)
  └─► Parámetros marginales de pérdidas (μ, σ por país)
        └─► Se combina con la matriz de correlaciones del xlsx para construir la distribución conjunta
```

Los países en ambos ficheros coinciden exactamente: Brazil, Chile, France, Italy, Germany.

---

## Capacidades disponibles en este contexto

### Puedo ejecutar directamente:
- ✅ Lectura y manipulación de `series_macro.xlsx` con pandas/openpyxl
- ✅ PCA sobre series temporales (sklearn / numpy)
- ✅ Simulación Monte Carlo (numpy)
- ✅ Cópula Normal multivariante y t-Student (scipy)
- ✅ Fórmula de Cardano (implementación algebraica exacta)
- ✅ Generación de outputs: xlsx con resultados, PDF de memoria

### Entregables que puedo generar:
- Hoja Excel con todas las simulaciones (Ej 1, 2, 3)
- PDF / Markdown con desarrollo teórico y resultados
- Código Python reproducible para cada ejercicio

---

## Notas de contexto

- El examen pide **memoria explicativa (PDF preferible)** + **hojas de cálculo identificadas por ejercicio**
- Trabajo en grupo; un único entregable
- Contacto para dudas: mmartinezbv@gmail.com (Maite Martínez)
- Licencia datos World Bank: CC BY-4.0
