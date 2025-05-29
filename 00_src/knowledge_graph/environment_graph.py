from knowledge_graph.client_neo4j import Neo4jClient
from knowledge_graph.graph_interface import GraphInterface
from environment.const import *
from environment.util import *
from gym_sokoban.envs import SokobanEnv

class EnvironmentGraph(GraphInterface):
    client : Neo4jClient
    env: SokobanEnv

    def __init__(self, env: SokobanEnv, client: Neo4jClient) -> None:
        self.env = env
        self.client = client
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
                    caption = "Floor [{x},{y}]".format(x=x, y=y)
                    has_box_target = tile == BOX_TARGET
                    nodes.append("(:Floor {{id: {id}, x:{x}, y:{y}, has_box_target:{has_box_target}, caption:\"{caption}\"}})".format(id=id, x=x, y=y, has_box_target=has_box_target, caption=caption))
                    id+=1
        cypher = "CREATE " + ",".join(nodes) + ";"
        self.client.write(cypher)

        # create relationships for neighbouring tiles
        self.client.write("""
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
                    caption = "Box"
                    is_on_target = tile == BOX_ON_TARGET
                    nodes.append("(:Box {{id: {id}, x:{x}, y:{y}, is_on_target:{is_on_target}, caption:\"{caption}\"}})".format(id=box_id, x=x, y=y, is_on_target=is_on_target, caption=caption))
                    box_id+=1
                elif tile == PLAYER:
                    caption = "Player"
                    nodes.append("(:Player {{id: {id}, x:{x}, y:{y}, caption:\"{caption}\"}})".format(id=player_id, x=x, y=y, caption=caption))
                    player_id+=1
        cypher = "CREATE " + ",".join(nodes) + ";"
        self.client.write(cypher)
        
        # create relationships for box targets
        targets = []
        for target_position, box_position in self.env.box_mapping.items():
            targets.append("(b.x = {box_x} AND b.y = {box_y} AND f.x = {tar_x} AND f.y = {tar_y})".format(tar_x=target_position[1], tar_y=target_position[0], box_x=box_position[1], box_y=box_position[0]))
        cypher = "MATCH (b:Box),(f:Floor) WHERE " + " OR ".join(targets) + " CREATE (b)-[:SHOULD_GO_TO]->(f);"
        self.client.write(cypher)

        self._create_position_relationshpis()
        self._create_action_nodes()
    
    def _create_position_relationshpis(self):
        # create relationships from boxes and player to the floor
        self.client.write("""
                                    MATCH (p:Player),(f:Floor)
                                        WHERE p.x = f.x AND p.y = f.y
                                    CREATE (p)-[:ON_TOP_OF]->(f);
                                """)

        self.client.write("""
                                    MATCH (b:Box),(f:Floor)
                                        WHERE b.x = f.x AND b.y = f.y
                                    CREATE (b)-[:ON_TOP_OF]->(f);
                                """)
    
    def _clear_position_relationships(self):
        self.client.write("""
                                    MATCH () -[r:ON_TOP_OF] -> () DELETE r
                                """)
    
    def _create_action_nodes(self) -> None:
        # create nodes for the actions
        nodes =[]
        player_pos = find_player(self.env)
        for id, dx, dy, caption  in ACTIONS:
            player_x, player_y = player_pos[0] + dx, player_pos[1] + dy
            box_x, box_y = player_x + dx, player_y + dy
            can_move = pos_in_bound(self.env, player_x, player_y) and self.env.room_state[player_y, player_x] in [FLOOR, BOX_TARGET]
            can_push_box = self.env.room_state[player_y, player_x] in [BOX_ON_TARGET, BOX] and pos_in_bound(self.env, box_x, box_y) and self.env.room_state[box_y, box_x] in [FLOOR, BOX_TARGET]
            if can_move or can_push_box:
                nodes.append("(:Action {{id: {id}, dx:{dx}, dy:{dy}, caption:\"{caption}\"}})".format(id=id, dx=dx, dy=dy, caption=caption))
        cypher = "CREATE " + ",".join(nodes) + ";"
        self.client.write(cypher)

        # create relationships from player to actions
        self.client.write("""
                                    MATCH (p:Player),(a:Action)
                                    CREATE (p)-[:CAN_MOVE]->(a);
                                """)
    
    def _clear_action_nodes(self) -> None:
        self.client.write("""
                                    MATCH () -[r:CAN_MOVE] -> () DELETE r
                                """)
        self.client.write("""
                                    MATCH (a:Action) DELETE a
                                """)
    
    def update(self) -> None:
        self._clear_position_relationships()
        self._clear_action_nodes()
        self._update_player_position()
        self._update_box_positions()
        self._create_position_relationshpis()
        self._create_action_nodes()

    def _update_player_position(self) -> None:
        player_pos = find_player(self.env)
        self.client.write("MATCH (p:Player {{id: {id}}}) SET p += {{x: {x}, y: {y}}} RETURN p".format(id=1, x=player_pos[0], y=player_pos[1]))

    def _update_box_positions(self) -> None:
        boxes = find_boxes(self.env)
        updatable_boxes = []
        records, summary, keys = self.client.read("""
                                MATCH (b:Box) RETURN b
                                """)
        for record in records:
            box_pos = (record["b"].get('x'), record["b"].get('y'))
            if box_pos in boxes:
                boxes.remove(box_pos)
            else:
                updatable_boxes.append(record)
        for update_record in updatable_boxes:
            id = update_record["b"].get('id')
            box_pos = boxes[0]
            self.client.write("MATCH (b:Box {{id: {id}}}) SET b += {{x: {x}, y: {y}}} RETURN b".format(id=id, x=box_pos[0], y=box_pos[1]))
            boxes.remove(box_pos)