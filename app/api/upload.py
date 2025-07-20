from fastapi import APIRouter,File,HTTPException,UploadFile,Depends,Form
from enum import Enum

from fastapi.routing import APIRouter
import uuid
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import UploadedFile
from app.utils.file_utils import extract_text_from_pdf,extract_text_from_txt
from app.chunking.chunking_strategies import recursive_chunk,semantic_paragraph_chunk,semantic_sentence_chunk
from app.embeddings.embedding_models import get_embedding
from app.vectorstore.pinecone_store import upsert_to_pinecone

router = APIRouter()

class EmbeddingModel(str, Enum):
    sbert_all_minilm_l6_v2 = "sbert-all-MiniLM-L6-v2"
    sbert_e5_small = "sbert-e5-small"
    sbert_bge_small = "sbert-bge-small"


class ChunkingStrategy(str, Enum):
    recursive = "recursive"
    semantic_paragraph = "semantic_paragraph"
    semantic_sentence = "semantic_sentence"


chunking_map = {
    ChunkingStrategy.recursive: recursive_chunk,
    ChunkingStrategy.semantic_paragraph: semantic_paragraph_chunk,
    ChunkingStrategy.semantic_sentence: semantic_sentence_chunk,
}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      chunking_strategy: ChunkingStrategy=Form(...),
                      embedding_model: EmbeddingModel = Form(...),
                      db: Session = Depends(get_db)):
    if file.content_type not in ['application/pdf','text/plain']:
        raise HTTPException(status_code=400,detail="Only pdf and txt files are allowed")
    
    if file.content_type == 'application/pdf':
        text = extract_text_from_pdf(file)
    else:
        text = extract_text_from_txt(file)
    
    chunking_function = chunking_map[chunking_strategy]
    chunks = chunking_function(text)

    embeddings = [get_embedding(chunk,model_name=embedding_model.value) for chunk in chunks]
    
    new_file = UploadedFile(
        file_name=file.filename,
        embedding_model=embedding_model.value,
        chunking_strategy=chunking_strategy.value
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    metadata_list = [{"id": str(uuid.uuid4()), "file_id": new_file.id, "chunk": chunk} for chunk in chunks]
    upsert_to_pinecone(embeddings, metadata_list)

    return {"message": "File processed and stored", "file_id": new_file.id}



