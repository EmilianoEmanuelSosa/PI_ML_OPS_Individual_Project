# Movies Repository

Machine Learning Operations (MLOps)

## Descripción

Este proyecto se enfoca en el tratamiento de un Dataset de películas y el despliegue de distintos endpoints, incluyendo un modelo de recomendación de películas.

## Características principales

- **FastAPI**: un framework de desarrollo web de alto rendimiento para construir los endpoints del proyecto ([enlace](https://fastapi.tiangolo.com)).
- **Render**: una plataforma de alojamiento y despliegue de aplicaciones web, para implementar y alojar el proyecto ([enlace](https://render.com)).
- **Datasets**: Se hace uso de los Datasets disponibles en el siguiente enlace: [Datasets](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu) para el análisis y entrenamiento del modelo de recomendación de películas.
- **Diccionario de datos**: El diccionario de datos utilizado se encuentra disponible en el siguiente enlace: [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0) y proporciona información sobre las variables y su significado en el Dataset **movies_dataset**.

## Requisitos

- Tener Python 3.x instalado en tu sistema.
- Ejecutar el siguiente comando en la terminal para instalar las bibliotecas requeridas:

  ```bash
  pip install -r requirements.txt
  ```

Asegúrate de estar ubicado en el directorio del proyecto donde se encuentra el archivo requirements.txt.

Este comando instalará automáticamente todas las bibliotecas necesarias en tu entorno virtual.

Si aún no tienes Python instalado, puedes descargarlo e instalarlo desde el sitio oficial de Python: https://www.python.org.

Guía de Uso de las APIs
A continuación se detallan las diferentes APIs disponibles en el proyecto y có

Ejemplo de uso: https://movies-repository.onrender.com/productoras_exitosas/Pixar Animation Studios
API: get_director
Esta API devuelve información sobre un director de películas, su nombre, el retorno total en sus peliculas y un diccionario con informacion de sus peliculas.

URL: https://movies-repository.onrender.com/get_director/{nombre_director}
Método: GET
Parámetros:
nombre_director: El nombre del director que deseas obtener información.
Ejemplo de uso: https://movies-repository.onrender.com/get_director/Steven Spielberg
API: recomendacion
Esta API devuelve una lista de 5 películas similares al título especificado, en forma de recomendación.

URL: https://movies-repository.onrender.com/recomendacion/{titulo}
Método: GET
Parámetros:
titulo: El título de la película para la cual deseas obtener recomendaciones.
Ejemplo de uso: https://movies-repository.onrender.com/recomendacion/Toy Story
Copy code
