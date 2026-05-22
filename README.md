# 🚀 AI-Powered Semantic Search & Research Analytics Platform

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

- 🔍 Semantic search using vector embeddings
- 🧠 Automatic sub-topic generation and clustering
- 📈 Research trend analytics with sub-topic heatmaps
- 🏷️ Metadata filtering (document type, citations, publication year, field)
- 🤖 Retrieval Augmented Generation (RAG) summaries using a local LLM
- ⚡ High-speed similarity search using Milvus vector database
- 🆔 Metadata enrichment with document IDs and research categorization

---

# 🧠 RAG Pipeline

The system integrates **Retrieval Augmented Generation (RAG)** to generate summaries from retrieved research papers.

System Architecture:

```text
User
↓
Text Embedding (Sentence Transformers)
↓
Milvus Vector Database
↓
Top-K Retrieval
↓
Metadata Filtering
↓
Sub-topic Discovery
↓
Trend Analytics
↓
Reranking Pipeline
↓
RAG (LLM)
↓
Frontend UI
```

Workflow:
```
User Query
↓
Text Embedding (Sentence Transformers)
↓
Vector Search (Milvus)
↓
Top-K Document Retrieval
↓
Metadata Filtering
↓
Sub-topic Discovery
↓
Trend Analytics Generation
↓
Reranking Pipeline
↓
Context Construction
↓
Filtering & Metadata Enrichment
↓
Trend Analysis (Time-based Insights)
↓
RAG (LLM-based Contextual Summary)
↓
Frontend Display (FastAPI + Nuxt.js)
```

This allows the system to **combine semantic search with generative AI**, providing users with **interpretable summaries of research results**.

---

# 🛠️ Technology Stack

| Layer | Tools |
|------|------|
| Backend | FastAPI, Milvus, Sentence Transformers, Ollama |
| AI/ML | all-MiniLM-L6-v2, Sentence Transformers, Scikit-learn |
| Frontend | Nuxt.js, Vue 3, Tailwind CSS, Chart.js |
| Data | OpenAlex API, Patent datasets |
| Infrastructure | Docker, MinIO |

---

# 📁 Project Structure

```text
search-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── data_ingestion.py
│   │   ├── fetch_openalex.py
│   │   ├── rag_service.py
│   │   ├── reranker.py
│   │
│   ├── Dockerfile
│   ├── .dockerignore
│
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── Dockerfile
│
├── docker-compose.yml
├── requirements.txt
├── docs/
└── README.md
```
---

# ✨ Key Features

- 🔍 **Semantic search** across patents and research papers
- 🤖 **RAG-based AI summaries** generated using a local LLM
- 🧠 Automatic research sub-topic generation
- 📈 Research trend visualization using sub-topic heatmaps
- 🔄 Reranking pipeline for improved retrieval quality
- 🆔 Stable document IDs with metadata enrichment
- 📊 Temporal research analytics across publication timelines
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

#### Create a virtual environment:
      cd backend
      python -m venv venv

#### Activate environment

##### Windows:
      venv\Scripts\activate

##### Install dependencies:
      pip install -r requirements.txt

---

#### Start Milvus + MinIO

### Requires Docker:
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

#### Start Backend API
    uvicorn main:app --reload

#### Backend runs on:
    http://localhost:8000
---

## 2️⃣ Frontend Setup
    cd frontend
    npm install
    npm run dev

## Open:
    http://localhost:3000
---

# 🚀 Deployment

| Component | Deployment |
|----------|------------|
| Frontend | Vercel |
| Backend | Local / Render / Railway |
| Vector DB | Docker (Milvus) |
| LLM | Ollama (local) |

## Frontend demo:
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
- metadata filtering
- reranking pipeline
- sub-topic generation
- trend analytics generation
- RAG summarization

Milvus enables **semantic similarity search**, allowing the system to retrieve documents based on **meaning rather than keyword matching**.

The RAG pipeline uses **Ollama-hosted LLMs** to generate **context-aware summaries** of retrieved research papers.

---

### Frontend

The frontend focuses on **usability and exploration**.

Features include:

- interactive semantic search
- metadata filters
- document cards
- AI generated summaries
- sub-topic trend heatmaps
- research analytics visualization

Nuxt.js and Tailwind CSS were used to create a **responsive and modern UI**.

---

# ⚖️ Assumptions, Challenges, and Trade-offs

### Challenges
- Large dataset preprocessing
- Vector indexing performance
- Docker networking issues
- Handling sparse metadata in patents
- Frontend ↔ Backend synchronization
- Vector schema evolution and metadata propagation

### Trade-offs

- Used local LLM (Ollama) instead of cloud APIs to reduce cost
- Limited clustering complexity to maintain fast response time

### What Worked Well

- Milvus vector search performance
- Local RAG summarization pipeline
- Sub-topic analytics generation
- Interactive research trend heatmap analytics
- Metadata filtering + reranking pipeline
- Interactive Nuxt.js UI

### What Could Be Improved

- Public backend deployment
- Larger dataset ingestion
- Advanced reranking models
- Research velocity analytics
- Hybrid retrieval (semantic + keyword search)

---

# 🐞 Known Issues

### Mobile Search

The deployed frontend connects to a **local backend**, so mobile devices cannot access search results without deploying the backend publicly.

### Backend Deployment

Currently the backend runs locally. To enable full functionality externally, users must deploy the FastAPI server.

---

# 📚 Notes

# Embedding model used:
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
