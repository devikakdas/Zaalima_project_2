from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Falls back to defaults if not set.
    """

    # Paths
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = project_root / "data"
    model_path: Path = data_dir / "models" / "ner_model"

    # Model settings
    model_name: str = "nlpaueb/legal-bert-base-uncased"
    min_confidence: float = 0.75
    max_length: int = 512

    # OCR settings
    ocr_dpi: int = 300
    ocr_min_confidence: float = 60.0

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    max_file_size_mb: int = 50

    # ✅ Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Global settings instance
settings = Settings()
