from abc import ABC, abstractmethod

class GraphInterface(ABC):

    @abstractmethod
    def update(self):
        pass