from environment.environment import SokobanEnvImpl
from knowledge_graph.knowledge_graph import KnowledgeGraph
from agents.agent_ollama import AgentOllama
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
    agent_player: AgentOllama 
        
    def set_agent_palyer(self, model:str) -> None:
        self.agent_player = AgentOllama(model,
[("system","You are a player who tries to solve a Sokoban game. Keep the reasoning short. Respond only with a single action out of ['UP', 'DOWN', 'LEFT', 'RIGHT'].",),
("human",("""Use the following results retrieved from a database to provide the next action for the Sokoban game.
Environment: {environment}
Shortest paths to place remaining boxes: {shortest_paths_to_place_remaining_boxes}
Attempted Actions: {attempted_actions}
Possible Actions: {possible_actions}
Action: """),),],
        extract_reasoning=True)
    