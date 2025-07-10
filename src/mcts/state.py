from environment.environment import SokobanEnvImpl
from knowledge_graph.knowledge_graph import KnowledgeGraph
from typing import List
from typing_extensions import TypedDict

class InputState(TypedDict):
    ignore: None

class OverallState(TypedDict):
    selection_id: int
    selection_trajectory: List[int]
    reward: float
    done: bool
    sim_value: float

class OutputState(TypedDict):
    reward: float
    done: bool

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class GlobalState():
    env: SokobanEnvImpl
    kg: KnowledgeGraph