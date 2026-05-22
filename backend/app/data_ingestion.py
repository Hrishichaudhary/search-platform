import pandas as pd

from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility
)

from sentence_transformers import SentenceTransformer

import sys

from datetime import datetime


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
    "optimization": "Operations Research"

}


SUB_TOPIC_MAP = {

    "machine learning":
    "Machine Learning",

    "deep learning":
    "Deep Learning",

    "neural network":
    "Neural Networks",

    "natural language processing":
    "NLP",

    "transformer":
    "Transformers",

    "optimization":
    "Optimization",

    "classification":
    "Classification",

    "genetics":
    "Genetics",

    "bioinformatics":
    "Bioinformatics",

    "physics":
    "Physics"

}


def generate_subtopic(
    title,
    abstract
):

    text = (

        str(title)
        + " " +
        str(abstract)

    ).lower()

    for key, value in SUB_TOPIC_MAP.items():

        if key in text:

            return value

    return "General"


def standardize_field(field):

    if not isinstance(
        field,
        str
    ):

        return "Unknown"

    field_lower = field.lower()

    for key, value in FIELD_STANDARDIZATION.items():

        if key in field_lower:

            return value

    return field


def convert_date(
    date_str
):

    try:

        return datetime.strptime(
            str(date_str),
            "%d-%m-%Y"
        ).strftime(
            "%Y-%m-%d"
        )

    except:

        try:

            if (

                len(
                    str(date_str)
                ) == 4

                and

                str(
                    date_str
                ).isdigit()

            ):

                return f"{date_str}-01-01"

            return str(
                date_str
            )

        except:

            return "1970-01-01"


try:

    connections.connect(

        host="localhost",

        port="19530"

    )

    print(
        "Connected to Milvus"
    )

except Exception as e:

    print(
        f"Connection failed: {e}"
    )

    sys.exit(1)


fields = [

    FieldSchema(

        name="id",

        dtype=DataType.VARCHAR,

        max_length=50,

        is_primary=True

    ),

    FieldSchema(

        name="vector",

        dtype=DataType.FLOAT_VECTOR,

        dim=384

    ),

    FieldSchema(

        name="title",

        dtype=DataType.VARCHAR,

        max_length=512

    ),

    FieldSchema(

        name="abstract",

        dtype=DataType.VARCHAR,

        max_length=65535

    ),

    FieldSchema(

        name="doc_type",

        dtype=DataType.VARCHAR,

        max_length=20

    ),

    FieldSchema(

        name="pub_date",

        dtype=DataType.VARCHAR,

        max_length=20

    ),

    FieldSchema(

        name="citation_count",

        dtype=DataType.INT32

    ),

    FieldSchema(

        name="field_of_research",

        dtype=DataType.VARCHAR,

        max_length=100

    ),

    FieldSchema(

        name="sub_topic",

        dtype=DataType.VARCHAR,

        max_length=120

    )

]


schema = CollectionSchema(

    fields=fields,

    description="Document search"

)


if utility.has_collection(
    "documents"
):

    utility.drop_collection(
        "documents"
    )

    print(
        "Dropped old collection"
    )


collection = Collection(

    name="documents",

    schema=schema

)


print(
    "Created collection"
)


collection.create_index(

    field_name="vector",

    index_params={

        "index_type":

        "IVF_FLAT",

        "metric_type":

        "L2",

        "params": {

            "nlist": 100

        }

    }

)


print(
    "Vector index created"
)


try:

    patents = pd.read_csv(

        "data/raw/patents.csv",

        nrows=10000

    )

    papers = pd.read_csv(

        "data/raw/papers.csv",

        nrows=10000

    )

except Exception as e:

    print(
        f"CSV load failed: {e}"
    )

    sys.exit(1)


for col in [

    "patent_id",

    "patent_title",

    "patent_abstract",

    "patent_date"

]:

    if col not in patents.columns:

        patents[col] = ""


if "citation_count" not in patents:

    patents["citation_count"] = 0


if "field_of_research" not in patents:

    patents["field_of_research"] = "Unknown"


for col in [

    "title",

    "abstract",

    "publication_date",

    "citation_count",

    "field_of_research"

]:

    if col not in papers:

        papers[col] = ""


patents["doc_type"] = "patent"

papers["doc_type"] = "paper"


patents["patent_date"] = (

    patents["patent_date"]

    .apply(
        convert_date
    )

)

papers["publication_date"] = (

    papers["publication_date"]

    .apply(
        convert_date
    )

)


patents_df = (

    patents[

        [

            "patent_id",

            "patent_title",

            "patent_abstract",

            "doc_type",

            "patent_date",

            "citation_count",

            "field_of_research"

        ]

    ]

    .rename(

        columns={

            "patent_id":

            "id",

            "patent_title":

            "title",

            "patent_abstract":

            "abstract",

            "patent_date":

            "pub_date"

        }

    )

)


papers_df = papers.copy()

papers_df["id"] = [

    f"paper_{i}"

    for i in range(

        len(papers_df)

    )

]

papers_df = (

    papers_df

    .rename(

        columns={

            "publication_date":

            "pub_date"

        }

    )

)


data = pd.concat(

    [

        patents_df,

        papers_df

    ],

    ignore_index=True

)


data.fillna(

    {

        "id":"",

        "title":"",

        "abstract":"",

        "citation_count":0,

        "field_of_research":"Unknown"

    },

    inplace=True

)


data["field_of_research"] = (

    data[
        "field_of_research"
    ]

    .apply(

        standardize_field

    )

)


data["sub_topic"] = (

    data.apply(

        lambda row:

        generate_subtopic(

            row["title"],

            row["abstract"]

        ),

        axis=1

    )

)


data["embedding_text"] = (

    data["title"]

    +

    ". "

    +

    data["abstract"]

)


model = SentenceTransformer(

    "all-MiniLM-L6-v2"

)


print(
    "Generating embeddings..."
)


embeddings = model.encode(

    data[
        "embedding_text"
    ].tolist(),

    show_progress_bar=True

)


records = []


for idx, row in data.iterrows():

    records.append({

        "id":

        str(row["id"]),

        "vector":

        embeddings[idx].tolist(),

        "title":

        str(row["title"]),

        "abstract":

        str(row["abstract"]),

        "doc_type":

        str(row["doc_type"]),

        "pub_date":

        str(row["pub_date"]),

        "citation_count":

        int(
            row[
                "citation_count"
            ]
        ),

        "field_of_research":

        str(

            row[
                "field_of_research"
            ]

        ),

        "sub_topic":

        str(

            row[
                "sub_topic"
            ]

        )

    })


collection.insert(
    records
)

collection.load()


print(

    f"Inserted "

    f"{len(records)} "

    "documents"

)