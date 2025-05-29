from abc import ABC, abstractmethod

class GraphInterface(ABC):

    @abstractmethod
    def step(self, action:int, reward:float, done:bool) -> None:
        pass

    @abstractmethod
    def set_state(self, trajectory:list[int]) -> None:
        pass