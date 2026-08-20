from app.database.mongodb import MongoDB


COLLECTION_NAME = "products"
INDEX_NAME = "comparex_vector_index"


def check_vector_index():
    database = MongoDB()
    collection = database.get_collection(COLLECTION_NAME)

    indexes = list(
        collection.list_search_indexes()
    )

    for index in indexes:
        if index.get("name") == INDEX_NAME:
            print(f"Index: {index.get('name')}")
            print(f"Status: {index.get('status')}")

            database.close()
            return

    database.close()

    print(f"Index '{INDEX_NAME}' was not found.")


if __name__ == "__main__":
    check_vector_index()