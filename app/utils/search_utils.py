from langchain_core.tools import tool
from app.vectorstore.pinecone_store import query_pinecone
from app.embeddings.embedding_models import get_embedding

@tool
def search_chunks(query: str) -> str:
    """
    Perform semantic search over document chunks using Pinecone.
    """
    query_embedding = get_embedding(query)
    results = query_pinecone(query_embedding)
    return "\n".join([res[1] for res in results])