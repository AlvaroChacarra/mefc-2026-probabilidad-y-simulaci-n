# Outputs · Entrega 2

La edición ampliada de los ejercicios 2 y 3 está en `main.html`, sus reportes HTML
y los notebooks. Incluye las derivaciones paso a paso y explicita los supuestos
de martingala y selección de la curva de volatilidad. Los dos PDF conservan su
formato resumido, con la misma continuidad pedagógica actualizada en 2.c y 3.

Para sincronizar el HTML conjunto después de editar las explicaciones de los
notebooks: `python tools/refresh_explanations_procesos.py` desde la raíz del repo.
Los reportes individuales se regeneran con `tools/nb_to_html.py`.

Los HTML incorporan Benton Sans BBVA, una paleta azul y ecuaciones SVG ya
compuestas, con el MathML original conservado para accesibilidad. Funcionan sin
red ni JavaScript y no incluyen logotipo. Las ecuaciones largas se distribuyen
en varias líneas cuando se puede preservar su estructura; las restantes tienen
desplazamiento local. La revisión pedagógica modifica solo el texto de los
notebooks: conserva todas las celdas de código, sus resultados y las semillas.

Antes de regenerar: `npm ci --prefix tools`. El renderizador se ejecuta solo al
construir los archivos. Para aplicar el diseño a un HTML existente:
`python tools/style_mobile_html.py entrega-2-procesos-estocasticos/output/main.html`.

Para reconstruir también los PDF desde los datos ya entregados, sin los adjuntos
originales: `python tools/build_output_procesos.py --matriz-operativa` y
`python tools/build_memoria_procesos.py --matriz-operativa`. El primer comando
regenera y sincroniza `main.html`; los reportes individuales se reconstruyen
por separado con `tools/nb_to_html.py`. Las explicaciones resumidas de los PDF
se mantienen en esos dos constructores.

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
