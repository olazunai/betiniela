from enum import StrEnum
from attr import dataclass


class WeekPhase(StrEnum):
    GROUP = "jornada"
    PLAYOFF = "playoff"
    SEMIS = "semifinal"
    FINAL = "final"



@dataclass
class Week:
    value: int
    phase: WeekPhase

    def name(self) -> str:
        return self.phase.capitalize() + f" {self.value}" if self.value != 0 else ""
