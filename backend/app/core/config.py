from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    app_name: str = "The Lenny Growth Assistant"
    app_version: str = "1.0.0"
    debug: bool = True

    database_url: str

    llm_provider: str = "ollama"

    ollama_base_url: str
    ollama_model: str

    anthropic_api_key: str = ""

    embedding_model: str


settings = Settings()