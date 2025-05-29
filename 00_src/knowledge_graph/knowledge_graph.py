from knowledge_graph.client_neo4j import Neo4jClient
from knowledge_graph.graph_interface import GraphInterface
from knowledge_graph.environment_graph import EnvironmentGraph
from environment.const import *
from environment.util import *
from gym_sokoban.envs import SokobanEnv

class KnowledgeGraph():
    client : Neo4jClient
    graphs : list[GraphInterface]

    def __init__(self, env: SokobanEnv) -> None:
        self.client = Neo4jClient()
        self.client.clear_db()
        self.graphs = [EnvironmentGraph(env, self.client)]
    
    def update(self) -> None:
        for graph in self.graphs:
            graph.update()

    def get_possible_actions(self) -> list[int]:
        records, summary, keys =  self.client.read("MATCH (a:Action) RETURN a")
        return [record["a"].get("id") for record in records]