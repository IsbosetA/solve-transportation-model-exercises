# Documentación de la Aplicación Web para Resolver el Modelo de Transporte

## Descripción

Esta aplicación web permite a los usuarios resolver ejercicios del modelo de transporte mediante la introducción de datos a través de formularios. La aplicación utiliza algoritmos de optimización para calcular la solución óptima, como el **Método de Mínimo Costo** y las **Aproximaciones de Vogel**.

## Requisitos

Para ejecutar esta aplicación, necesitas tener instalado lo siguiente:

- **Python 3.8 o superior**: Para ejecutar el servidor Flask.
- **Flask**: Framework para desarrollar la aplicación web.
- **Numpy**: Para operaciones numéricas.
- **SciPy**: Para algoritmos de optimización.

## Instalación

### Paso 1: Clonar el Repositorio

Si aún no has descargado el proyecto, clónalo usando Git o descarga el archivo ZIP.

```bash
git clone https://github.com/tu-repositorio.git
cd tu-repositorio
```

### Paso 2: Crear un Entorno Virtual

Recomendamos crear un entorno virtual para aislar las dependencias del proyecto.

```bash
python -m venv .venv
```

### Paso 3: Activar el Entorno Virtual

En Windows:

```bash
.venv\Scripts\activate
```

En macOS/Linux:

```bash
source .venv/bin/activate
```

### Paso 4: Instalar Dependencias

Una vez que el entorno virtual esté activo, instala las dependencias necesarias utilizando `pip`:

```bash
pip install -r requirements.txt
```

Si el archivo requirements.txt no está disponible, instala las dependencias manualmente:

```bash
pip install flask numpy scipy
```

### Configuración

La configuración de la aplicación es simple. No se requieren configuraciones adicionales, pero si deseas modificar el comportamiento de la aplicación (como cambiar el puerto o activar/desactivar el modo de depuración), puedes hacerlo desde el archivo `app.py` modificando la siguiente línea:

```python
app.run(debug=True)
```

Cambia debug=True a debug=False si deseas ejecutar la aplicación en modo de producción.

## Uso

### Paso 1: Ejecutar el Servidor

Una vez que hayas instalado las dependencias, ejecuta el servidor Flask:

```bash
python app.py
```

Esto iniciará el servidor en `http://127.0.0.1:5000` (por defecto). Si deseas usar otro puerto, puedes especificarlo así:

```bash
python app.py --port=8000
```

### Paso 2: Ingresar Datos en la Interfaz Web

Abre tu navegador web y ve a `http://127.0.0.1:5000` (o el puerto que hayas configurado).

En la página principal, encontrarás un formulario donde podrás ingresar los datos necesarios para el modelo de transporte:
Fuentes: Los puntos de origen que proveen los recursos.
Destinos: Los puntos de destino a los que se deben transportar los recursos.

Costos de transporte: La matriz de costos entre las fuentes y los destinos.

Suministros y demandas: La cantidad de recursos disponibles en cada fuente y la demanda en cada destino.

### Paso 3: Enviar los Datos

Cuando hayas ingresado todos los datos, presiona el botón para resolver el modelo. La aplicación enviará los datos al servidor y calculará la solución utilizando los algoritmos de optimización.

### Paso 4: Visualizar los Resultados

Una vez procesados los datos, la solución óptima será mostrada en la interfaz, indicando la distribución de los recursos entre los diferentes destinos y los costos asociados.

## API para el Modelo de Transporte

Si deseas integrar esta funcionalidad en otra aplicación o realizar llamadas directas al servidor, puedes utilizar la API REST que hemos implementado.

Endpoint: `POST /api/solve`

```json
{
    "metodo_optimo": "Método de Mínimo Costo",
    "costo_optimo": 2200,
    "matriz_optima": [
        [100, 0, 20],
        [0, 150, 30],
        [20, 0, 130]
    ],
    "comparacion": {
    "Metodo de Mínimo Costo": {
        "costo_total": 2200,
        "matriz_asignacion": [
            [100, 0, 20],
            [0, 150, 30],
            [20, 0, 130]
        ]
    },
    "Metodo de Aproximación de Vogel": {
        "costo_total": 2400,
        "matriz_asignacion": [
            [100, 0, 20],
            [0, 150, 30],
            [20, 0, 130]
      ]
    }
  }
}
```

La respuesta incluirá una matriz que muestra la distribución de los recursos entre los destinos y el costo total mínimo.

## Pruebas

### Datos de Prueba

Suministros: `[100, 150, 200]`
Demandas: `[120, 180, 150]`
Costos de transporte:

```csharp
[
    [8, 6, 10],
    [9, 4, 7],
    [5, 3, 8]
]
```

Puedes ingresar estos datos en la interfaz o utilizarlos para realizar pruebas directas con la API.

### Ejemplo de Llamada API

Prueba la API utilizando herramientas como Postman o directamente con `curl`:

```bash
curl -X POST http://127.0.0.1:5000/api/solve -H "Content-Type: application/json" -d '{
    "supply": [100, 150, 200],
    "demand": [120, 180, 150],
    "costs": [
        [8, 6, 10],
        [9, 4, 7],
        [5, 3, 8]
    ]
}'
```

## Contribución

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-nueva-caracteristica`).
3. Realiza tus cambios y haz un commit (`git commit -am 'Agregada nueva característica'`).
4. Haz un push a tu rama (`git push origin feature-nueva-caracteristica`).
5. Abre un `pull request` para que tus cambios sean revisados.
