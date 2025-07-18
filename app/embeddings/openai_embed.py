import openai

from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


def get_openai_embedding(text:str):
    reponse = openai.Embedding.create( input=[text],
        model="text-embedding-ada-002")
    return reponse["data"][0]["embedding"]
