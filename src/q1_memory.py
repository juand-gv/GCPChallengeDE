from typing import List, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import json
from utils import validate_tweet

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Procesa un archivo JSON línea por línea, analiza los tweets contenidos en él
    y devuelve una lista con las 10 fechas con más tweets y el usuario que más tweets
    publicó en cada una de esas fechas. Esta implementación está optimizada para el
    uso eficiente de memoria.

    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets. Cada línea del archivo
                         debe ser un objeto JSON que representa un tweet.

    Returns:
        List[Tuple[datetime.date, str]]: Una lista de tuplas, donde cada tupla contiene una fecha
                                         y el nombre de usuario del usuario que más tweets publicó
                                         en esa fecha. La lista está ordenada por la cantidad de tweets
                                         en orden descendente, incluyendo solo las 10 fechas principales.
    """

    # Contador para rastrear la cantidad de tweets por usuario en cada fecha
    date_user_count = defaultdict(Counter)

    # Leer el archivo línea por línea y procesar cada tweet
    with open(file_path, 'r') as file:
        for line in file:
            tweet = json.loads(line)  # Usar ujson para la carga rápida de JSON
            if not validate_tweet(tweet):  # Validar el esquema del tweet
                continue
            date = datetime.strptime(tweet["date"], "%Y-%m-%dT%H:%M:%S%z").date()  # Convertir la fecha a objeto de fecha
            user = tweet["user"]["username"]  # Obtener el nombre de usuario
            date_user_count[date][user] += 1  # Incrementar el contador para el usuario en la fecha correspondiente

    # Ordenar por cantidad de tweets y obtener las 10 fechas principales
    top_dates = sorted(date_user_count.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    
    # Obtener el usuario con más publicaciones en cada fecha
    result = [(date, user_count.most_common(1)[0][0]) for date, user_count in top_dates]
    return result


if __name__ == '__main__':
    file_path = "src/data/farmers-protest-tweets-2021-2-4.json"
    print(q1_memory(file_path))
