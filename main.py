import pandas as pd
from fastapi import FastAPI



def peliculas_idioma( Idioma: str ):

# def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la la duracion y el año.
#                     Ejemplo de retorno: X . Duración: x. Año: xx

# def franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
#                     Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia total de x y una ganancia promedio de xx

# def peliculas_pais( Pais: str ): Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.
#                     Ejemplo de retorno: Se produjeron X películas en el país X

# def productoras_exitosas( Productora: str ): Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.
#                     Ejemplo de retorno: La productora X ha tenido un revenue de x

# def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.