from typing import List, Tuple
from collections import Counter
import emoji
import regex
import json
from utils import validate_tweet

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Procesa un archivo JSON línea por línea, analiza el contenido de los tweets
    y devuelve una lista con los 10 emojis más usados y su respectivo conteo.
    Esta implementación está optimizada para el uso eficiente de memoria.

    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets. Cada línea del archivo
                         debe ser un objeto JSON que representa un tweet.

    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, donde cada tupla contiene un emoji y su conteo.
                               La lista está ordenada por conteo en orden descendente, incluyendo solo los 10 emojis principales.
    """
    emoji_count = Counter()

    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            if not validate_tweet(tweet):  # Validar el esquema del tweet
                continue
            content = tweet.get("content", "")
            
            emoji_list = []
            data = regex.findall(r'\X', content)
            for word in data:
                if any(char in emoji.EMOJI_DATA  for char in word):
                    emoji_list.append(word)

            emoji_count.update(emoji_list)

    top_emojis = emoji_count.most_common(10)
    return top_emojis


if __name__ == '__main__':
    file_path = "src/data/farmers-protest-tweets-2021-2-4.json"
    print(q2_memory(file_path))
