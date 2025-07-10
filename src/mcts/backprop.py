from mcts.state import OverallState, OutputState, GlobalState

def backprop(state: OverallState) -> OutputState:
    GlobalState().kg.backprop(state.get("sim_value"))
    return {"reward":state.get("reward"), "done":state.get("done")}