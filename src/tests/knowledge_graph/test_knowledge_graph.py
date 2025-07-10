import pytest
import numpy as np
from gym_sokoban.envs import SokobanEnv
from knowledge_graph.knowledge_graph import KnowledgeGraph, UP, LEFT

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

def test_step():
    testee = KnowledgeGraph(env=env)
    assert testee.step(UP, -0.1, False) == None

def test_set_state():
    testee = KnowledgeGraph(env=env)
    assert testee.step(UP, -0.1, False) == None
    assert testee.set_state([UP]) == None

def test_backprop():
    testee = KnowledgeGraph(env=env)
    assert testee.backprop(-0.1) == None

def test_get_possible_actions():
    testee = KnowledgeGraph(env=env)
    possible_actions = testee.get_possible_actions()
    assert len(possible_actions) == 2
    assert UP in possible_actions
    assert LEFT in possible_actions