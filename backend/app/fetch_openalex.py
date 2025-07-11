import requests
import pandas as pd
import os

def fetch_openalex_papers(limit=10000):
    papers = []
    url = "https://api.openalex.org/works"
    params = {
        "filter": "type:article,has_abstract:true",
        "per-page": 200,
        "cursor": "*"
    }
    count = 0
    while count < limit:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
        data = response.json()
        for work in data["results"]:
            if count >= limit:
                break
            # Reconstruct abstract text from inverted index
            abstract = work.get("abstract_inverted_index", {})
            if abstract:
                # OpenAlex provides a dict: word -> [positions]
                # We need to reconstruct the abstract in order
                word_positions = []
                for word, positions in abstract.items():
                    for pos in positions:
                        word_positions.append((pos, word))
                # Sort by position and join words
                abstract_text = " ".join(word for pos, word in sorted(word_positions))
            else:
                abstract_text = ""
            # Safe extraction of field_of_research
            field_of_research = (work.get("primary_topic") or {}).get("display_name", "Unknown")
            papers.append({
                "title": work.get("title", ""),
                "abstract": abstract_text,
                "publication_date": str(work.get("publication_year", "1970")),
                "citation_count": work.get("cited_by_count", 0),
                "field_of_research": field_of_research
            })
            count += 1
        params["cursor"] = data["meta"].get("next_cursor")
        if not params["cursor"]:
            break
        print(f"Fetched {count} papers...")
    df = pd.DataFrame(papers)
    os.makedirs("../data/raw", exist_ok=True)
    df.to_csv("../data/raw/papers.csv", index=False)
    print(f"Saved {len(df)} papers to ../data/raw/papers.csv")

if __name__ == "__main__":
    fetch_openalex_papers()
