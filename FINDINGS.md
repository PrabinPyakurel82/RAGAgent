#  Evaluation Findings: Chunking Strategies and Embedding Models

## Test Files Used
- `test1.txt`: Contains a paragraph about the Eiffel Tower.
- `test2.txt`: Contains a paragraph about the Moon landing.

---

## Objective

To evaluate the performance of various **chunking strategies** and **embedding models** in a retrieval-based question answering setup using Pinecone as the vector store. Each configuration is assessed based on:

- **Retrieval Accuracy**: Cosine similarity score of the top result with the original query.
- **Latency**: Time taken (in seconds) for the end-to-end retrieval process.

---

## Evaluation Setup

###  Chunking Strategies
- `recursive`: RecursiveCharacterTextSplitter with `chunk_size=500`, `chunk_overlap=50`.
- `semantic`: Semantic splitting based on newline separators using `split_documents`.

###  Embedding Models
- `sentence-transformers/all-MiniLM-L6-v2`
- `BAAI/bge-small-en-v1.5`

---

##  Results Summary

      
| Chunking Strategy   | Embedding Model         | Avg. Score | Avg. Latency (sec) |
|---------------------|--------------------------|------------|---------------------|
| Recursive           | sbert-all-MiniLM-L6-v2   | 0.73397    | 0.351               |
| Recursive           | sbert-e5-small           | 0.88609    | 0.326               |
| Recursive           | sbert-bge-small          | **0.91385**| 0.324               |
| Semantic Paragraph  | sbert-all-MiniLM-L6-v2   | 0.73397    | 0.3265              |
| Semantic Paragraph  | sbert-e5-small           | 0.88609    | 0.361               |
| Semantic Paragraph  | sbert-bge-small          | **0.91385**| 0.3695              |
| Semantic Sentence   | sbert-all-MiniLM-L6-v2   | 0.73397    | 0.347               |
| Semantic Sentence   | sbert-e5-small           | 0.88609    | 0.327               |
| Semantic Sentence   | sbert-bge-small          | **0.91385**| 0.3275              |

---

## Insights

- **Top Accuracy**  
  - **Strategy:** Any (all equal here)  
  - **Model:** `sbert-bge-small`  
  - **Avg. Score:** `0.91385`

- **Fastest Latency**  
  - **Strategy:** Recursive  
  - **Model:** `sbert-bge-small`  
  - **Latency:** `0.324 sec`



---

## Recommendation

For high-accuracy retrieval with general-purpose text:
> **Use recursvie Chunking with `bge-small-en-v1.5`**

This setup strikes a good balance between semantic relevance and performance.

---

