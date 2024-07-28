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
    return blob.open("rt")


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


# ========================
# Validador de esquema
# ========================

class DescriptionUrlModel(BaseModel):
    """
    Modelo que representa una URL de descripción dentro de un tweet.

    Attributes:
        text (str): El texto de la URL.
        indices (List[int]): Lista de índices que indican la posición de la URL en el texto del tweet.
    """

    text: str
    indices: List[int]

class UserModel(BaseModel):
    """
    Modelo que representa un usuario de Twitter.

    Attributes:
        username (str): El nombre de usuario de Twitter.
        displayname (Optional[str]): El nombre de pantalla del usuario.
        id (int): El ID del usuario.
        description (Optional[str]): La descripción del usuario.
        rawDescription (Optional[str]): La descripción cruda del usuario.
        descriptionUrls (Optional[List[DescriptionUrlModel]]): Lista de URLs en la descripción del usuario.
        verified (Optional[bool]): Indicador de si el usuario está verificado.
        created (Optional[str]): La fecha de creación de la cuenta del usuario.
        followersCount (Optional[int]): La cantidad de seguidores del usuario.
        friendsCount (Optional[int]): La cantidad de amigos del usuario.
        statusesCount (Optional[int]): La cantidad de estados del usuario.
        favouritesCount (Optional[int]): La cantidad de favoritos del usuario.
        listedCount (Optional[int]): La cantidad de listas en las que aparece el usuario.
        mediaCount (Optional[int]): La cantidad de medios publicados por el usuario.
        location (Optional[str]): La ubicación del usuario.
        protected (Optional[bool]): Indicador de si la cuenta del usuario está protegida.
        linkUrl (Optional[str]): URL del perfil del usuario.
        linkTcourl (Optional[str]): URL acortada del perfil del usuario.
        profileImageUrl (Optional[str]): URL de la imagen del perfil del usuario.
        profileBannerUrl (Optional[str]): URL del banner del perfil del usuario.
        url (Optional[str]): URL del usuario.
    """

    username: str
    displayname: Optional[str] = None
    id: int
    description: Optional[str] = None
    rawDescription: Optional[str] = None
    descriptionUrls: Optional[List[DescriptionUrlModel]] = None
    verified: Optional[bool] = None
    created: Optional[str] = None
    followersCount: Optional[int] = None
    friendsCount: Optional[int] = None
    statusesCount: Optional[int] = None
    favouritesCount: Optional[int] = None
    listedCount: Optional[int] = None
    mediaCount: Optional[int] = None
    location: Optional[str] = None
    protected: Optional[bool] = None
    linkUrl: Optional[str] = None
    linkTcourl: Optional[str] = None
    profileImageUrl: Optional[str] = None
    profileBannerUrl: Optional[str] = None
    url: Optional[str] = None

class TweetModel(BaseModel):
    """
    Modelo que representa un tweet.

    Attributes:
        url (str): URL del tweet.
        date (str): Fecha y hora del tweet en formato ISO 8601.
        content (Optional[str]): Contenido del tweet.
        renderedContent (Optional[str]): Contenido renderizado del tweet.
        id (int): ID del tweet.
        user (UserModel): Información del usuario que publicó el tweet.
        outlinks (Optional[List[str]]): Lista de URLs externas incluidas en el tweet.
        tcooutlinks (Optional[List[str]]): Lista de URLs acortadas incluidas en el tweet.
        replyCount (Optional[int]): Cantidad de respuestas al tweet.
        retweetCount (Optional[int]): Cantidad de retweets del tweet.
        likeCount (Optional[int]): Cantidad de "me gusta" del tweet.
        quoteCount (Optional[int]): Cantidad de citas del tweet.
        conversationId (Optional[int]): ID de la conversación a la que pertenece el tweet.
        lang (Optional[str]): Idioma del tweet.
        source (Optional[str]): Fuente desde donde se publicó el tweet.
        sourceUrl (Optional[str]): URL de la fuente desde donde se publicó el tweet.
        sourceLabel (Optional[str]): Etiqueta de la fuente desde donde se publicó el tweet.
        media (Optional[List[dict]]): Lista de medios adjuntos al tweet.
        retweetedTweet (Optional[dict]): Información del tweet retuiteado, si aplica.
        quotedTweet (Optional[dict]): Información del tweet citado, si aplica.
        mentionedUsers (Optional[List[UserModel]]): Lista de usuarios mencionados en el tweet.
    """

    url: str
    date: str
    content: Optional[str] = None
    renderedContent: Optional[str] = None
    id: int
    user: UserModel
    outlinks: Optional[List[str]] = None
    tcooutlinks: Optional[List[str]] = None
    replyCount: Optional[int] = None
    retweetCount: Optional[int] = None
    likeCount: Optional[int] = None
    quoteCount: Optional[int] = None
    conversationId: Optional[int] = None
    lang: Optional[str] = None
    source: Optional[str] = None
    sourceUrl: Optional[str] = None
    sourceLabel: Optional[str] = None
    media: Optional[List[dict]] = None
    retweetedTweet: Optional[dict] = None
    quotedTweet: Optional[dict] = None
    mentionedUsers: Optional[List[UserModel]] = None

    @field_validator('date')
    def validate_date_format(cls, value):
        """
        Valida que la fecha esté en el formato ISO 8601 correcto.

        Args:
            value (str): La fecha en formato de cadena.

        Returns:
            str: La fecha validada.

        Raises:
            ValueError: Si la fecha no está en el formato correcto.
        """

        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            raise ValueError("Incorrect date format")
        return value

def validate_tweet(tweet: dict) -> bool:
    """
    Valida que un diccionario de tweet cumpla con el esquema definido por TweetModel.

    Args:
        tweet (dict): Diccionario que representa el tweet.

    Returns:
        bool: True si el tweet es válido, False si no lo es.

    Raises:
        ValidationError: Si el tweet no cumple con el esquema.
    """
    
    try:
        TweetModel(**tweet)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False