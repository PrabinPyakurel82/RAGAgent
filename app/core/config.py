import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    DB_URL = os.getenv("DB_URL")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

settings = Settings()