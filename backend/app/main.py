from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer

from pymilvus import (
    Collection,
    utility,
    connections,
    list_collections
)

from collections import defaultdict
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer

from app.rag_service import generate_rag_summary
from app.reranker import rerank_documents

import traceback
import sys


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Query(BaseModel):

    text: str
    doc_type: Optional[str] = None
    date_range: Optional[List[str]] = None
    citation_min: Optional[int] = 0
    field_of_research: Optional[str] = None


try:

    connections.connect(
        alias="default",
        host="localhost",
        port="19530"
    )

    print("MILVUS CONNECTED")

except Exception:

    traceback.print_exc()
    sys.exit(1)


print(
    "Collections:",
    utility.list_collections()
)


if not utility.has_collection(
    "documents"
):

    print(
        "documents collection missing"
    )

    sys.exit(1)


print(
    "Loading collection..."
)

collection = Collection(
    "documents"
)

collection.load()

print(
    "Collection loaded"
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_subtopic_names(
    documents,
    labels,
    n_clusters
):

    tfidf = TfidfVectorizer(
        max_features=3,
        stop_words="english"
    )

    clusters = [

        []

        for _ in range(
            n_clusters
        )

    ]

    for doc, label in zip(
        documents,
        labels
    ):

        clusters[label].append(

            doc.get(
                "abstract",
                ""
            )

        )

    names = []

    for cluster in clusters:

        if not cluster:

            names.append(
                "Miscellaneous"
            )

            continue

        try:

            tfidf.fit_transform(
                cluster
            )

            names.append(

                " ".join(
                    tfidf.get_feature_names_out()[:2]
                )

            )

        except:

            names.append(
                "Miscellaneous"
            )

    return names


@app.get("/")
def root():

    return {

        "message":
        "Backend running"

    }


@app.get("/ping")
def ping():

    print(
        "PING HIT"
    )

    return {

        "status":
        "alive"

    }


@app.get("/list_collections")
def collections_api():

    return {

        "collections":
        list_collections()

    }


@app.post("/test")
async def test():

    print(
        "TEST HIT"
    )

    return {

        "ok": True

    }


@app.post("/search")
async def search(
    query: Query
):

    try:

        print("SEARCH HIT START")
        print(query)

        print("ENCODING")

        query_vector = model.encode(
            [query.text]
        )[0]

        print("ENCODING DONE")

        expr_parts = []

        if (
            query.doc_type
            and query.doc_type != ""
            and query.doc_type != "both"
        ):

            expr_parts.append(
                f"doc_type == '{query.doc_type}'"
            )

        if query.citation_min:

            expr_parts.append(
                f"citation_count >= {query.citation_min}"
            )

        if (
            query.field_of_research
            and query.field_of_research != ""
        ):

            expr_parts.append(
                f"field_of_research like '%{query.field_of_research}%'"
            )

        expr = None

        if expr_parts:

            expr = " and ".join(
                expr_parts
            )

        print("MILVUS SEARCH")

        results = collection.search(

            data=[query_vector],

            anns_field="vector",

            param={

                "metric_type": "L2",

                "params": {

                    "nprobe": 10

                }

            },

            limit=10,

            expr=expr,

            output_fields=[

                "title",

                "abstract",

                "doc_type",

                "pub_date",

                "citation_count",

                "field_of_research",

                "sub_topic"

            ]

        )

        print("MILVUS DONE")

        documents = []

        for hit in results[0]:

            entity = hit.entity

            documents.append({

                "id":
                str(hit.id),

                "title":
                entity.get("title")
                or "Untitled",

                "abstract":
                entity.get("abstract")
                or "",

                "doc_type":
                entity.get("doc_type")
                or "unknown",

                "pub_date":
                entity.get("pub_date")
                or "Unknown",

                "citation_count":
                entity.get("citation_count")
                or 0,

                "field_of_research":
                entity.get(
                    "field_of_research"
                )
                or "",

                "sub_topic":
                entity.get(
                    "sub_topic"
                )
                or "General"

            })

        print(
            "DOCS FOUND:",
            len(documents)
        )

        documents = rerank_documents(

            query.text,
            documents

        )

        summary = generate_rag_summary(

            query.text,
            documents

        )

        trends = defaultdict(
            lambda: defaultdict(int)
        )

        for doc in documents:

            topic = doc.get(
                "sub_topic",
                "General"
            )

            year = str(

                doc.get(
                    "pub_date",
                    ""
                )

            )[:4]

            if year:

                trends[
                    topic
                ][
                    year
                ] += 1

        trends = {

            topic:

            dict(years)

            for topic, years

            in trends.items()

        }

        return {

            "documents":
            documents,

            "trends":
            trends,

            "velocity": {},

            "ai_summary":
            summary

        }

    except Exception:

        print(
            "SEARCH FAILED"
        )

        traceback.print_exc()

        raise