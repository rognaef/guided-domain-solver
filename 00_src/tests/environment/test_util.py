import numpy as np
from environment.environment import SokobanEnvImpl
from environment.util import *

env = SokobanEnvImpl(fixatedEnv=(
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

def test_find_player():
    assert find_player(env) == (4,4)

def test_find_boxes():
    assert find_boxes(env) == [(3, 4), (5, 5), (7, 5), (2, 7)]

def test_find_box_targets():
    assert list(sorted(find_box_targets(env))) == [(1, 7), (4, 5), (5, 4), (7, 6)]

def test_pos_in_bound():
    assert pos_in_bound(env, 5, 5) == True
    assert pos_in_bound(env, 11, 5) == False
    assert pos_in_bound(env, 5, 11) == False
    assert pos_in_bound(env, -1, 5) == False
    assert pos_in_bound(env, 5, -1) == False

def test_breadth_first_search():
    assert len(breadth_first_search(env=env)) == 30

def test_breadth_first_search_unsolvable():
    unsolvable_env = SokobanEnvImpl(fixatedEnv=(
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                  [0, 1, 2, 1, 1, 2, 1, 1, 1, 0],
                  [0, 1, 1, 1, 2, 1, 1, 1, 1, 0],
                  [0, 1, 1, 1, 0, 1, 1, 2, 1, 0],
                  [0, 2, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                  [0, 1, 2, 4, 5, 2, 1, 1, 1, 0],
                  [0, 1, 1, 1, 2, 4, 1, 4, 1, 0],
                  [0, 1, 1, 1, 0, 1, 1, 2, 1, 0],
                  [0, 2, 4, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        {(6, 7): (5, 7), (5, 4): (5, 5), (4, 5): (4, 3), (7, 1): (7, 2)}
    )) # more box targets than boxes
    assert breadth_first_search(env=unsolvable_env) == None

def test_render_path():
    render_path(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_fig="./tests/environment/output/test_render_path.png", show_fig=False)

def test_animate_path():
    animate_path(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_ani="./tests/environment/output/test_animate_path.gif", draw_arrows=False)

def test_animate_path_trajectory():
    animate_path(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_ani="./tests/environment/output/test_animate_path_trajectory.gif")
