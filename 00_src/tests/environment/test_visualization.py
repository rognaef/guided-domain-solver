import numpy as np
from environment.environment import SokobanEnvImpl
from environment.visualization import *

env = SokobanEnvImpl(use_default_env=True)

def test_render():
    render(env=env, save_fig="./tests/environment/output/test_render.png", show_fig=False)

def test_render_trajectory():
    render(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_fig="./tests/environment/output/test_render_trajectory.png", show_fig=False)

def test_animate():
    animate(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_ani="./tests/environment/output/test_animate.gif", draw_arrows=False)

def test_animate_trajectory():
    animate(env=env, path=[RIGHT, RIGHT, RIGHT, DOWN, LEFT, LEFT, LEFT, LEFT, DOWN, LEFT, LEFT, DOWN, DOWN, RIGHT, UP, LEFT, UP, UP, RIGHT, RIGHT, DOWN, LEFT, UP, LEFT, DOWN, UP, UP, RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN, DOWN], save_ani="./tests/environment/output/test_animate_trajectory.gif")
