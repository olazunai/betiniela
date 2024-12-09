from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


@dataclass
class ConfigUpdaterService:
    config_repository: ConfigRepository

    def __call__(
        self,
        current_week: Optional[str] = None,
        betting_limit: Optional[datetime] = None,
        right_winner_points: Optional[int] = None,
        right_losser_points: Optional[int] = None,
    ) -> None:
        self.config_repository.update(
            current_week=Week.deserialize(current_week) if current_week else None,
            betting_limit=betting_limit,
            right_winner_points=right_winner_points,
            right_losser_points=right_losser_points,
        )
