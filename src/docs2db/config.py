"""Settings for the project."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base directory for storing content
    content_base_dir: str = "docs2db_content"

    # Docling Settings
    docling_pipeline: str = "standard"  # "standard" or "vlm"
    docling_model: str | None = None
    docling_device: str = "auto"  # "auto", "cpu", "cuda", "mps"
    docling_batch_size: int = 3
    docling_workers: int | None = None

    # Chunking Settings
    chunking_pattern: str = "**/source.json"
    chunking_workers: int | None = None

    # LLM Provider Settings for contextual chunking
    llm_skip_context: bool = False
    llm_provider: str = (
        "openai"  # Provider choice: "openai", "watsonx", "openrouter", "mistral"
    )
    llm_context_model: str = "qwen2.5:7b-instruct"
    llm_openai_url: str = "http://localhost:11434"  # Default to Ollama
    llm_watsonx_url: str | None = None
    llm_openrouter_url: str = "https://openrouter.ai/api"
    llm_mistral_url: str = "https://api.mistral.ai/v1"
    llm_context_limit_override: int | None = None
    llm_max_retries: int = 5
    llm_retry_min_wait: float = 1.0
    llm_retry_max_wait: float = 60.0
    llm_rate_limit: int = 0  # Requests per minute (0 = unlimited)

    # WatsonX credentials (only needed if using WatsonX provider)
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""

    # OpenRouter credentials (only needed if using OpenRouter provider)
    openrouter_api_key: str = ""

    # Mistral credentials (only needed if using Mistral provider)
    mistral_api_key: str = ""


    # Embedding Settings
    embedding_model: str = "ibm-granite/granite-embedding-30m-english"
    embedding_pattern: str = "**/chunks.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
