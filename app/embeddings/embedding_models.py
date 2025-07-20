from sentence_transformers import SentenceTransformer

MODELS = {
    "minilm": SentenceTransformer("all-MiniLM-L6-v2"),
    "e5": SentenceTransformer("intfloat/e5-small"),
    "bge": SentenceTransformer("BAAI/bge-small-en"),
}

def get_embedding(text: str, model_name="minilm"):
    model = MODELS[model_name]
    
    if model_name == "e5":
        text = f"passage: {text}"
    elif model_name == "bge":
        text = "Represent this sentence for retrieval: " + text
    
    return model.encode(text).tolist()
