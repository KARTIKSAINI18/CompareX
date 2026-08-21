import time
from pymongo.operations import SearchIndexModel
from app.database.mongodb import MongoDB

COLLECTION_NAME = "product_documents"
INDEX_NAME = "vector_index"

def create_vector_index():
    database = MongoDB()
    collection = database.get_collection(COLLECTION_NAME)

    index_definition = {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 384,
                "similarity": "cosine",
            }
        ]
    }

    existing_indexes = list(collection.list_search_indexes())
    for index in existing_indexes:
        if index.get("name") == INDEX_NAME:
            print(f"Vector index '{INDEX_NAME}' already exists.")
            database.close()
            return

    model = SearchIndexModel(
        definition=index_definition,
        name=INDEX_NAME,
        type="vectorSearch",
    )

    collection.create_search_index(model)
    print(f"Created vector index: {INDEX_NAME} on {COLLECTION_NAME}")
    database.close()

if __name__ == "__main__":
    create_vector_index()
