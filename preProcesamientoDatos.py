# Importamos las bibliotecas
import pandas
import numpy
import time # Para ver cuanto nos demoramos
import datetime # Para ver cuanto nos demoramos, pero lindo

# Importamos el csv con las reseñas y el de los datos
reviewsCsv = "reviews.csv"
dataJuegosCsv = "steam.csv"

# Comenzamos a contar el tiempo
inicioTiempoReviews = time.time()

# Creamos un dataframe con pandas.
reviewsDF = pandas.read_csv(reviewsCsv, header=0)

# Vamos a dejar solo 40 reviews de cada juego, porque de lo ontrario es infumable
newReviews = reviewsDF.groupby("id_game").sample(40, replace=True)

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

# Agregamos la columna de año y la de tags
newReviews["release_year"] = numpy.nan
newReviews["game_tags"] = numpy.nan


# Ya que tenemos un montón de juegos con reseñas
# vamos a buscar los tags y el año de lanzamiento en otro dataset
# Para eso vamos a hacer otro dataframe
datosJuego = pandas.read_csv(dataJuegosCsv, header=0, sep=",")
datosJuego = datosJuego[["name", "release_date", "steamspy_tags"]].copy()
datosJuego = datosJuego.sort_values("name")

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalReviews = time.time() - inicioTiempoReviews
print('Para hacer la base más pequeña y limpiarla nos demoramos ' + str(datetime.timedelta(seconds=tiempoFinalReviews))  + ' segundos')

# Comenzamos a contar cuanto nos demoramos en eliminar los juegos que no tienen los tags
inicioTiempoDatosJuego = time.time()

# Vamos a eliminar todos los juegos de los que no tengamos tags
# Para ello vamos a recorrer todas las filas del dataframe
for a in range(len(newReviews)-1):
    if a == len(newReviews)-1:
        break
    
    # Tomamos el nombre del juego
    nombreJuegoReviews = newReviews.iloc[a]["name"]
    
    # Si el juego, que tenemos en las reviews, no está en el
    # dataset que tiene los tags, entonces:
    if nombreJuegoReviews not in datosJuego["name"].values:
        # Tomamos la fila que vamos a eliminar
        eliminarJuego = newReviews.loc[newReviews["name"] == nombreJuegoReviews]
        # Guardamos los cambios
        newReviews = newReviews.drop(eliminarJuego.index)
    # En caso de que tengamos los tags del juego
    else:
        # Guardamos la fecha de lanzamiento
        fechaLanzamiento = datosJuego[(datosJuego == nombreJuegoReviews).any(axis=1)]["release_date"].values[0]
        anoLanzamiento = fechaLanzamiento[0:4] # Transformamos de fecha a años
        # Guardamos los tags
        tags = datosJuego[(datosJuego == nombreJuegoReviews).any(axis=1)]["steamspy_tags"].values[0]
        
        # Guardamos las cosas dentro del dataset        
        newReviews.iloc[a, newReviews.columns.get_loc("release_year")] = anoLanzamiento
        newReviews.iloc[a, newReviews.columns.get_loc("game_tags")] = tags
        

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalDatosJuego = time.time() - inicioTiempoDatosJuego
print('Para hacer la base más pequeña y limpiarla nos demoramos ' + str(datetime.timedelta(seconds=tiempoFinalDatosJuego)) + ' segundos')

# Ahora creamos un nuevo csv, para que podamos trabajar más rápido.
newReviews.to_csv("baseChiquita.csv", encoding="utf-8", index=False)

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
example = newReviews.groupby("name").sample(1, replace=True)
print(example.head(50))