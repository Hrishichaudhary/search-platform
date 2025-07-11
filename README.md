# 🚀 Search Platform

## 📝 Project Overview

A **semantic search engine** for patents and academic papers, featuring sub-topic clustering and trend visualization. Designed for researchers and engineers to efficiently explore prior art and discover relevant solutions.

### Core Capabilities

- 🔍 **Semantic search** for patents and papers using natural language queries
- 🏷️ **Filter** by document type, publication date, and field of research
- 🧠 **Cluster** results into sub-topics using vector embeddings
- 📈 **Visualize trends** in research and innovation via an interactive heatmap

## 🛠️ Stack

| Layer     | Tech/Tools                                                                                   |
|-----------|---------------------------------------------------------------------------------------------|
| Backend   | FastAPI, Milvus (vector database), Sentence Transformers (`all-MiniLM-L6-v2`), Minio        |
| Frontend  | Nuxt.js (Vue 3), Tailwind CSS, Chart.js                                                     |
| Deployment| Vercel (Frontend), Docker (Milvus/Minio), Render/Railway/Local (Backend)                    |

## 📁 Project Structure

```
search-platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── data_ingestion.py
│   │   ├── fetch_openalex.py
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── query.py
│   ├── data/
│   │   ├── processed/
│   │   ├── raw/
│   │   │   ├── g_cpc_current.tsv.zip
│   │   │   ├── g_patent_abstract.tsv.zip
│   │   │   ├── g_patent.tsv.zip
│   │   │   ├── papers.csv
│   │   │   └── patents.csv
│   ├── venv/
│   ├── requirements.txt
│   ├── docker-compose.yml
├── frontend/
│   ├── assets/
│   ├── components/
│   ├── content/
│   ├── pages/
│   ├── nuxt.config.ts
│   ├── package.json
│   ├── package-lock.json
│   ├── docs/
│   │   └── screenshots/
│   │       ├── search.png
│   │       ├── results.png
│   │       └── heatmap.png
├── README.md

```


## ✨ Features

- 🔍 **Semantic search** for patents and papers
- 🏷️ **Filter** by type, date range, and field of research
- 🧠 **Clustering** results into sub-topics
- 📈 **Trend heatmap** visualization
- ⚡ **Fast, scalable vector search** with Milvus
- 🛡️ **Robust handling** of missing data

## ⚙️ Setup

### 1. Backend

#### Create and activate a virtual environment
    cd backend
    python -m venv venv

#### On Windows
    venv\Scripts\activate

#### On Mac/Linux
    source venv/bin/activate

##### Install dependencies
    pip install -r requirements.txt

#### Start Milvus and Minio (requires Docker)
    docker-compose up -d

# * Ingest data
    cd app
    python data_ingestion.py

# * Run the FastAPI server
    uvicorn main:app --reload


### 2. Frontend

    cd frontend
    npm install
    npm run dev

  * Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🚀 Deployment

- **Frontend:** [https://search-platform-five.vercel.app/](https://search-platform-five.vercel.app/) (Vercel)
- **Backend:** Run FastAPI locally or deploy on Render, Railway, or your own server
- **Milvus:** Ensure Milvus is accessible from your backend

## 🔎 Sample Queries

| Query                     | Doc Type | Expected Output                  |
|---------------------------|----------|----------------------------------|
| machine learning          | Papers   | AI/ML research papers            |
| Injection molding machine | Patents  | Relevant manufacturing patents   |
| film                      | Both     | Patents and papers on films      |

## 🧩 Approach

- **Data ingestion:** Merges and standardizes CSVs for patents and papers, using title + abstract for robust semantic search.
- **Vector search:** Milvus enables fast, scalable similarity search.
- **Clustering:** KMeans groups results into meaningful sub-topics.
- **Frontend:** Nuxt.js provides a responsive, filterable UI with trend visualization.

## ⚖️ Assumptions, Challenges, and Trade-offs

- **Assumptions:** Patent abstracts may be sparse; citation data is often missing for patents.
- **Challenges:** Ensuring semantic search works with empty patent abstracts (solved by embedding both title and abstract); troubleshooting deployment and mobile search issues.
- **Trade-offs:** Citation filtering is only meaningful for papers; it is disabled for patents to avoid user confusion. Prioritized rapid deployment and robust desktop experience; mobile search may be inconsistent due to known Nuxt Content issues.

## 🐞 Known Issues

- **Mobile Search:** Search works reliably on desktop, but may not return results on some mobile browsers due to a known Nuxt Content bug. See [Nuxt Content issues](https://github.com/nuxt/content/issues).
- **Backend Deployment:** Only the frontend is deployed; backend must be run locally for full functionality.

## 📚 Notes

- Uses open-source embedding model: `all-MiniLM-L6-v2`.
- Can be extended with other models (e.g., OpenAI `text-embedding-ada-002`).
- Designed for maintainability and real-world research utility.

## 🏃 Running Locally

* Clone the repository and organize as above.
* Follow the **Setup** instructions for backend and frontend.

**Email:** Hrishikesh.kr.chaudhary16@gmail.com  
For questions or contributions, please open an [issue](https://github.com/Hrishichaudhary/search-platform/issues) or pull request on this repository.


**Good luck, and happy searching! 🚀**

* Running Locally

* Clone the repository and organize as above.
* Follow the Setup instructions for backend and frontend.

* Contact:

* mail: Hrishikesh.kr.chaudhary16@gmail.com

* For questions or contributions, please open an issue or pull request on this repository.

Good luck, and happy searching!
