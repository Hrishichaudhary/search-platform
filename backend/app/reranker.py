from sentence_transformers import CrossEncoder

# Load reranker model once
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query, documents):
    pairs = []

    for doc in documents:
        text = doc["title"] + " " + doc["abstract"]
        pairs.append((query, text))

    scores = reranker.predict(pairs)

    ranked_docs = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, score in ranked_docs]