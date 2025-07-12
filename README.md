# 🚀 Search Platform

## 📝 Project Overview

* The Search Platform is a robust, modern search engine designed to index and retrieve patents and academic papers using advanced vector search technology.

### The system features:

* **Backend**: Built with FastAPI, integrated with Milvus for high-performance vector storage and retrieval, and Minio for file storage.

* **Frontend**: Developed using Nuxt.js with Tailwind CSS for a responsive user interface, and Chart.js for interactive trend visualizations.

* **Key Features**: Supports natural language and keyword-based search, clustering of results into sub-topics, filtering by document type, date, citations, and research field, as well as heatmap-based trend exploration.

* **Deployment**: The frontend is deployed on Vercel for global accessibility, while backend services are orchestrated with Docker Compose for local development and testing.

* This platform is intended to empower researchers and innovators to efficiently explore intellectual property and research trends.

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


## ✨ Key Features:

- 🔍 **Semantic search** using state-of-the-art language models
- 🏷️ **Filter** by Kryword-type, date range, and No. of citations
- 🧠 **Clustering** of results into sub-topics for deeper exploration
- 📈 **Trend heatmap** visualizations of research and innovation trends
- ⚡ **Fast, scalable vector search** with Milvus
- 🛡️ **Robust handling** of missing or sparse data

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

#### Ingest data
    cd app
    python data_ingestion.py

#### Run the FastAPI server
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

## 🧩 Brief Approach

#### To make this search system, I broke it into two main parts: **the backend** and **the frontend**.

### Backend Development

* I set up FastAPI to handle search requests and manage all the backend connections. To get the data ready, I wrote Python scripts that pulled information from OpenAlex and patent files, cleaned up the messy and sometimes inconsistent data, and converted it into a format that could be easily searched. For storing and searching through all these records, I used Milvus, which lets the system find similar ideas based on meaning, not just matching keywords.

* To keep everything organized and reproducible, I used Docker Compose to run Milvus and Minio (for file storage) together. This setup made it easier to manage dependencies, but there were times when containers didn’t start as expected, or services like Milvus and Minio had trouble connecting—sometimes due to port conflicts or network settings in Docker. I had to double check configuration files and had to restart the containers to get everything working smoothly.

* Overall, my goal was to make sure the backend could handle large amounts of data efficiently, even if it meant spending extra time troubleshooting container issues and cleaning up raw datasets.

### Frontend Development

* For the frontend, I have used Nuxt.js to build this website that will load quickly and is simple for users to navigate. Using Tailwind CSS helped and ensure that the interface looks clean and adapts well to any screen size, making it accessible on both desktop and mobile devices. I integrated Chart.js to create interactive heatmaps that lets users to easily spot trends in the data. To organize search results into meaningful groups, I used KMeans clustering, which helps users to explore related topics without feeling overwhelmed.

* Setting up the configuration files like nuxt.config.ts and vercel.json made the build and deployment process smoother, especially when deploying to Vercel. Along the way, I had to pay special attention to how different components interacted, particularly when updating the UI based on search results or handling asynchronous data loading. There were occasional challenges with making sure visualizations rendered correctly on all devices, and I had to troubleshoot some issues with mobile search and content updates. My main focus throughout was to keep the interface user-friendly and to present complex data in a way that it will be easy to understand and explore.
  
## ⚖️ Assumptions, Challenges, and Trade-offs

- **Challenges**: Getting the data ready took longer than expected because the files were huge, and I had to tweak things to speed it up. Setting up Git failed at first with a `fatal: not a git repository` error, but I fixed it with `git init`. Sometimes Docker Compose had trouble with port conflicts when running Milvus and Minio.
- **Trade-offs**: As mentioned in the technology stack I have used Vercel for quick deployment, but it might not handle tons of users later. I made the result grouping simpler to save time, which might miss some details. I skipped extra search filters to finish on time.
- **What Worked**: The FastAPI backend teamed up with Milvus to search well, and the Nuxt.js frontend showed heatmaps nicely. The data scripts worked to process files, and Vercel got it online.
- **What Didn’t Work**: Git setup tripped me up at the start. Some heatmap parts were blank because of missing data, and Docker Compose had sync issues sometimes with Milvus and Minio.

## 🐞 Known Issues

- **Mobile Search:** The search works fine on my laptop when testing locally, but on my phone, it doesn’t show results. This might be because the backend is running on my computer (localhost), and my phone can’t connect to it over the same network. It could be a network setup problem, like the phone not finding the right address, or maybe a firewall blocking it. I think it’s not just a Nuxt Content bug but, more about how the phone and laptop talk to the local backend. I couldn’t fix it in time, but you can check the Nuxt Content issues page for related updates if needed. For more information and updates, see [Nuxt Content issues](https://github.com/nuxt/content/issues).

- **Backend Deployment & Access:** Only the frontend is deployed publicly; the backend (FastAPI + Milvus) currently runs locally.  
* To access the backend and enable full search functionality, users need to set up and run the backend on their own machine or deploy it to a public server. This involves:
  - Cloning the repository
  - Installing backend dependencies
  - Starting the backend server
  - Optionally, updating the frontend configuration to point to the correct backend URL

* Without this setup, the deployed frontend will not be able to fetch or display search results for external users.

## 📚 Notes

- Uses open-source embedding model: `all-MiniLM-L6-v2`.
- Can be extended with other models (e.g., OpenAI `text-embedding-ada-002`).
- Designed for maintainability and real-world research utility.

## 🏃 Running Locally

* Clone the repository and organize as above.
* Follow the **Setup** instructions for backend and frontend.

# Contact:

**Email:** Hrishikesh.kr.chaudhary16@gmail.com

* For questions or contributions, please open an [issue](https://github.com/Hrishichaudhary/search-platform/issues) or pull request on this repository.


**Good luck, and happy searching! 🚀**
