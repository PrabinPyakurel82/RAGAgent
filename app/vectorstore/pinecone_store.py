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


def query_pinecone(query_embedding: list, top_k: int = 5):
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    results = []
    for match in response['matches']:
        score = match['score']
        metadata = match.get('metadata', {})
        results.append((
            score,
            metadata.get("chunk"),
            metadata.get("file_id"),
            match.get("id")
        ))

    return results