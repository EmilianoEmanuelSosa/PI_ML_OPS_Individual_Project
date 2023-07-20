import pandas as pd
import numpy as np
from fastapi import FastAPI
import iso639
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Crear una instancia de la aplicación
app = FastAPI()
# Cargamos el dataframe
movies = pd.read_csv('Dataset_Api_Web/Movies_Credits_Merged.csv')




@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma: str):
    """
    Obtiene la cantidad de películas disponibles en un idioma específico.

    Parameters:
        - idioma (str): Idioma para el cual se desea obtener la información.Se debe ingresar el codigo del pais: por ejemplo "en" de English.
    Returns:
        - dict: Un diccionario que contiene el idioma y la cantidad de películas disponibles.
                En caso de que no se encuentre información para el idioma, se retorna un mensaje de error.
    """
    idioma_nombre = None
    try:
        codigo_iso639 = iso639.to_iso639_1(idioma.lower())
        idioma_nombre = iso639.to_name(codigo_iso639)
    except ValueError:
        return f"No se encontró información para el idioma {idioma}"

    # Filtrar las películas por el código ISO del idioma
    cantidad_peliculas = len(movies[movies['original_language'] == codigo_iso639])

    return {'idioma': idioma, 'cantidad': cantidad_peliculas}



@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula: str):
    """
    Obtiene la duración y el año de una película específica.

    Parameters:
        - pelicula (str): Nombre de la película para la cual se desea obtener la información.

    Returns:
        - dict: Un diccionario que contiene el nombre de la película, su duración y su año de lanzamiento.
                En caso de que no se encuentre información para la película, se retorna un mensaje de error.
    """
    # Filtra el DataFrame por la película ingresada
    pelicula_filtrada = movies[movies['title'] == pelicula]

    # Verifica si se encontró la película
    if pelicula_filtrada.empty:
        return f"No se encontró información para la película '{pelicula}'."

    # Obtiene la duración y el año de la película
    duracion = pelicula_filtrada['runtime'].values[0].item()
    anio = pelicula_filtrada['release_year'].values[0].item()

    # Devuelve la duración y el año de la película
    return {'pelicula': pelicula, 'duracion': duracion, 'anio': anio}




@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    """
    Obtiene información sobre una franquicia específica, incluyendo la cantidad de películas,
    la ganancia total y la ganancia promedio de la franquicia.

    Parameters:
        - franquicia (str): Nombre de la franquicia para la cual se desea obtener la información.

    Returns:
        - dict: Un diccionario que contiene el nombre de la franquicia, la cantidad de películas,
                la ganancia total y la ganancia promedio. En caso de no encontrar información para la franquicia,
                se retorna un mensaje de error.
    """
    # Validar que el parámetro franquicia no esté vacío
    if not franquicia:
        return "El parámetro franquicia no puede estar vacío."

    # Convertir el nombre de la franquicia a minúsculas y eliminar espacios en blanco al principio y al final
    franquicia = franquicia.lower().strip()

    # Limpia los valores NaN en la columna "Collections"
    movies_cleaned = movies.dropna(subset=['Collections'])

    # Filtra el DataFrame por la franquicia ingresada (en minúsculas)
    franquicia_filtrada = movies_cleaned[movies_cleaned['Collections'].str.lower().str.contains(franquicia, flags=re.IGNORECASE)]

    # Verifica si se encontró la franquicia
    if franquicia_filtrada.empty:
        return f"No se encontró información para la franquicia '{franquicia}'."

    # Calcula la cantidad de películas de la franquicia
    cantidad_peliculas = len(franquicia_filtrada)

    # Calcula la ganancia total y promedio de la franquicia
    ganancia_total = franquicia_filtrada['revenue'].sum()
    ganancia_promedio = franquicia_filtrada['revenue'].mean()

    # Devuelve la información de la franquicia
    return {'franquicia': franquicia, 'cantidad': cantidad_peliculas, 'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}





@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora: str):
    """
    Obtiene información sobre una productora específica, incluyendo el total de ingresos generados
    por sus películas y la cantidad de películas producidas por la productora.

    Parameters:
        - productora (str): Nombre de la productora para la cual se desea obtener la información.

    Returns:
        - dict: Un diccionario que contiene el nombre de la productora, el total de ingresos generados
                por sus películas y la cantidad de películas producidas por la productora. En caso de no encontrar
                películas para la productora, se retorna un mensaje de error.
    """
    # Validar que el parámetro productora no esté vacío
    if not productora:
        return "El parámetro productora no puede estar vacío."

    # Eliminar espacios en blanco al principio y al final del nombre de la productora
    productora = productora.strip()

    # Filtra el DataFrame por la productora ingresada (ignorando mayúsculas y minúsculas)
    productora_films = movies[movies['production_companies'].apply(lambda x: productora.lower() in x.lower())]

    if productora_films.empty:
        return f"No se encontraron películas para la productora {productora}."
    else:
        # Calcula el total de ingresos generados por las películas de la productora
        total_revenue = productora_films['revenue'].sum()

        # Calcula la cantidad de películas producidas por la productora
        cantidad_peliculas = len(productora_films)

        # Devuelve la información de la productora
        return {'productora': productora, 'revenue_total': total_revenue, 'cantidad': cantidad_peliculas}






@app.get('/peliculas_pais/{Pais}')
def peliculas_pais(Pais: str):
    """
    Obtiene la cantidad de películas producidas en un país específico.

    Parameters:
        - Pais (str): Nombre del país del cual se desea obtener la cantidad de películas producidas.

    Returns:
        - str: Un mensaje que indica la cantidad de películas producidas en el país especificado.

    Explanation:
        Esta función recibe como parámetro el nombre de un país y realiza un filtrado en el DataFrame para obtener
        las películas que se han producido en ese país. Luego, se cuenta la cantidad de películas obtenidas y se
        retorna un mensaje que indica dicha cantidad junto con el nombre del país.

        Por ejemplo, si se ingresa el país 'Estados Unidos', la función retornará el mensaje:
        "Se produjeron X películas en el país Estados Unidos."
    """
    # Aplica lower() y strip() al país ingresado
    pais_limpiado = Pais.lower().strip()

    # Filtra el DataFrame por el país ingresado
    peliculas_por_pais = movies[movies['production_companies'].str.contains(pais_limpiado, case=False)]

    # Obtiene la cantidad de películas producidas en el país
    cantidad_peliculas = len(peliculas_por_pais)

    return f"Se produjeron {cantidad_peliculas} películas en el país {Pais}."

print(peliculas_pais('Esta'))



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    """
    Obtiene información sobre un director y sus películas.

    Parameters:
        - nombre_director (str): Nombre del director del cual se desea obtener información.

    Returns:
        - dict: Un diccionario que contiene el promedio de éxito del director y una lista de películas
                dirigidas por el director.

    Explanation:
        Esta función recibe como parámetro el nombre de un director y realiza un filtrado en el DataFrame para
        obtener las películas dirigidas por ese director. Luego, se calcula el promedio de éxito de las películas
        (considerando la columna 'return') y se limita la cantidad de películas a devolver. Finalmente, se retorna
        un diccionario que contiene el promedio de éxito del director y una lista de las películas dirigidas por él.

        Si no se encuentran películas para el director especificado, se retornará el mensaje:
        "No se encontraron películas para el director {nombre_director}."
    """
    # Validar que el parámetro nombre_director no esté vacío
    if not nombre_director:
        return "El parámetro nombre_director no puede estar vacío."

    # Eliminar espacios en blanco al principio y al final del nombre del director
    nombre_director = nombre_director.strip()

    # Filtra el DataFrame por el nombre del director ingresado (ignorando mayúsculas y minúsculas)
    director_films = movies[movies['director'].str.lower().str.strip() == nombre_director.lower().strip()]

    if director_films.empty:
        return f"No se encontraron películas para el director {nombre_director}."

    # Limpia los valores 'N/A' y reemplaza los valores 'inf' y 'nan' en el DataFrame
    director_films = director_films.replace({'N/A': np.nan, np.inf: np.nan})

    # Calcula el promedio de éxito de las películas del director sin considerar los valores NaN
    director_success = director_films['return'].mean(skipna=True)

    # Limita la cantidad de películas a devolver
    max_movies = 6  # Puedes ajustar este valor según tus necesidades
    director_films = director_films.head(max_movies)

    # Crea una lista de películas dirigidas por el director
    movie_list = director_films[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')

    return {'director_success': director_success, 'lista_peliculas': movie_list}





@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    """
    Obtiene una lista de recomendaciones de películas similares a una película dada.

    Parameters:
        - titulo (str): Título de la película para la cual se desea obtener recomendaciones.

    Returns:
        - dict: Un diccionario que contiene una lista de títulos de películas recomendadas similares
                a la película dada.
    """
    # Convertir el título ingresado a minúsculas y eliminar espacios adicionales
    titulo = titulo.lower().strip()

    # Verificar si el título está en la columna 'title' del dataframe movies
    pelicula = movies[movies['title'].str.lower().str.strip() == titulo]

    if pelicula.empty:
        return f"No se encontró información para la película '{titulo}'."

    # Obtener las características de género de la película de interés
    generos_pelicula = pelicula['name_genre'].iloc[0].split(',')

    # Obtener la matriz de características de género de todas las películas
    generos = movies['name_genre'].str.get_dummies(',')

    # Obtener la matriz de puntuaciones de todas las películas
    puntuaciones = movies[['vote_average', 'vote_count']].values

    # Combinar las matrices de género y puntuaciones
    caracteristicas = pd.concat([generos, pd.DataFrame(puntuaciones, columns=['vote_average', 'vote_count'])], axis=1)

    # Calcular la similitud de coseno entre la película ingresada y todas las demás películas basada en características
    similitudes = cosine_similarity(caracteristicas.loc[pelicula.index], caracteristicas)

    # Obtener los índices de las películas más similares (excluyendo la película ingresada)
    indices_similares = similitudes.argsort()[0][::-1][1:]

    # Obtener los títulos de las 5 películas más similares
    peliculas_similares = movies.iloc[indices_similares][:5]['title'].tolist()

    return {'lista_recomendada': peliculas_similares}

print(recomendacion('The Dark Knight'))
