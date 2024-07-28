from google.cloud import storage
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError, field_validator
import emoji

# ========================
# Leer archivo json de GCP
# ========================
def read_file_from_gcs(bucket_name: str, file_path: str) -> str:
    """
    Lee un archivo desde Google Cloud Storage.

    Args:
        bucket_name (str): El nombre del bucket de GCS.
        file_path (str): La ruta del archivo dentro del bucket.

    Returns:
        str: El contenido del archivo como una cadena.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    return blob.download_as_text()


# ========================
# Extracción de Emojis
# ========================

def extract_emojis(text, emoji_pattern):
    """
    Extrae todos los emojis de un texto dado utilizando una expresión regular,
    excluyendo los modificadores de tono de piel.

    Args:
        text (str): El texto del cual extraer emojis.

    Returns:
        List[str]: Una lista de emojis encontrados en el texto, sin los modificadores de tono de piel.
    """
    emojis = [word for word in emoji_pattern.findall(text) if any(char in emoji.EMOJI_DATA for char in word)]
    return emojis


## ========================
# Validador de esquema
# ========================
class UserModel(BaseModel):
    username: str
    id: int

class TweetModel(BaseModel):
    url: str
    date: str
    id: int
    user: UserModel

    @field_validator('date')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            raise ValueError("Incorrect date format")
        return value

def validate_tweet(tweet: dict) -> bool:
    try:
        TweetModel(**tweet)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False