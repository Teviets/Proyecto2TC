# Proyecto 2 Teoria de la computacion

# CYK Parser con Lectura de Gramáticas

Este proyecto implementa el algoritmo **CYK (Cocke-Younger-Kasami)** para el análisis sintáctico de oraciones, utilizando una gramática en **Forma Normal de Chomsky** (FNC). La gramática se lee desde un archivo, y se analiza si una oración dada es sintácticamente correcta o no.

## Estructura del Proyecto

- `CYK`: Clase que implementa el algoritmo CYK.
- `Cell`: Clase auxiliar utilizada en el algoritmo CYK para manejar las reglas gramaticales en las celdas de la tabla.
- `Lectura`: Clase que lee y procesa la gramática desde un archivo de texto.
  
## Requisitos Previos

Antes de ejecutar este proyecto, asegúrate de tener instalado Python 3.x en tu sistema. También es necesario que el archivo que contiene la gramática esté en formato adecuado y que la terminal en la que corre el programa este dentro de la carpeta 'main'.

### Ejemplo de Gramática en Forma Normal de Chomsky

El archivo de gramática debe estar en formato FNC y puede contener reglas en el siguiente formato:

```plaintext
S -> NP VP
NP -> Det N
VP -> V NP | V NP PP
PP -> P NP
Det -> a | the
N -> dog | cat
V -> chases | sees
P -> with | on
```

Este archivo debe ser guardado con extensión `.txt` y su ruta será proporcionada al programa.

## Instalación

1. Clona el repositorio o descarga los archivos.

2. Asegúrate de tener un entorno de Python 3 instalado. Puedes crear un entorno virtual con los siguientes comandos:

   ```bash
   python -m venv env
   source env/bin/activate  # En Linux/Mac
   .\env\Scripts\activate  # En Windows
   ```

3. Si utilizas dependencias adicionales, instala los paquetes necesarios:

   ```bash
   pip install -r requirements.txt
   ```

4. Coloca tu archivo de gramática en el mismo directorio o asegúrate de conocer su ruta.

## Uso

1. Crea un archivo de gramática (por ejemplo, `gramatica.txt`) con las reglas en FNC.

2. Carga el archivo de gramática usando la clase `Lectura`, y luego ejecuta el análisis sintáctico usando la clase `CYK`.

### Ejemplo de Código

```python
from lectura import Lectura
from cyk import CYK

# Cargar la gramática
lectura = Lectura('gramatica.txt')
non_terminals, terminals, productions, start_symbol = lectura.read()

# Inicializar el CYK con las reglas de la gramática
cyk = CYK(productions)

# Ejecutar el parser sobre una oración de prueba
cyk.CYKParser("the dog chases the cat")
```

3. El resultado indicará si la oración es sintácticamente correcta o no, y mostrará el tiempo de ejecución junto con el árbol de análisis.

### Salida Esperada

Si la oración es correcta:

```plaintext
La frase es sintácticamente correcta (Sí)
Tiempo de ejecución: 0.00123 segundos
Árbol de análisis: ['S -> NP VP']
```

Si la oración es incorrecta:

```plaintext
La frase no es sintácticamente correcta (No)
Tiempo de ejecución: 0.00045 segundos
```

## Estructura de Archivos

- `cyk.py`: Contiene la clase CYK y su implementación.
- `lectura.py`: Contiene la clase Lectura, que procesa la gramática desde un archivo.
- `gramatica.txt`: Un archivo de ejemplo con una gramática en FNC (proporcionado por el usuario).

## Consideraciones

- Asegúrate de que las reglas de gramática estén en **Forma Normal de Chomsky**.
- Las reglas deben estar correctamente formateadas. Cada regla debe estar separada por el símbolo `->` o `→` y las alternativas con `|`.

## Participantes

Este proyecto fue desarrollado con la colaboración de:

- **Sebastian Estrada** - 21405
- **Diego Valdez** - 21328

## Link al vídeo:

https://youtu.be/4kWgmCqNKCQ

