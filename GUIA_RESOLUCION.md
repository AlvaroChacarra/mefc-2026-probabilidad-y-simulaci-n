# Guía de resolución y formato de los entregables

Este documento fija **cómo se resuelve y se presenta cada ejercicio** del examen,
de modo que los tres ejercicios sean homogéneos en esencia, estilo y calidad.
Se ha destilado a partir de la resolución del **Ejercicio 1** y se aplica por
igual a los Ejercicios 2 y 3.

> **Objetivo pedagógico.** Cada entregable debe demostrar al profesor un
> *entendimiento total* del problema y dejar *evidencia visual*. No basta con el
> resultado: hay que ver el razonamiento matemático, el código que lo
> implementa y los gráficos que lo confirman.

---

## 1. Formato de entrega por ejercicio

Dentro de cada carpeta `N-nombre-ejercicio/`:

| Artefacto | Ruta | Propósito |
|---|---|---|
| **Notebook** | `ejercicioN_*.ipynb` | Resolución completa: teoría (markdown) + código (Python) |
| **Reporte HTML** | `resultados/ejercicioN_reporte.html` | Versión navegable y autocontenida del notebook |
| **Gráficos** | `resultados/grafico_*.png` | Figuras guardadas, también embebidas en el HTML |

No se usan scripts `.py` sueltos para la resolución: **el notebook es el
entregable**. El único `.py` del repositorio es la herramienta de build
`tools/nb_to_html.py` (infraestructura, no solución).

---

## 2. Estructura del notebook

Todo notebook sigue el mismo esqueleto:

1. **Título + Objetivo** (markdown): cabecera del máster, enunciado resumido y
   qué se va a hacer.
2. **Configuración del entorno** (1 celda de código): imports, estilo de
   `matplotlib`, constantes del problema y **semillas fijas**. Centralizar aquí
   mantiene limpio el resto.
3. **Un bloque por apartado**, y dentro de cada apartado:
   - *Markdown* con la **matemática** (desarrollo analítico, fórmulas en LaTeX) y
     una **breve explicación** de qué se hace y por qué.
   - *Código* que lo implementa, **con comentarios que explican cada paso**.
   - **Verificación / validación** (numérica o gráfica) de que el resultado es
     correcto.
4. **Conclusiones** (markdown): tablas-resumen y discusión, con **todos los
   números tomados de las celdas ejecutadas**.

---

## 3. Convenciones de código

- **Markdown para explicar; código para calcular.** Cada celda de código va
  precedida o acompañada de una explicación de qué hace.
- **Setup centralizado**: una sola celda con `import`, `plt.rcParams`, constantes
  y semilla(s). Funciones del problema definidas una vez y reutilizadas.
- **Comentarios paso a paso** dentro de las celdas (`# 1) ...`, `# 2) ...`).
- **Aserciones defensivas** (`assert`) en los puntos donde un error rompería el
  resultado (p. ej. comprobar soporte de una densidad, normalización, etc.).
- **Estilo gráfico coherente** en todo el notebook (mismo `rcParams`).

---

## 4. Reproducibilidad y verificación

- **Semillas fijas** (`np.random.default_rng(SEED)`): los números del texto y de
  las conclusiones deben coincidir *exactamente* con los que produce el código.
  Nunca escribir cifras "a ojo" en el markdown.
- **Tablas-resumen generadas desde código** cuando sea posible, para evitar
  desincronización entre texto y resultados.
- **Verificación cruzada** de cada resultado: analítico vs. simulación,
  `scipy.integrate.quad` para integrales, tests (p. ej. Kolmogórov–Smirnov) o
  diferencias máximas histograma–densidad cuando aplique.

---

## 5. Visualizaciones (evidencia visual)

- Al menos una figura por apartado que **demuestre** el resultado (no decorativa).
- Buenas prácticas: títulos descriptivos, ejes etiquetados, leyenda, y
  superposición de la **curva teórica** sobre el **histograma simulado** para
  evidenciar el acuerdo.
- Guardar cada figura en `resultados/` con `savefig(..., dpi=150, bbox_inches="tight")`.

---

## 6. Generación del reporte HTML (autocontenido y offline)

El HTML se genera con la herramienta del repositorio:

```bash
python tools/nb_to_html.py <ruta>/ejercicioN_*.ipynb <ruta>/resultados/ejercicioN_reporte.html
```

Esta herramienta:
1. Ejecuta `jupyter nbconvert --to html --embed-images` (imágenes embebidas).
2. Convierte el **LaTeX a MathML nativo** (`latex2mathml`), de modo que las
   fórmulas se renderizan **sin depender de ningún CDN de MathJax**.
3. Elimina los scripts externos, dejando un HTML que se visualiza correctamente
   en cualquier navegador moderno **sin conexión a internet**.

Antes de generar el HTML, **ejecutar el notebook entero** para que los outputs
estén actualizados:

```bash
jupyter nbconvert --to notebook --execute --inplace <ruta>/ejercicioN_*.ipynb
```

---

## 7. Convenciones de git

- Mensajes de commit **descriptivos**: título claro + cuerpo explicando qué se ha
  hecho y por qué.
- Un commit coherente por unidad de trabajo (p. ej. "Ejercicio N resuelto").

---

## 8. Checklist antes de dar por cerrado un ejercicio

- [ ] Todos los apartados del enunciado están resueltos.
- [ ] Cada resultado analítico está **verificado por simulación** (o viceversa).
- [ ] Las cifras de las conclusiones **coinciden** con los outputs ejecutados.
- [ ] Hay **evidencia visual** (teoría superpuesta a simulación).
- [ ] El notebook se ejecuta de principio a fin **sin errores**.
- [ ] El reporte HTML se ha regenerado y **renderiza fórmulas y gráficos** offline.
