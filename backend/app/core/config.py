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

    # Anthropic direct API key (legacy / backup)
    anthropic_api_key: str = ""
    # OpenRouter API key — get yours at https://openrouter.ai/keys
    openrouter_api_key: str = ""
    # OpenRouter model slug, e.g. "anthropic/claude-opus-4-5"
    openrouter_model: str = "anthropic/claude-opus-4-5"

    embedding_model: str


settings = Settings()