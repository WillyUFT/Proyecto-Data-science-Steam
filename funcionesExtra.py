# Estos nos sirve para hacer los plot
import matplotlib.pyplot as plt

# Esto es para contar las palabras
from collections import Counter

# Importamos la biblioteca para las palabras en las fotitos
from wordcloud import WordCloud


# Vamos a hacer una función para hacer unas fotitos bien cute
def generador_palabras(data, title):

    # Keep top 1000 most frequent words
    most_freq = Counter(data).most_common(1000) 
    text = ''.join(str([x[0] for x in most_freq]))
    
    wordcloud = WordCloud(width = 800, height = 800,
                          background_color ='white',
                          min_font_size = 10,
                          collocations=False
                         ).generate(text)

    # plot the Word Cloud                      
    plt.figure(figsize = (6, 6), facecolor = None) 
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.title(title,fontsize=25)
    plt.show()
    plt.savefig(title)
