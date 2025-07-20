from sentence_transformers import SentenceTransformer

MODELS = {
    "sbert-all-MiniLM-L6-v2": SentenceTransformer("all-MiniLM-L6-v2"),
    "sbert-e5-small": SentenceTransformer("intfloat/e5-small"),
    "sbert-bge-small": SentenceTransformer("BAAI/bge-small-en"),
}

def get_embedding(text: str, model_name="sbert-all-MiniLM-L6-v2"):
    model = MODELS[model_name]
    
    if model_name == "sbert-e5-small":
        text = f"passage: {text}"
    elif model_name == "sbert-bge-small":
        text = "Represent this sentence for retrieval: " + text
    
    return model.encode(text).tolist()
