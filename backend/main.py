from fastapi import FastAPI, UploadFile, File
from backend.rag import ask_question, add_document
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    print("Start Reading")
    with open(path, "wb") as f:
        f.write(await file.read())
    print("Startr Incrept")
    result = add_document(path)
    print("finished can use prompt")
    return {"filename": file.filename, "result": result}


@app.get("/ask")
def ask(q: str):
    return ask_question(q)