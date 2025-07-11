import pandas as pd
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from sentence_transformers import SentenceTransformer
import sys
from datetime import datetime

# Standardization map for field_of_research
FIELD_STANDARDIZATION = {
    "machine learning": "Computer Science",
    "neural network": "Computer Science",
    "artificial intelligence": "Computer Science",
    "data classification": "Computer Science",
    "deep learning": "Computer Science",
    "advanced neural network": "Computer Science",
    "natural language processing": "Computer Science",
    "computational physics": "Physics",
    "bioinformatics": "Biology",
    "genetics": "Biology",
    "scheduling": "Operations Research",
    "optimization": "Operations Research",
    # Add more as needed
}

def standardize_field(field):
    if not isinstance(field, str):
        return "Unknown"
    field_lower = field.lower()
    for key, value in FIELD_STANDARDIZATION.items():
        if key in field_lower:
            return value
    return field

def convert_date(date_str):
    try:
        # Try patent format first (DD-MM-YYYY)
        return datetime.strptime(str(date_str), "%d-%m-%Y").strftime("%Y-%m-%d")
    except Exception:
        try:
            # Try paper format (already ISO or year)
            if len(str(date_str)) == 4 and str(date_str).isdigit():
                return f"{date_str}-01-01"
            return str(date_str)
        except Exception:
            return "1970-01-01"

# Connect to Milvus
try:
    connections.connect(host="localhost", port="19530")
    print("Connected to Milvus")
except Exception as e:
    print(f"Failed to connect to Milvus: {e}")
    sys.exit(1)

# Define collection schema
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=50, is_primary=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="abstract", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="doc_type", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="pub_date", dtype=DataType.VARCHAR, max_length=10),
    FieldSchema(name="citation_count", dtype=DataType.INT32),
    FieldSchema(name="field_of_research", dtype=DataType.VARCHAR, max_length=100)
]
schema = CollectionSchema(fields=fields, description="Document search")

# Create or recreate collection
if utility.has_collection("documents"):
    utility.drop_collection("documents")
    print("Dropped existing 'documents' collection")
collection = Collection(name="documents", schema=schema)
print("Created 'documents' collection")
collection.create_index(
    field_name="vector",
    index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 100}}
)
print("Created index for 'vector' field")

# Load and preprocess data from correct relative path
try:
    patents = pd.read_csv("../data/raw/patents.csv", nrows=10000)
    papers = pd.read_csv("../data/raw/papers.csv", nrows=10000)
except Exception as e:
    print(f"Error loading CSV files: {e}")
    sys.exit(1)

for col in ['patent_id', 'patent_title', 'patent_abstract', 'patent_date']:
    if col not in patents.columns:
        patents[col] = ""
if 'citation_count' not in patents.columns:
    patents['citation_count'] = 0
if 'field_of_research' not in patents.columns:
    patents['field_of_research'] = "Unknown"

for col in ['title', 'abstract', 'publication_date', 'citation_count', 'field_of_research']:
    if col not in papers.columns:
        papers[col] = "" if col != 'citation_count' else 0

# Add doc_type
patents["doc_type"] = "patent"
papers["doc_type"] = "paper"

# Convert patent_date and publication_date to ISO format
patents["patent_date"] = patents["patent_date"].apply(convert_date)
papers["publication_date"] = papers["publication_date"].apply(convert_date)

# Prepare and concatenate data
patents_df = patents[['patent_id', 'patent_title', 'patent_abstract', 'doc_type', 'patent_date', 'citation_count', 'field_of_research']].rename(columns={
    'patent_id': 'id',
    'patent_title': 'title',
    'patent_abstract': 'abstract',
    'patent_date': 'pub_date'
})
papers_df = papers[['title', 'abstract', 'doc_type', 'publication_date', 'citation_count', 'field_of_research']].copy()
papers_df['id'] = [f"paper_{i}" for i in range(len(papers_df))]
papers_df = papers_df.rename(columns={'publication_date': 'pub_date'})
papers_df = papers_df[['id', 'title', 'abstract', 'doc_type', 'pub_date', 'citation_count', 'field_of_research']]

data = pd.concat([patents_df, papers_df], ignore_index=True)
data.fillna({
    "id": "", "title": "", "abstract": "", "pub_date": "1970-01-01",
    "citation_count": 0, "field_of_research": "Unknown"
}, inplace=True)

# Standardize field_of_research
data["field_of_research"] = data["field_of_research"].apply(standardize_field)

# Ensure all IDs are non-empty and unique, and convert to string
mask = (data['id'] == "") | (data['id'].isnull())
data.loc[mask, 'id'] = [f"doc_{i}" for i in data[mask].index]
data['id'] = data['id'].astype(str)
data['pub_date'] = data['pub_date'].astype(str)

# ***** NEW: Use title + abstract for embedding *****
data["embedding_text"] = data["title"].fillna('') + ". " + data["abstract"].fillna('')

# Generate embeddings and insert into Milvus
model = SentenceTransformer('all-MiniLM-L6-v2')
try:
    embeddings = model.encode(data["embedding_text"].tolist(), show_progress_bar=True)
except Exception as e:
    print(f"Error generating embeddings: {e}")
    sys.exit(1)

entities = [
    data["id"].tolist(),
    embeddings.tolist(),
    data["title"].tolist(),
    data["abstract"].tolist(),
    data["doc_type"].tolist(),
    data["pub_date"].tolist(),
    data["citation_count"].tolist(),
    data["field_of_research"].tolist()
]
collection.insert(entities)
collection.load()
print("Data inserted into Milvus")
