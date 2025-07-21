import time
import uuid
import csv

from app.embeddings.embedding_models import MODELS, get_embedding
from app.vectorstore.pinecone_store import upsert_to_pinecone, query_pinecone, index
from app.chunking.chunking_strategies import recursive_chunk, semantic_paragraph_chunk, semantic_sentence_chunk

# Embedding models to use
EMBEDDING_MODELS = [
    "sbert-all-MiniLM-L6-v2",
    "sbert-e5-small",
    "sbert-bge-small"
]

CHUNKING_STRATEGIES = {
    "recursive": recursive_chunk,
    "semantic_paragraph": semantic_paragraph_chunk,
    "semantic_sentence": semantic_sentence_chunk
}

def evaluate(file_path: str, test_query: str):
    with open(file_path, "r") as f:
        text = f.read()

    results = []

    for strategy_name, chunk_func in CHUNKING_STRATEGIES.items():
        chunks = chunk_func(text)

        for model_name in EMBEDDING_MODELS:

            embeddings = [get_embedding(chunk, model_name) for chunk in chunks]

            metadata_list = [{
                "id": str(uuid.uuid4()),
                "file_id": file_path,
                "chunk": chunk,
                "strategy": strategy_name,
                "model": model_name
            } for chunk in chunks]

            upsert_to_pinecone(embeddings, metadata_list)


            test_query_embedding = get_embedding(test_query, model_name=model_name)

            start_time = time.time()
            results_from_query = query_pinecone(test_query_embedding,file_path)
            end_time = time.time()
            latency = round(end_time - start_time, 3)

            if not results_from_query:
                print(f"[WARNING] No results for query '{test_query}' using strategy '{strategy_name}' and model '{model_name}'")
                results.append({
                    "file": file_path,
                    "strategy": strategy_name,
                    "model": model_name,
                    "latency": latency,
                    "top_chunk": None,
                    "retrieved": False
                })
                continue

            top_chunk = results_from_query[0][1]

            print(f"\n[{file_path}] Strategy: {strategy_name}, Model: {model_name}")
            print("Top Match:", top_chunk[:200], "...")
            print("Latency:", latency, "sec")

            results.append({
                "file": file_path,
                "strategy": strategy_name,
                "model": model_name,
                "latency": latency,
                "top_chunk": top_chunk,
                "retrieved": True
            })

    return results


def export_results_to_csv(results, csv_file="evaluation_results.csv"):
    fieldnames = ["file", "strategy", "model", "latency", "top_chunk", "retrieved"]

    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row_to_write = dict(row)
            if row_to_write["top_chunk"]:
                row_to_write["top_chunk"] = row_to_write["top_chunk"][:300].replace('\n', ' ')
            writer.writerow(row_to_write)



if __name__ == "__main__":
    query1 = "eiffel tower located?"
    query2 = "great wall of china?"

    all_results = []
    all_results.extend(evaluate("test_files/test1.txt", query1))
    all_results.extend(evaluate("test_files/test2.txt", query2))

    export_results_to_csv(all_results)
    print("\nEvaluation results exported to 'evaluation_results.csv'")
