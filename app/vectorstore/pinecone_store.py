from pinecone import Pinecone
from app.core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX)


def upsert_to_pinecone(embeddings,metadata_list):
    vectors = []
    for i, (embedding,metadata) in enumerate(zip(embeddings,metadata_list)):
        vectors.append({
            "id": metadata['id'],
            "values": embedding,
            "metadata": metadata

        }
        )
    index.upsert(vectors)