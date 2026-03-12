import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "gemma3:1b"   # use the model you already downloaded


def generate_rag_summary(query, documents):
    """
    Generates AI insight summary from retrieved documents
    """

    context_docs = []

    for doc in documents[:5]:
        text = f"Title: {doc['title']}\nAbstract: {doc['abstract']}"
        context_docs.append(text)

    context = "\n\n".join(context_docs)

    prompt = f"""
You are an AI research assistant.

User question:
{query}

Relevant research documents:
{context}

Tasks:
1. Summarize the key insights
2. Identify emerging research themes
3. Highlight interesting innovations

Answer clearly using bullet points.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return result.get("response", "")