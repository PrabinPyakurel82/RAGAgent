from fastapi import APIRouter,File,HTTPException,UploadFile,Depends

from fastapi.routing import APIRouter
import uuid
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import UploadedFile
from app.utils.file_utils import extract_text_from_pdf,extract_text_from_txt
from app.chunking.recursive_chunking import recursive_chunk
from app.embeddings.openai_embed import get_openai_embedding
from app.embeddings.sbert_embed import get_sbert_embedding
from app.vectorstore.pinecone_store import upsert_to_pinecone

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...),db: Session = Depends(get_db)):
    if file.content_type not in ['application/pdf','text/plain']:
        raise HTTPException(status_code=400,detail="Only pdf and txt files are allowed")
    
    if file.content_type == 'application/pdf':
        text = extract_text_from_pdf(file)
    else:
        text = extract_text_from_txt(file)

    chunks = recursive_chunk(text)


    embeddings = [get_sbert_embedding(chunk) for chunk in chunks]
    
    new_file = UploadedFile(
        file_name=file.filename,
        embedding_model="sbert-all-MiniLM-L6-v2",
        chunking_strategy="recursive"
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    metadata_list = [{"id": str(uuid.uuid4()), "file_id": new_file.id, "chunk": chunk} for chunk in chunks]
    upsert_to_pinecone(embeddings, metadata_list)

    return {"message": "File processed and stored", "file_id": new_file.id}



