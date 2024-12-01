from abc import ABC, abstractmethod


class BBDDClient(ABC):
    @classmethod
    @abstractmethod
    def init(cls, *args, **kwargs) -> "BBDDClient":
        pass

    @abstractmethod
    def close(self, *args, **kwargs) -> None:
        pass
