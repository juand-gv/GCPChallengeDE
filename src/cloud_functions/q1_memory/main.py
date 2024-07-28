from datetime import datetime
from collections import defaultdict, Counter
import ujson
import gc
from utils import validate_tweet, read_file_from_gcs

def q1_memory(request):
    """
    Usage:
        {
            "bucket_name": "gcs-bucket-gtest-dev",
            "file_path": "tweets/farmers-protest-tweets-2021-2-4.json"
        }
    """

    request_json = request.get_json(silent=True)
    bucket_name = request_json['bucket_name']
    file_path = request_json['file_path']
    

    # Contador para rastrear la cantidad de tweets por usuario en cada fecha
    date_user_count = defaultdict(Counter)

    # Leer archivo desde CLoud Storage
    file_content  = read_file_from_gcs(bucket_name, file_path)
    lines = file_content.split('\n')


    # Leer el archivo línea por línea y procesar cada tweet
    for line in lines:
        if not line.strip():
            continue
        tweet = ujson.loads(line)
        if not validate_tweet(tweet):  # Validar el esquema del tweet
            continue
        date = datetime.strptime(tweet["date"], "%Y-%m-%dT%H:%M:%S%z").date()  # Convertir la fecha a objeto de fecha
        user = tweet["user"]["username"]  # Obtener el nombre de usuario
        date_user_count[date][user] += 1  # Incrementar el contador para el usuario en la fecha correspondiente


    # Liberar memoria de variables grandes
    del line
    del tweet
    gc.collect()


    # Ordenar por cantidad de tweets y obtener las 10 fechas principales
    top_dates = sorted(date_user_count.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    
    # Obtener el usuario con más publicaciones en cada fecha
    result = [(date, user_count.most_common(1)[0][0]) for date, user_count in top_dates]
    
    return {'top_dates': result}

