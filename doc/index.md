![image](https://user-images.githubusercontent.com/221018/189548519-f30dff6c-74f4-4b50-943d-c411084b3a4e.png)

# Scikit-Risk. Documentación para usuarios finales.

Scikit-Risk es una biblioteca de Python para el análisis de riesgo mediante simulación de Monte Carlo. Centrada en el análisis de riesgo, se nombró "scikit" porque es una extensión de la biblioteca scipy que funciona como caja de herramientas científicas construida alrededor de SciPy.

Hoy día se existen varias herramientas como las que están listadas acá: [Comparison of risk analysis Microsoft Excel add-ins - Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_risk_analysis_Microsoft_Excel_add-ins) que resultan útiles para el análisis de riesgo pero no son de acceso abierto. Entre las mencionadas, las herramientas que lideran el mercado son:

- @Risk de Palisade https://www.palisade.com/risk/ y
- Crystall Ball (actualmente propiedad de IBM) https://www.oracle.com/middleware/technologies/crystalball.html.

Scikit-Risk se basa de Jupyter y el ecosistema Pandas, lo cual es clave en su uso preferente para manejo de análisis de riesgo.

Los lineamientos para desarrollo de scikits están establecidos en [SciKits &mdash; SciPy.org](https://svn.scipy.org/scikits.html)

Si deseas sumarte al trabajo que se ha realizado para esta biblioteca, debes asegurarte de:

- Seguir los estándares de codificación de Python, es decir, utilizar pylint, black, isort, etc.
- Debes utilizar github flow. Aquí tienes una guía: [Flujo de GitHub - GitHub Docs](https://docs.github.com/es/get-started/quickstart/github-flow)
- Debes implantar pruebas unitarias, utilizando pytest.
- Debes crear los issues a través de la herramienta de seguimiento de las issues en Github. Una vez te hayas incorporado al equipo de forma más activa, podrás hacer revisión de las tareas asignadas.

## Instalación

La última versión estable de esta biblioteca se encuentra directamente desde el repositorio en [Github del proyecto](https://github.com/qu4nt/scikit-risk). Puedes descargarlo como un archivo -zip o clonar el repositorio.

Para instalar Scikit-Risk es deseable que crees un entorno virtual y lo instales ejecutando:

`pip install scikit-risk`

**Ten en cuenta que scikit-risk sólo está disponible para python 3**.

We are currently in active development so we are aiming for the latest versions of each dependency. As soon as a stable version is established, dependencies with particular versions will be indicated.

## [](https://github.com/qu4nt/scikit-risk#setup-a-development-environment)Setup a development environment

Two things to note for those wishing to participate in scikit-risk development:

1. [Github flow](https://docs.github.com/es/get-started/quickstart/github-flow) is being used as a working method.
  
  That is, you create a project fork from [GitHub - qu4nt/scikit-risk: A python library to do Monte Carlo probabilistic modeling and risk analysis.](https://github.com/qu4nt/scikit-risk), to propose any change you create a new branch from this repository and add a Pull Request directly from this new branch.
  
2. To create a development environment you have to clone the repository locally, create a development environment, activate it, and run:
  
  ```shell
  pip install -e .
  ```
  
  From the root folder of scikit-risk
  

Lo mínimo que se espera es:

1. Estructuras de datos que faciliten el ingreso de los datos de forma ordenada y clara.
2. Reporte de cada componentes probabilísticos del modelo.
3. Un mecanismo para ejecutar fácilmente la simulación con algunos parámetros modificables.
4. Generación de reportes vistosos y agradables, similares a los que generan las herramientas de Excel.

Para el ingreso del proyecto se debería utilizar un grafo dirigido acíclico que permita indicar las relaciones entre los distintos componentes del modelo. Este gráfo sera nuestro proyecto de simulación y sobre este se realizará la simulación, y se generarán los reportes.

Otro objetivo es aprovechar al máximo las funcionalidades tanto de Pandas, Scipy como Jupyter para generar celdas interactivas, o reportes interactivos en HTML y Javascript (VUE), eso lo analizaremos más adelante.

Scikit-Risk

 
