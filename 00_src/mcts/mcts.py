from environment.environment import SokobanEnvImpl
from knowledge_graph.knowledge_graph import KnowledgeGraph
from mcts.selection import selection
from mcts.expansion import expansion
from mcts.simulation import simulation, eval_state
from mcts.backprop import backprop
from mcts.state import InputState, OverallState, OutputState, GlobalState
from langgraph.utils.runnable import RunnableLike
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
import time

class MonteCarloTreeSearch:
    mcts_step: CompiledStateGraph

    def __init__(self, builder) -> None:        
        langgraph = StateGraph(OverallState, input=InputState, output=OutputState)
        langgraph.add_node("selection", builder.selection)
        langgraph.add_node("expansion", builder.expansion)
        langgraph.add_node("simulation", builder.simulation)
        langgraph.add_node("backprop", builder.backprop)

        langgraph.add_edge(START, "selection")
        langgraph.add_edge("selection", "expansion")
        langgraph.add_edge("expansion", "simulation")
        langgraph.add_edge("simulation", "backprop")
        langgraph.add_edge("backprop", END)

        self.mcts_step = langgraph.compile()
    
    def solve(self, env:SokobanEnvImpl) -> set[int, float]:
        GlobalState().env = env
        GlobalState().kg = KnowledgeGraph(env)
        GlobalState().kg.backprop(eval_state())

        start_time = time.time()
        while True:
            result = self.mcts_step.invoke({})
            if result.get("reward") > 5:
                break
        
        needed_time = time.time() - start_time
        path_nodes, summary, keys = GlobalState().kg.client.read("""MATCH (p:Path) RETURN p""")
        num_explored_nodes = len(path_nodes)
        records, summary, keys = GlobalState().kg.client.read("""MATCH (p:Path) WHERE p.done RETURN p """)
        trajectory = records[0]["p"]["trajectory"]
        return trajectory, num_explored_nodes, needed_time

class Builder:
    selection: RunnableLike
    expansion: RunnableLike
    simulation: RunnableLike
    backprop: RunnableLike

    def __init__(self) -> None:
        self.selection = selection
        self.expansion = expansion
        self.simulation = simulation
        self.backprop = backprop

    def setSelection(self, selection:RunnableLike):
        self.selection = selection
        return self

    def setExpansion(self, expansion:RunnableLike):
        self.expansion = expansion
        return self

    def setSimulation(self, simulation:RunnableLike):
        self.simulation = simulation
        return self

    def setBackprop(self, backprop:RunnableLike):
        self.backprop = backprop
        return self
    
    def build(self) -> MonteCarloTreeSearch:
        return MonteCarloTreeSearch(self)

