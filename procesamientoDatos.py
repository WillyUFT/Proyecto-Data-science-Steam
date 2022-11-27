# Importamos pandas para leer el csv
import pandas

# Importamos RE, para hacer el conteo de tags.
import re

# Importamaos el tiempo
import time
import datetime

# Importamos algunas funciones
import funcionesExtra as funEx

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


# Vamos a importar las bases
basePreprocesadaCsv = "basePreProcesada.csv"
baseCatalogoJuegosCsv = "datosJuego.csv"

# Creamos un dataframe con pandas
baseProcesada = pandas.read_csv(basePreprocesadaCsv, header=0)
baseCatalogoJuegos = pandas.read_csv(baseCatalogoJuegosCsv, header=0)

# Comenzamos a tomar el tiempo
tiempoInicialBaseProcesada = time.time()

# Así se hacen los filtros
# Hacemos un data frame donde tengamos todos los juegos de acción que estén en el catálogo
dataFrameJuegosAccion = baseCatalogoJuegos.loc[
    baseCatalogoJuegos["game_tags"].str.contains("action", case=False)
]

# Hacemos una lista con el título de los juegos de acción
listaJuegosAccion = dataFrameJuegosAccion["name"].values.tolist()

# Luego buscamos todas las reviews de esos juegos
reviewsJuegosAccion = baseProcesada[baseProcesada["name"].isin(listaJuegosAccion)]

# Hacemos esa fotito de las palabras
funEx.generador_palabras(
    reviewsJuegosAccion["review"],
    "Palabras más usadas en las reviews de juegos de acción",
)