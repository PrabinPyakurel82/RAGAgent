from fastapi import FastAPI
from app.api import upload,agent

from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(upload.router,prefix="/api")
app.include_router(agent.router,prefix="/api")

@app.get("/")
async def root():
    return {"Message": "Hello World"}