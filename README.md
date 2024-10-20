Pilar Leyva Maldonado grupo 14, 8vo spring 

# Urban Routes Test Automation with Selenium and PyTest

Este proyecto automatiza pruebas de rutas urbanas utilizando **Selenium** y **PyTest**. Simula el proceso de solicitar un taxi, seleccionar un tipo de servicio, introducir detalles de pago, y realizar otros pasos como ingresar un mensaje para el conductor y realizar un pedido especial (cubeta de helado). El proyecto está diseñado para ejecutarse utilizando **Selenium WebDriver** con **Google Chrome** y permite la captura de pantallas en distintos pasos del proceso.

## Requisitos

### Instalaciones Previas
- [Python 3.x](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/intl/es/chrome/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
- Editor de código, como [PyCharm](https://www.jetbrains.com/pycharm/)

### Dependencias Python
Este proyecto utiliza las siguientes bibliotecas de Python, que pueden instalarse con `pip`:

```bash
pip install selenium pytest
```

## Execution code

```bash
pytest main.py
``` 

pytest folder/de/proyecto/tests.py

### Explicación adicional:

- **`data.py`**: Este archivo centraliza los datos que se van a utilizar en las pruebas, lo que permite separar la lógica de los test de los datos en sí, facilitando la modificación y reutilización del código.
- **Capturas de pantalla**: Se utilizan en las pruebas para verificar visualmente cada paso del proceso y proporcionar una referencia en caso de errores o fallos en el sistema.

