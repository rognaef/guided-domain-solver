from .state import InputState, OverallState, GlobalState
         
def selection(state: InputState) -> OverallState:
    records, summary, keys =  GlobalState().kg.client.read("""
                            MATCH (p:Path)
                            WHERE p.done = false AND size([ (p)-[:MOVE]->(x) | x ]) < size(p.possible_actions)
                            RETURN p
                            ORDER BY p.value DESC
                            LIMIT 1
                            """)
    if len(records) != 1:
          raise Exception("No further paths can be examined.")
    return {"selection_id":records[0]["p"]["id"], "selection_trajectory":records[0]["p"]["trajectory"]}