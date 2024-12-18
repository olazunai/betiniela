from dataclasses import dataclass

from src.core.domain.entities.config import Config
from src.core.domain.repositories.config_repository import ConfigRepository


@dataclass
class ConfigRetrieverService:
    config_repository: ConfigRepository

    def __call__(self) -> Config:
        return self.config_repository.get()
