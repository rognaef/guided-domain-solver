from knowledge_graph.client_neo4j import Neo4jClient
from knowledge_graph.graph_interface import GraphInterface
from environment.const import *
from environment.util import *

class PathGraph(GraphInterface):
    client : Neo4jClient
    trajectory : list[int]
    node_id : int

    def __init__(self, client: Neo4jClient) -> None:
        self.client = client
        self.trajectory = []
        self.node_id = 1
        self._init_path()

    def _init_path(self):
        cypher = "CREATE (:Path {{id: {id}, trajectory:{trajectory}, reward:{reward}, done:{done}, caption:\"{caption}\"}});".format(id=self.node_id, trajectory=self.trajectory, reward=0, done=False, caption="Root")
        self.client.write(cypher)
    
    def step(self, action:int, reward:float, done:bool) -> None:
        # update values
        self.trajectory.append(action)
        self.node_id+=1

        # create new node
        caption = "Solution" if done else "Path"
        cypher = "CREATE (:Path {{id: {id}, trajectory:{trajectory}, reward:{reward}, done:{done}, caption:\"{caption}\"}});".format(id=self.node_id, trajectory=self.trajectory, reward=reward, done=done, caption=caption)
        self.client.write(cypher)

        # create relationship
        action = next(filter(lambda a:a[0]==action, ACTIONS), "")[3]
        self.client.write("""   MATCH (p1:Path),(p2:Path)
                                WHERE p1.id = {last_id} AND p2.id = {id}
                                CREATE (p1)-[:MOVE {{action: \"{action}\"}}]->(p2);
                        """.format(last_id=self.node_id-1, id=self.node_id, action=action))