from typing import List, Tuple
from collections import Counter
import regex
import json
from utils import validate_tweet, extract_mentions


mention_pattern = regex.compile(r'@\w+')

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo JSON línea por línea, analiza el contenido de los tweets
    y devuelve una lista con los 10 usuarios más mencionados y su respectivo conteo.
    Esta implementación está optimizada para el uso eficiente de memoria.

    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets. Cada línea del archivo
                         debe ser un objeto JSON que representa un tweet.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, donde cada tupla contiene un usuario y su conteo.
                               La lista está ordenada por conteo en orden descendente, incluyendo solo los 10 usuarios principales.
    """
    
    mention_count = Counter()

    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            if not validate_tweet(tweet):
                continue
            content = tweet.get("content", "")
            mentions = extract_mentions(content, mention_pattern)
            mention_count.update(mentions)

    return mention_count.most_common(10)


if __name__ == '__main__':
    file_path = "src/data/farmers-protest-tweets-2021-2-4.json"
    print(q3_memory(file_path))