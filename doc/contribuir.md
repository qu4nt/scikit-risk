## Cómo contribuir

Los lineamientos para desarrollo de scikits están establecidos en [SciKits — SciPy.org](https://svn.scipy.org/scikits.html). Si deseas sumarte al trabajo que se hacemos en esta biblioteca, debes asegurarte de:

- Seguir los estándares de codificación de Python, es decir, utilizar pylint, black, isort, etc.
- Debes utilizar github flow. Aquí tienes una guía: [Flujo de GitHub - GitHub Docs](https://docs.github.com/es/get-started/quickstart/github-flow)
- Debes implantar pruebas unitarias, utilizando pytest.
- Debes crear los issues a través de la herramienta de seguimiento de las issues en Github. Una vez te hayas incorporado al equipo de forma más activa, podrás hacer revisión de las tareas asignadas.

Si deseas sumarte al equipo de desarrollo, puedes contactarnos a través de [hola@qu4nt.com](mailto:hola@qu4nt.com)

## [Cómo configurar un entorno de desarrollo](https://github.com/qu4nt/scikit-risk#setup-a-development-environment)

Para participar en el desarrollo de este proyecto, te pedimos que tengas en cuenta lo siguiente:

1. Utilizamos [Github flow](https://docs.github.com/es/get-started/quickstart/github-flow) como método de trabajo. Esto quiere decir que debes crear un fork de este proyecto, tomándo desde [GitHub - qu4nt/scikit-risk: A python library to do Monte Carlo probabilistic modeling and risk analysis](https://github.com/qu4nt/scikit-risk).

2. A fin de proponer cualquier cambio, debes crear una nueva rama de este repositorio y agregar un Pull Request directamente desde la nueva rama.

3. Para crear un entorno de desarrollo, debes clonar el repositorio de forma local, crear el entorno de desarrollo, activarlo y ejecutar:
   
   ```shell
   pip install -e .
   ```
   
   desde la carpeta raíz de scikit-risk


