from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pymilvus import Collection, utility, connections, list_collections
from sklearn.cluster import KMeans
from collections import defaultdict
from typing import List, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

from app.rag_service import generate_rag_summary
from app.reranker import rerank_documents

# --- FastAPI setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define Query model ---
class Query(BaseModel):
    text: str
    doc_type: Optional[str] = None
    date_range: Optional[List[str]] = None
    citation_min: Optional[int] = None
    field_of_research: Optional[str] = None


# --- Milvus connection ---
try:
    connections.connect(host="localhost", port="19530")
except Exception as e:
    print(f"Failed to connect to Milvus: {str(e)}", file=sys.stderr)
    sys.exit(1)

if not utility.has_collection("documents"):
    print("Collection 'documents' not found. Run data_ingestion.py first.", file=sys.stderr)
    sys.exit(1)

collection = Collection("documents")
collection.load()

# --- Embedding model ---
model = SentenceTransformer("all-MiniLM-L6-v2")


# --- Subtopic name generator ---
def generate_subtopic_names(documents, labels, n_clusters):
    tfidf = TfidfVectorizer(max_features=3, stop_words="english")
    clusters = [[] for _ in range(n_clusters)]

    for doc, label in zip(documents, labels):
        clusters[label].append(doc["abstract"] or "")

    names = []
    for cluster in clusters:
        if not cluster or all(not x for x in cluster):
            names.append("Miscellaneous")
            continue
        try:
            tfidf_matrix = tfidf.fit_transform(cluster)
            feature_names = tfidf.get_feature_names_out()
            names.append(" ".join(feature_names[:2]))
        except Exception:
            names.append("Miscellaneous")

    return names


# --- Debug endpoint ---
@app.get("/list_collections")
def list_collections_endpoint():
    try:
        collections = list_collections()
        return {"collections": collections}
    except Exception as e:
        return {"error": str(e)}


# --- Search endpoint ---
@app.post("/search")
async def search(query: Query):

    try:
        query_vector = model.encode([query.text])[0]

        expr_parts = []

        if query.doc_type and query.doc_type != "both":
            expr_parts.append(f"doc_type == '{query.doc_type}'")

        if (
            query.date_range
            and isinstance(query.date_range, list)
            and len(query.date_range) == 2
            and query.date_range[0]
            and query.date_range[1]
        ):
            expr_parts.append(
                f"pub_date >= '{query.date_range[0]}' and pub_date <= '{query.date_range[1]}'"
            )

        if query.citation_min is not None:
            try:
                citation_min = int(query.citation_min)
                if citation_min > 0:
                    expr_parts.append(f"citation_count >= {citation_min}")
            except Exception:
                pass

        if query.field_of_research:
            expr_parts.append(
                f"field_of_research like '%{query.field_of_research}%'"
            )

        expr = " and ".join(expr_parts) if expr_parts else None

        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = collection.search(
            data=[query_vector],
            anns_field="vector",
            param=search_params,
            limit=10,
            expr=expr,
            output_fields=[
                "id",
                "title",
                "abstract",
                "doc_type",
                "pub_date",
                "citation_count",
                "field_of_research",
                "vector",
            ],
        )

    except Exception as e:
        return {"documents": [], "trends": {}, "velocity": {}, "error": str(e)}

    documents = []
    vectors = []

    for hit in results[0]:

        entity = hit.entity

        doc = {
            "id": entity.get("id"),
            "title": entity.get("title") or "Untitled",
            "abstract": entity.get("abstract") or "",
            "doc_type": entity.get("doc_type"),
            "pub_date": entity.get("pub_date"),
            "citation_count": entity.get("citation_count") or 0,
            "field_of_research": entity.get("field_of_research") or "",
        }

        vector = entity.get("vector") if "vector" in entity else getattr(entity, "vector", None)

        if vector is not None:
            vectors.append(vector)
        else:
            vectors.append([0.0] * len(query_vector))

        documents.append(doc)

    if not documents:
        return {
            "documents": [],
            "trends": {},
            "velocity": {},
            "error": "No results found.",
        }

    # --- Apply CrossEncoder reranking ---
    documents = rerank_documents(query.text, documents)

    # --- Clustering ---
    sub_topics = []

    if vectors and len(vectors) > 1 and all(np.all(np.isfinite(v)) for v in vectors):

        n_clusters = min(5, len(vectors))

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)

        vectors_array = np.array(vectors)

        labels = kmeans.fit_predict(vectors_array)

        sub_topic_names = generate_subtopic_names(documents, labels, n_clusters)

        for i, doc in enumerate(documents):
            doc["sub_topic"] = sub_topic_names[labels[i]]
            sub_topics.append(sub_topic_names[labels[i]])

    else:

        for doc in documents:
            doc["sub_topic"] = "Miscellaneous"

    # --- Trend calculation ---
    trends = defaultdict(lambda: defaultdict(int))

    for doc in documents:
        year = str(doc["pub_date"])[:4]
        trends[doc["sub_topic"]][year] += 1

    velocity = {}

    for topic in trends:

        topic_years = []

        years_counts = {}

        for date_str, count in trends[topic].items():

            try:
                year = str(date_str)[:4]

                if year.isdigit():
                    years_counts[year] = years_counts.get(year, 0) + count

            except Exception:
                continue

        for year in sorted(years_counts):

            count = years_counts[year]

            prev_year = str(int(year) - 1)

            prev_count = years_counts.get(prev_year, 0)

            topic_years.append((year, count, count - prev_count))

        velocity[topic] = topic_years

    # --- RAG summary ---
    rag_summary = generate_rag_summary(query.text, documents)

    return {
        "documents": documents,
        "trends": dict(trends),
        "velocity": velocity,
        "ai_summary": rag_summary,
    }