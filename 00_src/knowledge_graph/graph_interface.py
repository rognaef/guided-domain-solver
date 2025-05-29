from abc import ABC, abstractmethod

class GraphInterface(ABC):

    @abstractmethod
    def step(self, action:int, reward:float, done:bool):
        pass