from dataclasses import dataclass
from typing import Optional

from core.domain.entities.match import MatchID


@dataclass
class BettingFormMatchData:
    match_id: MatchID
    winner: Optional[str] = None
    losser: Optional[str] = None
