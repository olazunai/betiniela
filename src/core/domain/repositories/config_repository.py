from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from core.domain.entities.config import Config
from core.domain.value_objects.week import Week


class ConfigRepository(ABC):
    @abstractmethod
    def get(self) -> Config:
        pass

    @abstractmethod
    def update(
        self,
        current_week: Optional[Week] = None,
        betting_limit: Optional[datetime] = None,
        right_winner_points: Optional[int] = None,
        right_losser_points: Optional[int] = None,
    ) -> None:
        pass
