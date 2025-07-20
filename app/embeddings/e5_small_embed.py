from sentence_transformers import SentenceTransformer

e5_model = SentenceTransformer("intfloat/e5-small")


def get_e5_small_embedding(text:str):
    text = f"passage: {text}"
    return e5_model.encode(text).tolist()



