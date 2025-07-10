from environment.const import *
from environment.util import find_shortest_paths_to_place_remaining_boxes
from agents.agent_ollama import AgentOllama
import random
import ast
from mcts.state import OverallState, GlobalState

agent_player = AgentOllama("qwen3:32b",
[("system","You are a player which tries to solve a Sokoban game. Keep the reasoning short. Respond only with a single action out of ['UP', 'DOWN', 'LEFT', 'RIGHT'].",),
("human",("""Use the following results retrieved from a database to provide the next action for the Sokoban game.
Enviroment: {enviorment}
Shortest paths to place remaining boxes: {shortest_paths_to_place_remaining_boxes}
Attempted Actions: {attempted_actions}
Posstible Actions: {possible_actions}
Action: """),),],
extract_reasoning=True)

def expansion(state: OverallState) -> OverallState:
     id = state.get("selection_id")
     trajectory = state.get("selection_trajectory")
     GlobalState().env.set_state(trajectory)
     GlobalState().kg.set_state(trajectory)

     #Enviroment
     enviroment, summary, keys =  GlobalState().kg.client.read("""
                                                 MATCH (e) 
                                                 WHERE NOT e:Path AND NOT e:Action
                                                 RETURN 
                                                  CASE 
                                                    WHEN e.has_box_target IS NOT NULL THEN {caption: e.caption, x: e.x, y: e.y, has_box_target: e.has_box_target}
                                                    WHEN e.is_on_target IS NOT NULL THEN {caption: e.caption + ' [' + toString(e.x) + ',' + toString(e.y) + ']', x: e.x, y: e.y, is_on_target: e.is_on_target}
                                                    ELSE {caption: e.caption, x: e.x, y: e.y}
                                                END AS environment""")
     
     # Shortest Paths to place remaining boxes
     shortest_paths_to_place_remaining_boxes = find_shortest_paths_to_place_remaining_boxes(GlobalState().env)
     
     # Attempted actions
     attempted_actions, summary, keys =  GlobalState().kg.client.read("""
                            MATCH (p:Path {{id: {id}}})-[m:MOVE]->(c:Path)
                            MATCH (a:Action)
                            WHERE m.id = a.id
                            RETURN {{caption: a.caption, reward: p.reward-c.reward}} AS attempted_actions
                            """.format(id=id))

     # Unexplored actions
     records, summary, keys =  GlobalState().kg.client.read("""
                            MATCH (a:Action)
                            WHERE NOT EXISTS {{
                              MATCH (p:Path {{id: {id}}})-[m:MOVE]->(c:Path)
                              WHERE m.id = a.id
                            }}
                            RETURN a.caption AS possible_actions
                            """.format(id=id))
     possible_actions = [caption_action_dict.get(record["possible_actions"].upper()) for record in records]
     
     # agent
     next_step = agent_player.invoke(
        {"enviorment": enviroment,
         "shortest_paths_to_place_remaining_boxes": shortest_paths_to_place_remaining_boxes,
         "attempted_actions": attempted_actions,
         "possible_actions": records}
     )
     
     # evaluate action
     next_action = 0 # default do nothing
     for action_id in caption_action_dict.keys():
        if action_id in next_step:
            next_action = caption_action_dict.get(action_id)
    
     # fail safe
     if next_action not in possible_actions:
         next_action = random.choice(possible_actions)

     observation, reward_last, done, info = _doStep(next_action)

     return {"reward":reward_last, "done":done}

def expansion_random_sampling(state: OverallState) -> OverallState:
     id = state.get("selection_id")
     trajectory = state.get("selection_trajectory")
     GlobalState().env.set_state(trajectory)
     GlobalState().kg.set_state(trajectory)
     
     # Shortest Paths to place remaining boxes
     shortest_paths_to_place_remaining_boxes = find_shortest_paths_to_place_remaining_boxes(GlobalState().env)

     # Unexplored actions
     records, summary, keys =  GlobalState().kg.client.read("""
                            MATCH (a:Action)
                            WHERE NOT EXISTS {{
                              MATCH (p:Path {{id: {id}}})-[m:MOVE]->(c:Path)
                              WHERE m.id = a.id
                            }}
                            RETURN a.caption AS possible_actions
                            ORDER BY a.id DESC
                            """.format(id=id))
     possible_actions = [caption_action_dict.get(record["possible_actions"].upper()) for record in records]
    
     
     # evaluate action
     next_action = 0 # default do nothing
     random_choice = ast.literal_eval(random.choice(shortest_paths_to_place_remaining_boxes)['shortest_path_to_place'])
     if random_choice is not None:
        next_action = caption_action_dict.get(random_choice[0])
    
     # fail safe
     if next_action not in possible_actions:
        next_action = random.choice(possible_actions)

     observation, reward_last, done, info = _doStep(next_action)

     return {"reward":reward_last, "done":done}

def _doStep(action:int) -> bool:
    observation, reward_last, done, info = GlobalState().env.step(action)
    GlobalState().kg.step(action, reward_last, done)
    return observation, reward_last, done, info