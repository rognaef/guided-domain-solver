from knowledge_graph.client_neo4j import Neo4jClient
from gym_sokoban.envs import SokobanEnv

FLOOR = 1
BOX_TARGET = 2

class KnowledgeGraph():
    client : Neo4jClient
    env: SokobanEnv

    def __init__(self, env: SokobanEnv) -> None:
        self.env = env
        self.client = Neo4jClient()
        self.client.clear_db()
        self._init_static_layer()

    def _init_static_layer(self) -> None:
        # create nodes for the floor
        id = 1
        nodes =[]
        for y in range(len(self.env.room_fixed)):
            for x in range(len(self.env.room_fixed[y])):
                tile = self.env.room_fixed[y][x]
                if tile == FLOOR or tile == BOX_TARGET:
                    tag = "Floor [{x},{y}]".format(x=x, y=y)
                    has_box_target = tile == BOX_TARGET
                    nodes.append("(:Floor {{id: {id}, x:{x}, y:{y}, has_box_target:{has_box_target}, tag:\"{tag}\"}})".format(id=id, x=x, y=y, has_box_target=has_box_target, tag=tag))
                    id+=1
        cypher = "CREATE " + ",".join(nodes) + ";"
        self.client.execute_write(cypher)

        # create relationships for neighbouring tiles
        self.client.execute_write("""
                                    MATCH (o1:Floor),(o2:Floor)
                                      WHERE (o1.x = o2.x AND o1.y = o2.y-1)
                                         OR (o1.x = o2.x AND o1.y = o2.y+1)
                                         OR (o1.x = o2.x-1 AND o1.y = o2.y)
                                         OR (o1.x = o2.x+1 AND o1.y = o2.y)
                                    CREATE (o1)-[:CAN_GO_TO]->(o2);
                                """)

    