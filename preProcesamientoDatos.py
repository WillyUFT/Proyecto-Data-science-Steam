# Importamos las bibliotecas
import pandas
import numpy

# Importamos bibliotecas de tiempo
import time  # Para ver cuanto nos demoramos
import datetime  # Para ver cuanto nos demoramos, pero lindo

# Importamos las funciones extra
import funcionesExtra as funEx

# Importamos las librerías de las palabras malas
import nltk
from nltk.corpus import stopwords  # Este es para sacar las palabras no deseadas

# Importamos el csv con las reseñas y el de los datos
reviewsCsv = "reviews.csv"
dataJuegosCsv = "steam.csv"

# Comenzamos a contar el tiempo
inicioTiempoReviews = time.time()

# Creamos un dataframe con pandas.
reviewsDF = pandas.read_csv(reviewsCsv, header=0)

# Vamos a dejar solo 200 reviews de cada juego, porque de lo contrario es infumable
newReviews = reviewsDF.groupby("id_game").sample(200, replace=True)

# Vamos a eliminar todas las reviews que estén repetidas.
newReviews = newReviews.drop_duplicates(subset=["review"], keep="first")

# También vamos a ordenarlos por nombre del juego
newReviews = newReviews.sort_values("title_game")

# Ahora vamos a eliminar la columna de id_game, no sirve pa na
newReviews = newReviews.drop(columns=["id_game", "review_recomend"])

# Creamos unos headers que sean legibles
newReviews = newReviews.set_axis(
    ["name", "review", "recomended"], axis=1, inplace=False
)

# Eliminamos los valores vacío
newReviews = newReviews.dropna()

# Vamos a mostrar un ejemplo de como se ve la tabla
vallhalla = newReviews.loc[newReviews["name"] == "VA-11 Hall-A: Cyberpunk Bartender Action"]

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
print(vallhalla.head(20))

# Vamos a limpiar las reviews
newReviews["review"] = newReviews["review"].apply(lambda x: funEx.limpiar_texto(x))

# Tenemos que volver a una estructura ordenada, pues con la tokenización se nos
# desordena la tabla
reviewsSeiso = newReviews.explode(column="review")

# Vamos a eliminar las stopwords
reviewsSeiso = funEx.eliminar_stopwords(reviewsSeiso, "review")

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalReviews = time.time() - inicioTiempoReviews
print(
    "Para hacer la base más pequeña y limpiarla nos demoramos "
    + str(datetime.timedelta(seconds=tiempoFinalReviews))
    + " segundos"
)

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
example = reviewsSeiso.groupby("name").sample(4, replace=True)
print(example.head(50))

# Comenzamos a contar el tiempo, pero para el catálogo
inicioTiempoCatalogo = time.time()

# Vamos a hacer otro data set que tenga los juegos, sus tags, y su año de lancamiento
catalogoJuegos = newReviews.drop(columns=["review", "recomended"])

catalogoJuegos = catalogoJuegos.groupby("name").sample(1, replace=True)

# Agregamos la columna de año y la de tags (Estas son columnas vacías)
catalogoJuegos["release_year"] = numpy.nan
catalogoJuegos["game_tags"] = numpy.nan
catalogoJuegos["play_time"] = numpy.nan
catalogoJuegos["owners"] = numpy.nan

# Ya que tenemos un montón de juegos con reseñas
# vamos a buscar los tags y el año de lanzamiento en otro dataset
# Para eso vamos a hacer otro dataframe
datosJuego = pandas.read_csv(dataJuegosCsv, header=0, sep=",")
datosJuego = datosJuego[
    ["name", "release_date", "steamspy_tags", "median_playtime", "owners"]
].copy()
datosJuego = datosJuego.sort_values("name")

# Vamos a eliminar todos los juegos de los que no tengamos tags
for a in range(len(catalogoJuegos) - 1):
    if a == len(catalogoJuegos) - 1:
        break

    # Tomamos el nombre del juego
    nombreJuego = catalogoJuegos.iloc[a]["name"]

    # Si el juego, que tenemos en el catálogo, no está en el
    # dataset de los datos del juego, entonces:
    if nombreJuego not in datosJuego["name"].values:
        # Ahora vamos a eliminar el juego
        catalogoJuegos = catalogoJuegos.drop(
            catalogoJuegos.loc[catalogoJuegos["name"] == nombreJuego].index
        )
    # En caso de que tengamos los tags del juego
    else:
        # Guardamos la fecha de nacimiento
        fechaLanzamiento = datosJuego[(datosJuego == nombreJuego).any(axis=1)][
            "release_date"
        ].values[0]
        anoLanzamiento = fechaLanzamiento[0:4]  # Transformamos de fecha a años

        # Guardamos los tags
        tags = datosJuego[(datosJuego == nombreJuego).any(axis=1)][
            "steamspy_tags"
        ].values[0]
        # Los preprocesamos al tiro
        tags = tags.replace(";", " ")  # Seramos los tags por espacios
        tags = tags.lower()  # Cambiamos a minúsculas

        # Guardamos el tiempo promedio de juego
        tiempoJuego = datosJuego[(datosJuego == nombreJuego).any(axis=1)][
            "median_playtime"
        ].values[0]

        # Guardamos cuantos compradores tienen el juego
        adquisidores = datosJuego[(datosJuego == nombreJuego).any(axis=1)][
            "owners"
        ].values[0]

        # Guardamos las cosas dentro del dataset
        catalogoJuegos.iloc[
            a, catalogoJuegos.columns.get_loc("release_year")
        ] = anoLanzamiento
        catalogoJuegos.iloc[a, catalogoJuegos.columns.get_loc("game_tags")] = tags
        catalogoJuegos.iloc[
            a, catalogoJuegos.columns.get_loc("play_time")
        ] = tiempoJuego
        catalogoJuegos.iloc[a, catalogoJuegos.columns.get_loc("owners")] = adquisidores


# Eliminamos los valores vacío de nuevo, a veces surgen errores
catalogoJuegos = catalogoJuegos.dropna()

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalCatalogo = time.time() - inicioTiempoCatalogo
print(
    "Para hacer la base del catálogo de juegos "
    + str(datetime.timedelta(seconds=tiempoFinalCatalogo))
    + " segundos"
)

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
example = catalogoJuegos.groupby("name").sample(1, replace=True)
print(example.head(50))

# Creamos los csv con los datos.
reviewsSeiso.to_csv("baseProcesada.csv", encoding="utf-8", index=False)
catalogoJuegos.to_csv("datosJuego.csv", encoding="utf-8", index=False)
