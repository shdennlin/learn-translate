import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Base Settings. """
    BASE_DIR: Path = Path(__file__).parent.parent
    OUTPUT_DIR: Path = Path("output")
    LOG_DIR: Path = Path("log")
    TMP_DIR: Path = Path("tmp")
    DOTENV_PATH: Path = Path(".env")

    load_dotenv()
    TRANSLATION_API_KEY: str = os.getenv('TRANSLATION_API_KEY=')
    TEXT_TO_SPEECH_API_KEY: str = os.getenv('CLOUD_TRANSLATION_API_KEY')

    @validator("OUTPUT_DIR")
    def valid_output_dir(cls, v, values, **kwargs):
        """Validate OUTPUT_DIR."""
        return values["BASE_DIR"].joinpath(v)

    @validator("LOG_DIR")
    def valid_log_folder(cls, v, values, **kwargs):
        """Valid LOG_DIR."""
        return values["BASE_DIR"].joinpath(v)

    @validator("TMP_DIR")
    def valid_tmp_folder(cls, v, values, **kwargs):
        """Valid TMP_DIR."""
        return values["BASE_DIR"].joinpath(v)

    @validator("DOTENV_PATH")
    def valid_dotenv_path(cls, v, values, **kwargs):
        """Valid dotenv path."""
        return values["BASE_DIR"].joinpath(v)


def get_settings():
    """Return Settings."""
    return Settings()


class GlobalVariable:

    def __init__(self):
        self.stop_playing: bool = False
