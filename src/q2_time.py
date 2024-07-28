from typing import List, Tuple
from collections import Counter
import regex
import ujson
from utils import validate_tweet, extract_emojis


emoji_pattern = regex.compile(r'\X')
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo JSON línea por línea, analiza el contenido de los tweets
    y devuelve una lista con los 10 emojis más usados y su respectivo conteo.

    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets. Cada línea del archivo
                         debe ser un objeto JSON que representa un tweet.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, donde cada tupla contiene un emoji y su conteo.
                               La lista está ordenada por conteo en orden descendente, incluyendo solo los 10 emojis principales.
    """
    
    # Leer y procesar el archivo en una sola pasada para mejorar la eficiencia
    with open(file_path, 'r') as file:
        data = [ujson.loads(line) for line in file]

    emoji_count = Counter()

    for tweet in data:
        if not validate_tweet(tweet):
            continue

        content = tweet.get("content", "")
        emojis = extract_emojis(content, emoji_pattern)
        emoji_count.update(emojis)
        
    result = emoji_count.most_common(10)
    return result


if __name__ == '__main__':
    file_path = "src/data/farmers-protest-tweets-2021-2-4.json"
    print(q2_time(file_path))

