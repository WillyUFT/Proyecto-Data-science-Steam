# Importamos pandas para leer el csv
import pandas

pandas.options.mode.chained_assignment = None

# Importamaos el tiempo
import time
import datetime

# Importamos algunas funciones
import funcionesExtra as funEx

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


# Vamos a importar las bases
baseProcesadaCsv = "baseProcesada.csv"
baseCatalogoJuegosCsv = "datosJuego.csv"

# Creamos un dataframe con pandas
baseProcesada = pandas.read_csv(baseProcesadaCsv, header=0)
baseCatalogoJuegos = pandas.read_csv(baseCatalogoJuegosCsv, header=0)

# Comenzamos a tomar el tiempo
tiempoInicialJuegosAccion = time.time()

# Así se hacen los filtros
# Hacemos un data frame donde tengamos todos los juegos de acción que estén en el catálogo
dataFrameJuegosAccion = baseCatalogoJuegos.loc[
    baseCatalogoJuegos["game_tags"].str.contains("action", case=False)
]

# Hacemos una lista con el título de los juegos de acción
listaJuegosAccion = dataFrameJuegosAccion["name"].values.tolist()

# Luego buscamos todas las reviews de esos juegos
reviewsJuegosAccion = baseProcesada[baseProcesada["name"].isin(listaJuegosAccion)]

# Hacemos el filtro para los recomendados y los no recomendados
reviewsJuegosAccionBuenos = reviewsJuegosAccion[reviewsJuegosAccion["recomended"] == 1]
reviewsJuegosAccionMalos = reviewsJuegosAccion[reviewsJuegosAccion["recomended"] == -1]


# Hacemos esa fotito de las palabras, las más frecuentes de los juegos de acción
funEx.generador_palabras(
    reviewsJuegosAccionBuenos["review"],
    "Palabras más usadas en las reviews de juegos de acción recomendados por los usuarios",
)

# Hacemos el gráfico aun más exacto
funEx.top_10_palabras(
    reviewsJuegosAccionBuenos,
    "review",
    "Top 10 palabras más utilizadas para juegos de acción recomendados por los usuarios",
)

# Hacemos esa fotito de las palabras, las más frecuentes de los juegos de acción
funEx.generador_palabras(
    reviewsJuegosAccionMalos["review"],
    "Palabras más usadas en las reviews de juegos de acción no recomendados por los usuarios",
)

# Hacemos el gráfico aun más exacto
funEx.top_10_palabras(
    reviewsJuegosAccionMalos,
    "review",
    "Top 10 palabras más utilizadas para juegos de acción no recomendados por los usuarios",
)

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalJuegosAccion = time.time() - tiempoInicialJuegosAccion
print(
    "Para buscar todos los juegos de acción nos demoramos "
    + str(datetime.timedelta(seconds=tiempoFinalJuegosAccion))
    + " segundos"
)

# Comenzamos a tomar el tiempo
tiempoInicialJuegosIndie = time.time()

# Si nosotros quisieramos meter un juego a steam, tendría que ser indie, no tenemos plata, así que revisemos
# los juegos indies igual.

# Hacemos un data frame donde tengamos todos los juegos indie que estén en el catálogo
dataFrameJuegosIndie = baseCatalogoJuegos.loc[
    baseCatalogoJuegos["game_tags"].str.contains("indie", case=False)
]

# Hacemos una lista con el título de los juegos indie
listaJuegosIndie = dataFrameJuegosIndie["name"].values.tolist()

# Luego buscamos todas las reviews de esos juegos
reviewsJuegosIndie = baseProcesada[baseProcesada["name"].isin(listaJuegosIndie)]

# Hacemos el filtro para los recomendados y los no recomendados
reviewsJuegosIndieBuenos = reviewsJuegosIndie[reviewsJuegosIndie["recomended"] == 1]
reviewsJuegosIndieMalos = reviewsJuegosIndie[reviewsJuegosIndie["recomended"] == -1]

# Hacemos esa fotito de las palabras, las más frecuentes de los juegos de acción
funEx.generador_palabras(
    reviewsJuegosIndieBuenos["review"],
    "Palabras más usadas en las reviews de juegos indie recomendados por los usuarios",
)

# Hacemos el gráfico aun más exacto
funEx.top_10_palabras(
    reviewsJuegosIndieBuenos,
    "review",
    "Top 10 palabras más utilizadas para juegos indie recomendados por los usuarios",
)

# Hacemos esa fotito de las palabras, las más frecuentes de los juegos indie
funEx.generador_palabras(
    reviewsJuegosIndieMalos["review"],
    "Palabras más usadas en las reviews de juegos indie no recomendados por los usuarios",
)

# Hacemos el gráfico aun más exacto
funEx.top_10_palabras(
    reviewsJuegosIndieMalos,
    "review",
    "Top 10 palabras más utilizadas para juegos indie no recomendados por los usuarios",
)

# Vamos a ver cuanto tiempo nos demoramos
tiempoFinalJuegosIndie = time.time() - tiempoInicialJuegosIndie
print(
    "Para buscar todos los juegos indie nos demoramos "
    + str(datetime.timedelta(seconds=tiempoFinalJuegosIndie))
    + " segundos"
)

# Comenzamos a tomar el tiempo
tiempoInicialCorrelacionIndieAccion = time.time()

# Vamos a hacer la correlación entre juegos de Acción buenos y juegos indie buenos
# Para ello, vamos a analizar las palabras que se ocupan en las reviews y su frecuencia

# Agregamos una columna de acción e indie
reviewsJuegosAccionBuenos["genero"] = "accion"
reviewsJuegosIndieBuenos["genero"] = "indie"

reviewsJuegosAccionMalos["genero"] = "accion"
reviewsJuegosIndieMalos["genero"] = "indie"

# Juntamos las reviews
reviewJuegosAccionIndieBuenos = pandas.concat(
    [reviewsJuegosAccionBuenos, reviewsJuegosIndieBuenos]
)

# Hacemos el pivote para sacar la correlación
reviewsAccionIndieBuenosPivote = (
    reviewJuegosAccionIndieBuenos.groupby(["genero", "review"])["review"]
    .agg(["count"])
    .reset_index()
    .pivot(index="review", columns="genero", values="count")
)

# Vemos la correlación en una tabla
tablaCorrelacionJuegosBuenos = reviewsAccionIndieBuenosPivote.corr(
    method=funEx.similitud_coseno
)
print("")
print(tablaCorrelacionJuegosBuenos)

# Le quitamos los nombres a las columnas
reviewsAccionIndieBuenosPivote.columns.name = None

# Hacemos el gráfico de correlación
funEx.grafico_correlacion(reviewsAccionIndieBuenosPivote, "accion", "indie")

# Ahora vamos a hacer el análisis de sentimientos, con él podremos sacar alguna conclusión
AccionIndieBuenosSentimientos = funEx.asignacion_sentimientos(
    reviewJuegosAccionIndieBuenos
)

# Hacemos una edición en el data frame para verlo mejor
AccionIndieBuenosSentimientos = (
    AccionIndieBuenosSentimientos[["name", "recomended", "sentimiento"]]
    .groupby(["name"])
    .sum()
    .reset_index()
)

# Calculamos el total de sentimientos
funEx.calculadora_sentimientos(AccionIndieBuenosSentimientos, "accion")
funEx.calculadora_sentimientos(AccionIndieBuenosSentimientos, "indie")

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
example = AccionIndieBuenosSentimientos.groupby("name").sample(1, replace=True)
example = example.sort_values(by=["sentimiento"], ascending=False)
print(example.head(10))


# Ahora haremos los mismo para los negativos
# Juntamos las reviews
reviewJuegosAccionIndieMalos = pandas.concat(
    [reviewsJuegosAccionMalos, reviewsJuegosIndieMalos]
)

# Hacemos el pivote para sacar la correlación
reviewsAccionIndieMalosPivote = (
    reviewJuegosAccionIndieMalos.groupby(["genero", "review"])["review"]
    .agg(["count"])
    .reset_index()
    .pivot(index="review", columns="genero", values="count")
)

# Vemos la correlación en una tabla
tablaCorrelacionJuegosMalos = reviewsAccionIndieMalosPivote.corr(
    method=funEx.similitud_coseno
)
print("")
print(tablaCorrelacionJuegosMalos)

# Le quitamos los nombres a las columnas
reviewsAccionIndieMalosPivote.columns.name = None

# Hacemos el gráfico de correlación
funEx.grafico_correlacion(reviewsAccionIndieMalosPivote, "accion", "indie")

# Ahora vamos a hacer el análisis de sentimientos, con él podremos sacar alguna conclusión
AccionIndieMalosSentimientos = funEx.asignacion_sentimientos(
    reviewJuegosAccionIndieMalos
)

# Hacemos una edición en el data frame para verlo mejor
AccionIndieMalosSentimientos = (
    AccionIndieMalosSentimientos[["name", "recomended", "sentimiento"]]
    .groupby(["name"])
    .sum()
    .reset_index()
)

# Vamos a mostrar 50 reviews de juegos distintos
print("\n\n\nEJEMPLO DEL DATA FRAME\n\n\n")
example = AccionIndieMalosSentimientos.groupby("name").sample(1, replace=True)
example = example.sort_values(by=["sentimiento"], ascending=True)
print(example.head(10))

# Calculamos el total de sentimientos
funEx.calculadora_sentimientos(AccionIndieMalosSentimientos, "accion")
funEx.calculadora_sentimientos(AccionIndieMalosSentimientos, "indie")
