from typing import List, Tuple
from collections import Counter
import regex
import ujson
from utils import validate_tweet, extract_mentions


mention_pattern = regex.compile(r'@\w+')


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo JSON línea por línea, analiza el contenido de los tweets
    y devuelve una lista con los 10 usuarios más mencionados y su respectivo conteo.

    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets. Cada línea del archivo
                         debe ser un objeto JSON que representa un tweet.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, donde cada tupla contiene un usuario y su conteo.
                               La lista está ordenada por conteo en orden descendente, incluyendo solo los 10 usuarios principales.
    """
    
    # Leer y procesar el archivo en una sola pasada para mejorar la eficiencia
    with open(file_path, 'r') as file:
        data = [ujson.loads(line) for line in file]
    
    mention_count = Counter()    

    for tweet in data:
                
        if not validate_tweet(tweet):
            continue
        content = tweet.get("content", "")
        mentions = extract_mentions(content, mention_pattern)
        mention_count.update(mentions)

    result = mention_count.most_common(10)
    return result


if __name__ == '__main__':
    file_path = "src/data/farmers-protest-tweets-2021-2-4.json"
    print(q3_time(file_path))