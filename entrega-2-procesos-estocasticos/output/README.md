# Outputs · Entrega 2

La edición ampliada de los ejercicios 2 y 3 está en `main.html`, sus reportes HTML
y los notebooks. Incluye las derivaciones paso a paso y explicita los supuestos
de martingala y selección de la curva de volatilidad. Los PDF conservan la
edición resumida anterior.

Para sincronizar el HTML conjunto después de editar las explicaciones de los
notebooks: `python tools/refresh_explanations_procesos.py` desde la raíz del repo.
Los reportes individuales se regeneran con `tools/nb_to_html.py`.

| Material | Uso |
|---|---|
| [main.html](main.html) | Documento unificado de los tres ejercicios, lectura vertical y offline |
| [procesos_estocasticos.pdf](procesos_estocasticos.pdf) | Mismo documento en PDF, 16 páginas |
| [procesos_estocasticos.xlsx](procesos_estocasticos.xlsx) | Libro que reproduce los resultados de la entrega |
| [ejercicio2_simulacion_Mt.xlsx](ejercicio-2/ejercicio2_simulacion_Mt.xlsx) | Hoja de simulación solicitada en 2.c |
| [memoria_detallada.pdf](memoria_detallada.pdf) | Memoria complementaria de decisiones y controles, 22 páginas |

Los reportes y gráficos por ejercicio se agrupan en:

- [ejercicio-1/](ejercicio-1/): [reporte de ratings](ejercicio-1/ejercicio1_reporte.html) y tres figuras.
- [ejercicio-2/](ejercicio-2/): [reporte de Itô](ejercicio-2/ejercicio2_reporte.html), simulación Excel y cuatro figuras.
- [ejercicio-3/](ejercicio-3/): [reporte de volatilidad y asiática](ejercicio-3/ejercicio3_reporte.html) y dos figuras.

Para regenerar, consulta las [instrucciones de la entrega](../README.md#reproducir). Los notebooks están en sus carpetas de ejercicio; aquí se reúnen las salidas.
