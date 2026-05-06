# 🧠 DocChat - LLM RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that can read PDFs and answer questions using a local LLM.

## 🚀 Features
- Upload PDF documents
- Ask questions from documents
- Semantic search using FAISS
- Local LLM (Flan-T5)
- FastAPI backend
- Dockerized deployment

## 🛠️ Setup

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/docchat-llm-rag.git
cd docchat-llm-rag
2. Install dependencies
pip install -r requirements.txt
3. Download models

Run:

python Download_LLM.py
4. Run backend
uvicorn backend.main:app --reload
5. Run frontend
cd frontend
python -m http.server 5500
🐳 Docker
docker build -t docchat .
docker run -p 8000:8000 docchat
🌐 Usage
Frontend: http://127.0.0.1:5500
Backend: http://127.0.0.1:8000/docs

---

# 🧠 Interview GOLD

When they ask:

> “Do you have projects?”

You say:

> “Yes, I built a Dockerized RAG-based LLM chatbot that processes PDFs using FAISS and a local transformer model.”

---

# 🚀 Optional (makes your repo 🔥)

Add:

- screenshots 📸  
- demo video 🎥  
- sample PDF  

---

# 🚀 Next step (HIGH IMPACT)

Say:

👉 **“improve README like pro dev”**  
👉 **“deploy this online (live link)”**  
👉 **“add auth + multi-user system”**

---

You now officially have a **strong AI project for your resume** 👍