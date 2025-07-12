from mcts.mcts import Builder
from mcts.selection import selection
from mcts.expansion import expansion_random_sampling
from mcts.simulation import simulation
from mcts.backprop import backprop
from environment.environment import SokobanEnvImpl
import numpy as np
import random

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

def test_solve_multiple():
    testee = Builder().build()
    env_01 = SokobanEnvImpl(fixated_env=(
        np.array([[0, 0, 0, 0, 0],
                  [0, 2, 1, 1, 0],
                  [0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0],
                  [0, 2, 4, 5, 0],
                  [0, 0, 0, 0, 0]]),
        {(1, 1): (2, 1)}
    ))
    env_02 = SokobanEnvImpl(fixated_env=(
        np.array([[0, 0, 0, 0, 0],
                  [0, 1, 1, 2, 0],
                  [0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0],
                  [0, 5, 4, 2, 0],
                  [0, 0, 0, 0, 0]]),
        {(3, 1): (2, 1)}
    ))
    trajectory, num_explored_nodes, needed_time = testee.solve(env_01, log_path="../tests/mcts/output/01_test_")
    assert len(trajectory) == 1
    trajectory, num_explored_nodes, needed_time = testee.solve(env_02, log_path="../tests/mcts/output/02_test_")
    assert len(trajectory) == 1

def test_solve_random_sampling():
    testee = Builder().setSelection(selection).setExpansion(expansion_random_sampling).setSimulation(simulation).setBackprop(backprop).build()
    env = SokobanEnvImpl(fixated_env=(
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0],
                  [0, 1, 1, 1, 2, 0],
                  [0, 2, 1, 1, 2, 0],
                  [0, 1, 1, 1, 2, 0],
                  [0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0],
                  [0, 5, 0, 0, 0, 0],
                  [0, 4, 4, 1, 2, 0],
                  [0, 2, 1, 4, 2, 0],
                  [0, 1, 1, 4, 2, 0],
                  [0, 0, 0, 0, 0, 0]]),
        {(2,4):(2,2), (3,1):(2,1), (3,4):(3,3), (4,4):(4,3)}
    ))
    random.seed(42)
    trajectory_1, num_explored_nodes_1, needed_time_1 = testee.solve(env)
    assert len(trajectory_1) == 9

    env.reset()
    random.seed(42)
    trajectory_2, num_explored_nodes_2, needed_time_2 = testee.solve(env)
    assert len(trajectory_2) == 9
    assert num_explored_nodes_1 == num_explored_nodes_2