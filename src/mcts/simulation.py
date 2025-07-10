from environment.const import *
from environment.util import breadth_first_search
from .state import OverallState, GlobalState

def eval_state()->float:
    optimal = breadth_first_search(GlobalState().env)
    state_value = 0
    if optimal != None:
        state_value = (60-len(optimal))/60
    return state_value

def simulation(state: OverallState) -> OverallState:
    sim_value = eval_state()
    return {"reward":state.get("reward"), "done":state.get("done"), "sim_value":sim_value}