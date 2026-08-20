from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "CompareX"
    app_version: str = "0.1.0"
    debug: bool = True

    # MongoDB
    mongodb_uri: str = ""
    mongodb_database: str = "comparex"

    # LLM
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""

    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()