# Estos nos sirve para hacer los plot
import matplotlib.pyplot as plt
import seaborn

# Esto es para contar las palabras
from collections import Counter

# Importamos la biblioteca para las palabras en las fotitos
from wordcloud import WordCloud

# Importamos RE, para hacer el conteo de tags.
import re

# Importamos el numpy
import numpy

# Importamos el pandas
import pandas

# Importamos lo del test de correlación
from scipy.spatial.distance import cosine

# Importamos nltk para las stopwords
import nltk
from nltk.corpus import stopwords

# Ahora vamos a sacar las palabras indeseadas
# Descargamos las palabras que no nos sirven
nltk.download("stopwords", quiet=True)

# Metemos las palabras malas en una variable
stopwords = stopwords.words("english")

# También vamos a agregar unas palabras propias
stopwords.extend(
    (
        "really",
        "game",
        "one",
        "much",
        "amp",
        "youtube",
        "https",
        "http",
        "overall",
        "watch",
        "nbsp",
        "play",
        "i'm",
        "time",
        "games",
        "also",
        "would",
    )
)

# Buscamos los sentimientos de esta página
lexicon = pandas.read_table(
    "https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt",
    names=["termino", "sentimiento"],
)

# Vamos a hacer una función para hacer unas fotitos bien cute
def generador_palabras(data, titulo):

    # contamos las palabras más mencionadas
    masFrecuentes = Counter(data).most_common(1000)
    texto = "".join(str([x[0] for x in masFrecuentes]))

    wordcloud = WordCloud(
        width=1000,
        height=1000,
        background_color="white",
        min_font_size=5,
        collocations=False,
    ).generate(texto)

    # lo mostramos en un gráfico
    plt.figure(figsize=(6, 6), facecolor=None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(titulo, fontsize=25)
    plt.show()


# Función para asignar los sentimientos a las reviews
def asignacion_sentimientos(dataframe):
    # Hacemos un dataframe con los sentimientos
    data = pandas.merge(
        left=dataframe,
        right=lexicon,
        left_on="review",
        right_on="termino",
        how="inner",
    )

    # Borramos la columna del término
    data = data.drop(columns="termino")

    return data

# Función para calcular los sentimientos 
def calculadora_sentimientos(dataframe, genero):
    print("\nPara el género " + genero)
    puntuacionPositiva = round(100 * numpy.mean(dataframe.sentimiento > 0), 2)
    puntuacionNeutral = round(100 * numpy.mean(dataframe.sentimiento == 0), 2)
    puntuacionNegativa = round(100 * numpy.mean(dataframe.sentimiento < 0), 2)
    print("puntación positiva: " + str(puntuacionPositiva))
    print("puntación neutral: " + str(puntuacionNeutral))
    print("puntación negativa: " + str(puntuacionNegativa))
    

# Esta es la función para limpiar los textos de las reviews
def limpiar_texto(texto):
    # Pimero que todo convertimos a minúsculas
    textoLimpio = texto.lower()
    # Luego eliminamos todos los links, hay gente que pone videos en las reviews
    textoLimpio = re.sub("http\S+", " ", textoLimpio)
    # Eliminamos también los signos de puntuación.
    puntos = "[\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]"
    textoLimpio = re.sub(puntos, " ", textoLimpio)
    # Eliminamos los números
    textoLimpio = re.sub("\d+", " ", textoLimpio)
    # Eliminamos los textos en blanco que son de más de 2
    textoLimpio = re.sub("\\s+", " ", textoLimpio)
    # Tokenizamos, esto básicamente lo que hace es separar el texto en palabras
    textoLimpio = textoLimpio.split(sep=" ")
    # Eliminamos los tokens con una longitud menor a 2
    textoLimpio = [token for token in textoLimpio if len(token) > 1]
    # retornamos el texto
    return textoLimpio


# Función para eliminar las stopwords de una columna
def eliminar_stopwords(dataframe, columna):
    dataframe = dataframe[~(dataframe[columna].isin(stopwords))]
    return dataframe


# Función para mostrar gráficos de top 10 palabras de una columna
def top_10_palabras(dataframe, columna, titulo):
    plt.figure(figsize=(10, 5), facecolor=None)

    # contamos las palabras más mencionadas
    masFrecuentes = Counter(dataframe[columna]).most_common(10)

    # listas
    palabras = []
    cantidad = []

    for a in range(0, len(masFrecuentes) - 1):
        palabras.append(masFrecuentes[a][0])
        cantidad.append(masFrecuentes[a][1])

    colores = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]

    plt.bar(palabras, cantidad, color=colores, width=0.4)

    plt.title(titulo, fontsize=15)
    plt.show()


# Función para la similitud del coseno
def similitud_coseno(a, b):
    distancia = cosine(a, b)
    return 1 - distancia


# Función para hacer el gráfico de correlación
def grafico_correlacion(pivote, columna1, columna2):

    f, ax = plt.subplots(figsize=(6, 4))
    plt.rc("axes", unicode_minus=False)
    temp = pivote.dropna()
    seaborn.regplot(
        x=numpy.log(temp[columna1]),
        y=numpy.log(temp[columna2]),
        scatter_kws={"alpha": 0.05},
        ax=ax,
    )

    for i in numpy.random.choice(range(temp.shape[0]), 100):
        ax.annotate(
            text=temp.index[i],
            xy=(numpy.log(temp[columna1][i]), numpy.log(temp[columna2][i])),
            alpha=0.7,
        )

    plt.show()
