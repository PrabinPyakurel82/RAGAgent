from datetime import datetime
from sqlalchemy import Column,Integer,String,DateTime,func

from app.core.database import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key = True, index=True)
    file_name = Column(String)
    embedding_model = Column(String)
    chunking_strategy = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer,primary_key= True,index=True)
    full_name = Column(String)
    email = Column(String,nullable=False)
    timestamp = Column(DateTime)