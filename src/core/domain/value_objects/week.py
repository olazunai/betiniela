from enum import StrEnum
from dataclasses import dataclass


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
    
    def serialize(self) -> str:
        return self.name()
    
    @classmethod
    def deserialize(cls, obj: str) -> "Week":
        return cls(
            value=int(obj.split()[-1]),
            phase=WeekPhase(obj.split()[0]),
        )
