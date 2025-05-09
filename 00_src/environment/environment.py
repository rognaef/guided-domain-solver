import numpy as np
from gym_sokoban.envs import SokobanEnv
from gym.spaces.discrete import Discrete
from environment.const import *

class SokobanEnvImpl(SokobanEnv):
    fixatedEnv:tuple[np.array, np.array, dict] #(room_fixed, room_state, box_mapping)

    def __init__(self, dim_room=(10, 10), max_steps=120, num_boxes=4, num_gen_steps=None, reset=True, fixatedEnv=None):
        self.fixatedEnv = fixatedEnv
        super().__init__(dim_room=dim_room, max_steps=max_steps, num_boxes=num_boxes, num_gen_steps=num_gen_steps, reset=reset)
        self.action_space = Discrete(5) # limit to push actions

    def reset(self, second_player=False, render_mode='rgb_array') -> None:
        if (self.fixatedEnv is None):
            super().reset(second_player=second_player, render_mode=render_mode)
        else:
            self._reset_fixated_env(render_mode=render_mode)
    
    def _reset_fixated_env(self, render_mode:str) -> None:
        self.room_fixed = self.fixatedEnv[0].copy()
        self.room_state = self.fixatedEnv[1].copy()
        self.box_mapping = self.fixatedEnv[2].copy()

        self.player_position = np.argwhere(self.room_state == PLAYER)[0]
        self.num_env_steps = 0
        self.reward_last = 0
        self.boxes_on_target = 0

        starting_observation = self.render(render_mode)
        return starting_observation # Close environment after testing