# 🔍 Agentic RAG System with File Upload & Interview Booking API

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
| Email         | SMTP (simple email confirmation)            |

---

## ⚙️ API Endpoints

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

### 2. `/api/start-session` — Start Session

- **Method**: `POST`

- **Sample Request**:
```bash
curl -X POST http://localhost:8000/api/start-session
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
curl -X POST http://localhost:8000/api/agent \
  -F "session_id=session_id" \
  -F "question=question"
```
  
