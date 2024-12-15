from datetime import datetime

from src.core.domain.entities.match import Match
from src.core.domain.entities.user import UserRole
from src.core.domain.dtos.data import Data


def is_week_started(data: Data, week_name: str) -> bool:
    if data.user.role == UserRole.SUPERUSER:
        return data.config.started_week

    first_match: Match = sorted(
        sorted(
            data.matches_by_week.matches[week_name].matches,
            key=lambda x: x.day,
        )[0].matches,
        key=lambda x: x.match_time,
    )[0]
    return datetime.now() > datetime.combine(
        first_match.match_day, first_match.match_time
    )
