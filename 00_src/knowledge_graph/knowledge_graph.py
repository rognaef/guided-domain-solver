from knowledge_graph.client_neo4j import Neo4jClient
from gym_sokoban.envs import SokobanEnv

FLOOR = 1
BOX_TARGET = 2
BOX_ON_TARGET = 3
BOX = 4
PLAYER = 5

class KnowledgeGraph():
    client : Neo4jClient
    env: SokobanEnv

    def __init__(self, env: SokobanEnv) -> None:
        self.env = env
        self.client = Neo4jClient()
        self.client.clear_db()
        self._init_static_layer()
        self._init_dynamic_layer()

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
    
    def _init_dynamic_layer(self) -> None:
        # create nodes for the boxes and player
        player_id = 1
        box_id = 1
        nodes =[]
        for y in range(len(self.env.room_state)):
            for x in range(len(self.env.room_state[y])):
                tile = self.env.room_state[y][x]
                if tile == BOX_ON_TARGET or tile == BOX:
                    tag = "Box"
                    is_on_target = tile == BOX_ON_TARGET
                    nodes.append("(:Box {{id: {id}, x:{x}, y:{y}, is_on_target:{is_on_target}, tag:\"{tag}\"}})".format(id=box_id, x=x, y=y, is_on_target=is_on_target, tag=tag))
                    box_id+=1
                elif tile == PLAYER:
                    tag = "Player"
                    nodes.append("(:Player {{id: {id}, x:{x}, y:{y}, tag:\"{tag}\"}})".format(id=player_id, x=x, y=y, tag=tag))
                    player_id+=1
        cypher = "CREATE " + ",".join(nodes) + ";"
        self.client.execute_write(cypher)

        # create relationships from boxes and player to the floor
        self.client.execute_write("""
                                    MATCH (p:Player),(f:Floor)
                                        WHERE p.x = f.x AND p.y = f.y
                                    CREATE (p)-[:ON_TOP_OF]->(f);
                                """)

        self.client.execute_write("""
                                    MATCH (b:Box),(f:Floor)
                                        WHERE b.x = f.x AND b.y = f.y
                                    CREATE (b)-[:ON_TOP_OF]->(f);
                                """)
        
        # create relationsships for box targets
        targets = []
        for target_position, box_position in self.env.box_mapping.items():
            targets.append("(b.x = {box_x} AND b.y = {box_y} AND f.x = {tar_x} AND f.y = {tar_y})".format(tar_x=target_position[1], tar_y=target_position[0], box_x=box_position[1], box_y=box_position[0]))
        cypher = "MATCH (b:Box),(f:Floor) WHERE " + " OR ".join(targets) + " CREATE (b)-[:SHOULD_GO_TO]->(f);"
        self.client.execute_write(cypher)

    