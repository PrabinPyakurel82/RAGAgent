from sentence_transformers import SentenceTransformer

bge_model = SentenceTransformer("BAAI/bge-small-en")


def get_bge_small_embedding(text:str):
    text = f"Represent this sentence for retrieval: {text}"
    return bge_model.encode(text).tolist()


