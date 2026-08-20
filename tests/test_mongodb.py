from app.database.mongodb import MongoDB


def test_mongodb_connection():
    database = MongoDB()

    assert database.ping() is True

    database.close()