from dataclasses import dataclass

from uvicorn import Config
from core.domain.repositories.config_repository import ConfigRepository


@dataclass
class ConfigRetrieverService:
    config_repository: ConfigRepository

    def __call__(self) -> Config:
        return self.config_repository.get()
