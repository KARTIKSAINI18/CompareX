from pymongo import MongoClient

from app.core.config import settings


class MongoDB:
    """MongoDB connection manager for CompareX."""

    def __init__(self):
        if not settings.mongodb_uri:
            raise ValueError("MONGODB_URI is not configured.")

        self.client = MongoClient(settings.mongodb_uri)

        self.database = self.client[settings.mongodb_database]

    def get_collection(self, collection_name: str):
        return self.database[collection_name]

    def ping(self) -> bool:
        self.client.admin.command("ping")
        return True

    def close(self):
        self.client.close()