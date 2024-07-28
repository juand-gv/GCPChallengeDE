from collections import Counter
import regex
import ujson
from utils import validate_tweet, extract_emojis

def process_emoji_message(event, context):
    line = event['data'].decode('utf-8')
    tweet = ujson.loads(line)
    
    if not validate_tweet(tweet):  # Validar el esquema del tweet
        return
    
    content = tweet.get("content", "")
    emoji_pattern = regex.compile(r'\X')
    emojis = extract_emojis(content, emoji_pattern)
    
    # Guardar conteo de emojis en un bucket o base de datos
    store_emoji_count(emojis)

def store_emoji_count(emojis):
    emoji_count = Counter(emojis)
    print(emoji_count)
