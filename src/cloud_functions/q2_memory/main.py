from typing import List, Tuple
from collections import Counter
import emoji
import regex
import ujson
import gc
from utils import validate_tweet, read_file_from_gcs

def q2_memory(request):
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

    emoji_count = Counter()

    # Leer archivo desde CLoud Storage
    file_content  = read_file_from_gcs(bucket_name, file_path)
    lines = file_content.split('\n')


    for line in lines:
        tweet = ujson.loads(line)
        if not validate_tweet(tweet):  # Validar el esquema del tweet
            continue
        content = tweet.get("content", "")
        
        emoji_list = []
        data = regex.findall(r'\X', content)
        for word in data:
            if any(char in emoji.EMOJI_DATA  for char in word):
                emoji_list.append(word)

        emoji_count.update(emoji_list)

    # Liberar memoria de variables grandes
    del line
    del tweet
    gc.collect()

    top_emojis = emoji_count.most_common(10)
    
    return {"top_emojis": top_emojis}