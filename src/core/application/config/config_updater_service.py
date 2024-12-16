from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.value_objects.week import Week


@dataclass
class ConfigUpdaterService:
    config_repository: ConfigRepository

    def __call__(
        self,
        current_week: Optional[str] = None,
        right_winner_points: Optional[int] = None,
        right_losser_points: Optional[int] = None,
        started_week: Optional[bool] = None,
    ) -> None:
        self.config_repository.update(
            current_week=Week.deserialize(current_week) if current_week else None,
            right_winner_points=right_winner_points,
            right_losser_points=right_losser_points,
            started_week=started_week,
        )
