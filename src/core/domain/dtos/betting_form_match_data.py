from dataclasses import dataclass
from typing import Optional

from core.domain.entities.match import MatchID
from core.domain.value_objects.team import Team


@dataclass
class BettingFormMatchData:
    match_id: MatchID
    winner: Optional[str] = None
    losser: Optional[str] = None
