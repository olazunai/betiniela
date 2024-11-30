from abc import ABC, abstractmethod


class BBDDClient(ABC):
    @abstractmethod
    @classmethod
    def init(self, *args, **kwargs) -> "BBDDClient":
        pass

    @abstractmethod
    def close(self, *args, **kwargs) -> None:
        pass
