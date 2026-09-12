# Outputs · Entrega 2

Los **tres notebooks son la fuente de contenido**. Cada reporte HTML reproduce
todas sus celdas Markdown, tablas, resultados y figuras; `main.html` reúne los
tres reportes en el mismo orden. El código se puede desplegar, pero las gráficas
y los resultados permanecen visibles. No se transcriben resultados a mano.

## Reconstruir y comprobar

Después de editar y ejecutar los notebooks, desde la raíz del repositorio:

```bash
npm ci --prefix tools
python tools/build_notebooks_procesos.py
python tools/build_notebooks_procesos.py --check
```

La primera orden prepara el renderizador ya utilizado por el proyecto. La
construcción genera los cuatro HTML. El control verifica el número de celdas,
el orden de las fórmulas, las tablas numéricas y las imágenes, además de la
igualdad de contenido entre cada reporte y su sección del HTML conjunto.
También detecta notebooks con errores y enlaces internos rotos.

El comando anterior `python tools/refresh_explanations_procesos.py` sigue
funcionando: ahora reconstruye el contenido completo, no una selección de texto.

## Materiales

| Material | Contenido |
|---|---|
| [main.html](main.html) | Los tres ejercicios completos, offline y con 10 figuras |
| [Ejercicio 1](ejercicio-1/ejercicio1_reporte.html) | Markov: 3 figuras |
| [Ejercicio 2](ejercicio-2/ejercicio2_reporte.html) | Itô: 5 figuras, incluida la muestra del Excel |
| [Ejercicio 3](ejercicio-3/ejercicio3_reporte.html) | Volatilidad y asiática: 2 figuras |
| [procesos_estocasticos.xlsx](procesos_estocasticos.xlsx) | Libro de resultados |
| [ejercicio2_simulacion_Mt.xlsx](ejercicio-2/ejercicio2_simulacion_Mt.xlsx) | Trayectoria y 5.000 réplicas de 2.c |

Los PNG por ejercicio son las mismas figuras guardadas al ejecutar el notebook.
Los HTML incorporan Benton Sans BBVA, colores azules y fórmulas SVG con MathML
semántico: no requieren conexión ni JavaScript y no llevan logotipo.

## Alcance de esta edición

Se mantienen cálculos, semillas y resultados anteriores. Cambia la explicación
y la presentación de las gráficas; se añade la lectura del Excel de 2.c sin
generar otra muestra. Los paneles se apilan y la cohorte deja de utilizar doble
eje. Los reportes se verifican también a anchuras de móvil.

Los PDF [procesos_estocasticos.pdf](procesos_estocasticos.pdf) (16 páginas) y
[memoria_detallada.pdf](memoria_detallada.pdf) (22 páginas) conservan la edición
resumida previa. No son una exportación completa de los notebooks de esta
edición, ni se han regenerado en esta revisión de notebooks y HTML.

Para ejecutar los notebooks, consulta [Reproducir](../README.md#reproducir).
