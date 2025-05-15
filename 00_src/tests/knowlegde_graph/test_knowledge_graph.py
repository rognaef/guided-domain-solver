import pytest
import numpy as np
from gym_sokoban.envs import SokobanEnv
from knowledge_graph.knowledge_graph import KnowledgeGraph, UP, LEFT
from knowledge_graph.client_neo4j import Neo4jClient

# set up
class SokobanEnvFixated(SokobanEnv):     
    def reset(self, second_player=False, render_mode='rgb_array'):

        self.room_fixed = np.array([[0, 0, 0, 0, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 2, 1, 1, 0],
                                    [0, 2, 1, 1, 0],
                                    [0, 0, 0, 0, 0]])
        self.room_state = np.array([[0, 0, 0, 0, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 2, 4, 1, 0],
                                    [0, 2, 4, 5, 0],
                                    [0, 0, 0, 0, 0]])
        self.box_mapping = {(2, 1): (2, 2), (3, 1): (3, 2)}

        self.player_position = np.argwhere(self.room_state == 5)[0]
        self.num_env_steps = 0
        self.reward_last = 0
        self.boxes_on_target = 0

        starting_observation = self.render(render_mode)
        return starting_observation
env = SokobanEnvFixated(dim_room=(5, 5), max_steps=40, num_boxes=2, num_gen_steps=None, reset=True)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Before each
    yield
    # After each
    env.reset()

def test_static_layer():
    testee = KnowledgeGraph(env=env)
    records, summary, keys = testee.client.read("""
                                MATCH (n:Floor) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 9

def test_dynamic_layer():
    testee = KnowledgeGraph(env=env)
    records, summary, keys = testee.client.read("""
                                MATCH (n:Box) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 2
    records, summary, keys = testee.client.read("""
                                MATCH (n:Player) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 1
    records, summary, keys =  testee.client.read("""
                                MATCH () -[r:SHOULD_GO_TO] -> () RETURN r LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 2
    records, summary, keys =  testee.client.read("""
                                MATCH (n:Action) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 2

def test_update():
    testee = KnowledgeGraph(env=env)
    env.step(UP)
    testee.update()
    records, summary, keys =  testee.client.read("""
                                MATCH (n:Action) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 3
    env.step(LEFT)
    testee.update()
    records, summary, keys =  testee.client.read("""
                                MATCH (n:Action) RETURN n LIMIT $limit
                                """,
                                limit = 25)
    assert len(records) == 2

def test_get_possible_actions():
    testee = KnowledgeGraph(env=env)
    possible_actions = testee.get_possible_actions()
    assert len(possible_actions) == 2
    assert possible_actions[0] == UP
    assert possible_actions[1] == LEFT