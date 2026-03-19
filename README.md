# 🚀 Semantic Search & RAG Research Platform

## 📝 Project Overview

The **Semantic Search & RAG Research Platform** is a modern AI-powered search engine designed to index and retrieve **patents and research papers** using **vector search and Retrieval Augmented Generation (RAG)**.

The system allows users to perform **natural language queries**, retrieve semantically relevant documents, analyze research trends, and generate **AI-powered summaries of search results using a local LLM**.

This platform demonstrates how modern AI systems combine **vector databases, embeddings, and large language models** to build intelligent research tools.

---

# 🔍 System Features

### Backend
Built with **FastAPI**, integrated with:

- **Milvus** for high-performance vector search
- **Sentence Transformers** for semantic embeddings
- **Ollama (local LLM)** for RAG-based summaries
- **Scikit-learn** for clustering and trend analysis
- **MinIO** for file storage

### Frontend
Developed using:

- **Nuxt.js (Vue 3)**
- **Tailwind CSS**
- **Chart.js** for trend visualization

### AI Capabilities

The platform supports:

- 🔍 **Semantic search** using vector embeddings
- 🧠 **Document clustering** into research sub-topics
- 📈 **Trend analysis** across research areas
- 🏷️ **Filtering** by document type, citations, and date
- 🤖 **AI generated research summaries (RAG)**
- ⚡ **Fast similarity search using Milvus vector database**

---

# 🧠 RAG Pipeline

The system integrates **Retrieval Augmented Generation (RAG)** to generate summaries from retrieved research papers.

Workflow:

User Query
↓
Sentence Transformer Embedding
↓
Milvus Vector Search
↓
Top-K Relevant Documents
↓
Context Construction
↓
Local LLM (Ollama)
↓
AI Generated Research Summary


This allows the system to **combine semantic search with generative AI**, providing users with **interpretable summaries of research results**.

---

# 🛠️ Technology Stack

| Layer | Tools |
|------|------|
| Backend | FastAPI, Milvus, Sentence Transformers, Ollama |
| AI/ML | all-MiniLM-L6-v2, Scikit-learn, KMeans |
| Frontend | Nuxt.js, Vue 3, Tailwind CSS, Chart.js |
| Data | OpenAlex API, Patent datasets |
| Infrastructure | Docker, MinIO |

---

# 📁 Project Structure

```
search-platform/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── data_ingestion.py
│ │ ├── fetch_openalex.py
│ │ ├── rag_service.py
│ │ ├── reranker.py
│ │ └── models/
│ │
│ ├── data/
│ │ ├── raw/
│ │ │ ├── papers.csv
│ │ │ └── patents.csv
│ │
│ ├── requirements.txt
│ └── docker-compose.yml
│
├── frontend/
│ ├── pages/
│ ├── components/
│ ├── assets/
│ ├── package.json
│ └── nuxt.config.ts
│
├── docs/
│ └── screenshots/
│
└── README.md
```
---

# ✨ Key Features

- 🔍 **Semantic search** across patents and research papers
- 🤖 **RAG-based AI summaries** generated using a local LLM
- 🧠 **Automatic topic clustering** using KMeans
- 📈 **Trend visualization** of research areas
- 🏷️ **Advanced filtering** by:
  - document type
  - publication year
  - citation count
  - field of research
- ⚡ **High-speed vector search** using Milvus
- 🛡️ **Robust handling of sparse or missing data**

---

# ⚙️ Setup

## 1️⃣ Backend Setup

Create a virtual environment:
    cd backend
    python -m venv venv

Activate environment

Windows:
    venv\Scripts\activate

Install dependencies:
    pip install -r requirements.txt

---

## Start Milvus + MinIO

Requires Docker:
    docker-compose up -d

---

## Data Ingestion

cd app
python data_ingestion.py


This will:

- Process research datasets
- Generate embeddings
- Insert vectors into Milvus

---

## Start Backend API

uvicorn main:app --reload

Backend runs on:

    http://localhost:8000


---

# 2️⃣ Frontend Setup

    cd frontend
    npm install
    npm run dev

Open:
    http://localhost:3000

---

# 🚀 Deployment

| Component | Deployment |
|----------|------------|
| Frontend | Vercel |
| Backend | Local / Render / Railway |
| Vector DB | Docker (Milvus) |
| LLM | Ollama (local) |

Frontend demo:

    https://search-platform-five.vercel.app/


---

# 🔎 Example Queries

| Query | Doc Type | Expected Output |
|------|------|------|
| machine learning | Papers | AI/ML research papers |
| injection molding machine | Patents | Manufacturing patents |
| film | Both | Patents and papers on films |

---

# 🧩 System Design Approach

The system is designed with **two main components**:

### Backend

The backend handles:

- data ingestion
- embedding generation
- vector similarity search
- document filtering
- clustering
- RAG summarization

Milvus enables **semantic similarity search**, allowing the system to retrieve documents based on **meaning rather than keyword matching**.

The RAG pipeline uses **Ollama-hosted LLMs** to generate **context-aware summaries** of retrieved research papers.

---

### Frontend

The frontend focuses on **usability and exploration**.

Features include:

- interactive search interface
- filtering options
- document cards
- topic clustering
- research trend visualizations

Nuxt.js and Tailwind CSS were used to create a **responsive and modern UI**.

---

# ⚖️ Assumptions, Challenges, and Trade-offs

### Challenges

- Large dataset preprocessing
- Vector indexing performance
- Docker networking issues
- Handling sparse metadata in patents

### Trade-offs

- Used local LLM (Ollama) instead of cloud APIs to reduce cost
- Limited clustering complexity to maintain fast response time

### What Worked Well

- Milvus vector search performance
- RAG summaries using local LLM
- Interactive UI with Nuxt.js

### What Could Be Improved

- Public backend deployment
- Larger dataset ingestion
- advanced reranking models

---

# 🐞 Known Issues

### Mobile Search

The deployed frontend connects to a **local backend**, so mobile devices cannot access search results without deploying the backend publicly.

### Backend Deployment

Currently the backend runs locally. To enable full functionality externally, users must deploy the FastAPI server.

---

# 📚 Notes

Embedding model used:
    all-MiniLM-L6-v2


The system can easily be extended with:

- OpenAI embeddings
- larger LLMs
- advanced reranking models

---

# 🏃 Running Locally

Clone the repository and follow the **Setup** instructions.

---

# 👤 Contact

Email:
    Hrishikesh.kr.chaudhary16@gmail.com


For questions or contributions please open an issue or pull request.

---

**Happy researching! 🚀**
