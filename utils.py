import re
from xmlrpc.client import Boolean
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def preprocess_tweet(tweet, stem: Boolean):

    """
    Preprocesamiento automático de tweets

    Parametros
    ----------
    tweet: str
    stem: bool

    Salida
    ------
    tokens: list[str]
    """

    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

    tokens = tokenizer.tokenize(tweet)

    # Eliminar emojis
    def eliminarEmojis(token):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticonos
            u"\U0001F300-\U0001F5FF"  # símbolos
            u"\U0001F680-\U0001F6FF"  # transporte y mapas
            u"\U0001F1E0-\U0001F1FF"  # banderas
                            "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',token)
    
    tokens = [eliminarEmojis(token) for token in tokens]

    # Eliminar urls
    url_rx = re.compile(r'(http(s)?).+|www\..+')
    tokens = [token for token in tokens if not url_rx.match(token)]

    # Eliminar números
    numeros_rx = re.compile(r'^[0-9]+$')
    tokens = [token for token in tokens if not numeros_rx.match(token)]

    # Eliminar signos de puntuación
    tokens = [re.sub(r'^([^\w]|_)+$', '', token) for token in tokens]

    def eliminar_acentos(texto):
        texto = re.sub(r"[àáâãäå]", 'a', texto)
        texto = re.sub(r"[èéêë]", 'e', texto)
        texto = re.sub(r"[ìíîï]", 'i', texto)
        texto = re.sub(r"[òóôõö]", 'o', texto)
        texto = re.sub(r"[ùúûü]", 'u', texto)
        return texto

    # Palabras vacías sin acentuar
    stop_words_sin_acentuar = [eliminar_acentos(s_word) for s_word in stopwords.words('spanish')]

    # Eliminar palabras vacías
    tokens = [token for token in tokens if token not in stopwords.words('spanish') and token not in stop_words_sin_acentuar]

    # Eliminamos los tokens vacíos
    tokens = [token for token in tokens if token]

    if(stem == True):
        spanish_stemmer = SnowballStemmer('spanish')
        tokens = [spanish_stemmer.stem(token) for token in tokens]

    return tokens



