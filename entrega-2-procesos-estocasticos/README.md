# Entrega 2 · Procesos Estocásticos

## Entrega definitiva: solo tres notebooks

1. [ejercicio1_cadenas_markov_ratings.ipynb](1-cadenas-markov-ratings/ejercicio1_cadenas_markov_ratings.ipynb)
2. [ejercicio2_ito_martingalas.ipynb](2-ito-martingalas/ejercicio2_ito_martingalas.ipynb)
3. [ejercicio3_volatilidad_determinista_asiatica.ipynb](3-volatilidad-determinista-asiatica/ejercicio3_volatilidad_determinista_asiatica.ipynb)

Los tres archivos contienen toda la resolución: teoría, cálculos, datos, simulaciones,
tablas, gráficas, resultados e interpretación. No necesitan Excel, HTML, PDF, imágenes
externas ni resultados previos. La matriz original de ratings está incorporada con
su precisión íntegra; la convención Caa-C y los cálculos se conservan.

El alumno confirmó el 13/09/2026 que la profesora permite Jupyter para la simulación
que el PDF original solicita en Excel.

## Ejecutar

Abrir cada notebook en Jupyter y elegir **Restart Kernel and Run All Cells**.
Se puede copiar cada `.ipynb` a cualquier carpeta y ejecutarlo solo. Requiere Python 3,
NumPy, pandas, Matplotlib, SciPy y Jupyter/IPython. No se necesita conexión de red
para los cálculos una vez instalado el entorno. Los resultados ya están guardados.

## Validación

La [auditoría final](AUDITORIA.md) contrasta todos los apartados del enunciado y
registra ejecución aislada: 29 celdas de código sin errores, contadores consecutivos
y 10 figuras embebidas. Cada notebook incluye su propia matriz de cobertura.

Los resultados numéricos del ejercicio 1 y del 3 coinciden con la versión anterior:
PD 25Y de la cohorte 54,1342 % y asiática 13,621805. En 2.c, la simulación se construye
en Python y una única muestra de 400.000 pares sirve para los contrastes marginales
y condicionales; se mantiene la muestra condicional anterior.

## Material histórico

`output/` y las herramientas de exportación conservan versiones anteriores para
consulta. **No forman parte de la entrega vigente y pueden diferir de los notebooks
actuales.** No hay que entregar ni regenerar esos archivos.

Los documentos de auditoría anteriores se conservan como historial cuando están
identificados como tales; el informe vigente es `AUDITORIA.md`.
