import os
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# =========================
# LOAD MODELS (LOCAL)
# =========================
print("Loading embedding...")
embed_model = SentenceTransformer("models/embedding")

print("Loading LLM...")
tokenizer = AutoTokenizer.from_pretrained("models/llm")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "models/llm",
    torch_dtype=torch.float32
)

# =========================
# VECTOR STORE
# =========================
dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []   # stores text chunks

# =========================
# PDF LOADER
# =========================
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

# =========================
# SPLIT TEXT
# =========================
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks

# =========================
# ADD DOCUMENT
# =========================
def add_document(file_path):
    text = load_pdf(file_path)
    chunks = split_text(text)

    embeddings = embed_model.encode(chunks)

    index.add(np.array(embeddings))
    documents.extend(chunks)

    return {"status": "added", "chunks": len(chunks)}

# =========================
# GENERATE ANSWER
# =========================
def generate(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_length=200,
        do_sample=False,
        num_beams=4   # better quality
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# =========================
# ASK QUESTION
# =========================
def ask_question(query):
    q_embed = embed_model.encode([query])

    D, I = index.search(np.array(q_embed), k=3)

    contexts = []
    for idx, dist in zip(I[0], D[0]):
        if dist < 1.5:   # filter weak matches
            contexts.append(documents[idx])

    context = "\n\n".join(contexts[:3])

    prompt = f"""
    You are an AI assistant.

    Answer the question clearly and in simple words using ONLY the context below.

    If the answer is not in the context, say: "I don't know".

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    answer = generate(prompt)

    return {
        "question": query,
        "context": context,
        "answer": answer
    }