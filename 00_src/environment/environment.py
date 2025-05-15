import copy
import numpy as np
from gym_sokoban.envs import SokobanEnv
from gym.spaces.discrete import Discrete
from environment.const import *

DEFAULT_ENVIRONMENT = (
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
    )

class SokobanEnvImpl(SokobanEnv):
    fixated_env:tuple[np.array, np.array, dict] #(room_fixed, room_state, box_mapping)

    def __init__(self, dim_room=(10, 10), max_steps=120, num_boxes=4, num_gen_steps=None, reset=True, fixated_env=None, use_default_env=False):
        self.fixated_env = DEFAULT_ENVIRONMENT if use_default_env else fixated_env
        super().__init__(dim_room=dim_room, max_steps=max_steps, num_boxes=num_boxes, num_gen_steps=num_gen_steps, reset=reset)
        self.action_space = Discrete(5) # limit to push actions

    def reset(self, second_player=False, render_mode='rgb_array') -> None:
        if (self.fixated_env is None):
            super().reset(second_player=second_player, render_mode=render_mode)
        else:
            self._reset_fixated_env(render_mode=render_mode)
    
    def _reset_fixated_env(self, render_mode:str) -> None:
        self.room_fixed = self.fixated_env[0].copy()
        self.room_state = self.fixated_env[1].copy()
        self.box_mapping = self.fixated_env[2].copy()

        self.player_position = np.argwhere(self.room_state == PLAYER)[0]
        self.num_env_steps = 0
        self.reward_last = 0
        self.boxes_on_target = 0

        starting_observation = self.render(render_mode)
        return starting_observation # Close environment after testing
    
    def as_fixated(self) -> SokobanEnv:
        env = copy.deepcopy(self)
        env.fixated_env = (self.room_fixed, self.room_state, self.box_mapping)
        return env