# Agentic RAG System

##  Overview

This backend system provides:

1. **File Upload & Vectorization API**  
   Upload `.pdf` or `.txt` files, extract and chunk text using various strategies, generate embeddings using multiple models, and store them in a vector database (Pinecone). Metadata is saved in a relational database (PostgreSQL).

2. **Agentic RAG API**  
   A conversational agent powered by LangChain, supporting memory via Redis. This agent answers user queries using chunk-retrieval tools. It also supports interview booking and email confirmation.

---

##  Tech Stack

| Layer         | Tools Used                                 |
|---------------|---------------------------------------------|
| Framework     | FastAPI                                     |
| Embeddings    | Sentence Trnasformers
| Vector Store  | Pinecone                                    |
| Chunking      | Recursive, Semantic (Sentence/Paragraph)    |
| Database      | PostgreSQL (metadata), Redis (memory)       |
| Agent         | LangChain Agent (zero-shot-react)           |
---

## API Endpoints

### 1. `/api/upload` — File Upload and Vectorization

- **Method**: `POST`
- **Input**: `.pdf` or `.txt` file, chunking method, embedding model
- **Process**:
  - Extracts text
  - Chunks using specified method (`recursive`, `semantic_paragraph`, `semantic_sentence`)
  - Generates embeddings using specified model 
  - Saves embeddings to Pinecone
  - Logs metadata to PostgreSQL

- **Sample Request**:
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf" \
  -F "chunking_strategy=semantic_sentence" \
  -F "embedding_model=e5-small"
```
- **Sample Response**
```json
  {
  "message": "File processed and stored",
  "file_id": 8
  }
```

### 2. `/api/start-session` — Start Session

- **Method**: `POST`

- **Sample Request**:
```bash
curl -X POST http://localhost:8000/api/start-session
```
- **Sample Response**
```json
   {
  "session_id": "f5396391-4022-4766-8de5-49be13fc8ad3"
   }
```

### 3. `/api/agent` — Retrieval

- **Method**: `POST`
- **Input**: `session_id` and `query`
- **Process**:
  - Converts query itno embedding
  - Search the vectore_store for related chunks
  - Answers based on chunks retrieved 
  - Saves the session into redis

- **Sample Request**:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/agent/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "session_id": "f5396391-4022-4766-8de5-49be13fc8ad3",
  "question": "Is AI replacing humans?"
}'
```
- **Sample Response**
```json
{
  "answer": {
    "input": "Is AI replacing humans?",
    "chat_history": [
      {
        "content": "What is AI?",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": null,
        "example": false
      },
      {
        "content": "Generally speaking, Artificial Intelligence is a computing concept that helps a machine think and solve complex problems as humans do with their intelligence. It involves a machine working on a problem, making mistakes, and learning from them in a self-correcting manner as part of its self-improvement.",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "ai",
        "name": null,
        "id": null,
        "example": false,
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": null
      }
    ],
    "output": "AI is replacing some jobs through automation, but it is also creating new jobs and redefining existing ones, leading to a complex and evolving job market."
  }
}
```
  
