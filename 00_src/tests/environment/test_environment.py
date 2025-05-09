import numpy as np
from environment.environment import SokobanEnvImpl
from environment.util import *

def test_environment():
    testee = SokobanEnvImpl(dim_room=(8, 8), max_steps=120, num_boxes=2)
    assert testee.dim_room == (8,8)
    assert find_player(testee) is not None
    assert len(find_boxes(testee)) == 2

def test_fixated_environment():
    testee = SokobanEnvImpl(fixatedEnv=(
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                  [0, 1, 1, 1, 1, 2, 1, 1, 1, 0],
                  [0, 1, 1, 1, 2, 1, 1, 1, 1, 0],
                  [0, 1, 1, 1, 0, 1, 1, 2, 1, 0],
                  [0, 2, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                  [0, 1, 1, 4, 5, 2, 1, 1, 1, 0],
                  [0, 1, 1, 1, 2, 4, 1, 4, 1, 0],
                  [0, 1, 1, 1, 0, 1, 1, 2, 1, 0],
                  [0, 2, 4, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        {(6, 7): (5, 7), (5, 4): (5, 5), (4, 5): (4, 3), (7, 1): (7, 2)}
    ))
    assert find_player(testee) == (4,4)
    testee.step(RIGHT)
    assert find_player(testee) == (5,4)
    testee.reset()
    assert find_player(testee) == (4,4)