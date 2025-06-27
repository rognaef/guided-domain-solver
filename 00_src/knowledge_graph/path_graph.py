from knowledge_graph.client_neo4j import Neo4jClient
from knowledge_graph.graph_interface import GraphInterface
from environment.const import *
from environment.util import *
import copy

class PathGraph(GraphInterface):
    client : Neo4jClient
    trajectory : list[int]
    max_id: int
    node_id : int
    parent_id : int
    reward : float

    root_parent_id = 0
    learning_rate = 0.1
    decay = 0.01

    def __init__(self, client: Neo4jClient) -> None:
        self.client = client
        self.trajectory = []
        self.max_id = 1
        self.node_id = 1
        self.parent_id = self.root_parent_id
        self.reward = 0
        self._init_path()

    def _init_path(self):
        cypher = "CREATE (:Path {{id: {id}, parent_id:{parent_id}, possible_actions:{possible_actions}, trajectory:{trajectory}, reward:{reward}, value:{value}, done:{done}, caption:\"{caption}\"}});".format(id=self.node_id, parent_id=self.parent_id, possible_actions=self._get_possible_actions(), trajectory=self.trajectory, reward=0, value=0, done=False, caption="Root")
        self.client.write(cypher)

    def _get_possible_actions(self) -> list[int]:
        records, summary, keys =  self.client.read("MATCH (a:Action) RETURN a")
        return [record["a"].get("id") for record in records]
    
    def step(self, action:int, reward:float, done:bool) -> None:
        # update values
        self.trajectory.append(action)
        self.parent_id = self.node_id
        self.node_id = self._create_next_id()
        self.reward+=reward

        # create new node
        caption = "Solution" if done else "Path"
        cypher = "CREATE (:Path {{id: {id}, parent_id:{parent_id}, possible_actions:{possible_actions}, trajectory:{trajectory}, reward:{reward}, value:{value}, done:{done}, caption:\"{caption}\"}});".format(id=self.node_id, parent_id=self.parent_id, possible_actions=self._get_possible_actions(), trajectory=self.trajectory, reward=self.reward, value=0, done=done, caption=caption)
        self.client.write(cypher)

        # create relationship
        caption = next(filter(lambda a:a[0]==action, ACTIONS), "")[3]
        self.client.write("""   MATCH (p1:Path),(p2:Path)
                                WHERE p1.id = {parent_id} AND p2.id = {id}
                                CREATE (p1)-[:MOVE {{id:{action}, caption:\"{caption}\"}}]->(p2);
                        """.format(parent_id=self.parent_id, id=self.node_id, action=action, caption=caption))
        
    def _create_next_id(self) -> int:
        self.max_id+=1
        return self.max_id
    
    def set_state(self, trajectory:list[int]) -> None:
        records, summary, keys =  self.client.read("MATCH (p:Path) WHERE p.trajectory={trajectory} return p".format(trajectory=trajectory))
        if len(records) != 1:
            raise Exception("Trajectory {trajectory} not visited".format(trajectory=trajectory))
        path_node = records[0]["p"]
        self.trajectory = path_node.get("trajectory")
        self.node_id = path_node.get("id")
        self.reward = path_node.get("reward")

    def backprop(self, sim_value:float):
        current_id = copy.deepcopy(self.node_id)
        value = copy.deepcopy(sim_value)

        while current_id is not self.root_parent_id:
            records, summary, keys = self.client.read("MATCH (p:Path) WHERE p.id = {id} SET p += {{value: p.value + ({learning_rate} * {value})}} return p".format(id=current_id, learning_rate=self.learning_rate, value=value))
            if len(records) != 1:
                raise Exception("Path node with id {id} not found".format(id=current_id))
            value = value * self.decay
            current_id = records[0]["p"]["parent_id"]
