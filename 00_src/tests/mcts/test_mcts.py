from mcts.mcts import Builder
from mcts.selection import selection
from mcts.expansion import expansion_random_sampling
from mcts.simulation import simulation
from mcts.backprop import backprop
from environment.environment import SokobanEnvImpl
import numpy as np

def test_solve():
    testee = Builder().build()
    env = SokobanEnvImpl(fixated_env=(
        np.array([[0, 0, 0, 0, 0],
                  [0, 2, 1, 1, 0],
                  [0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0],
                  [0, 2, 4, 5, 0],
                  [0, 0, 0, 0, 0]]),
        {(1, 1): (2, 1)}
    ))
    trajectory, num_explored_nodes, needed_time = testee.solve(env)
    assert len(trajectory) == 1

def test_solve_random_sampling():
    testee = Builder().setSelection(selection).setExpansion(expansion_random_sampling).setSimulation(simulation).setBackprop(backprop).build()
    env = SokobanEnvImpl(use_default_env=True)
    trajectory, num_explored_nodes, needed_time = testee.solve(env)
    assert len(trajectory) == 30