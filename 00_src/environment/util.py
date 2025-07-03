from collections import deque
from environment.const import *
from environment.environment import SokobanEnvImpl
import numpy as np
import copy
import sys

action_caption_dict = {0: "WAIT", UP:"UP", DOWN:"DOWN", LEFT:"LEFT", RIGHT:"RIGHT"}

find_player = lambda env: next((x, y) for y, row in enumerate(env.room_state) for x, val in enumerate(row) if val == PLAYER)
find_boxes = lambda env: [(x, y) for y, row in enumerate(env.room_state) for x, val in enumerate(row) if val == BOX_ON_TARGET or val == BOX]
find_box_targets = lambda env: set((x, y) for y, row in enumerate(env.room_fixed) for x, val in enumerate(row) if val == BOX_TARGET)
in_bound = lambda array, n: n >= 0 and n < len(array)
pos_in_bound = lambda env, x, y: in_bound(env.room_state, y) and in_bound(env.room_state[0], x)

def breadth_first_search(env: SokobanEnvImpl) -> list:
    """
    Seraches the optimal path with a bredth first search in the given enviroment

    Args:
        env: The Sokoban environment.
    """
    # Find initial player position and boxes
    player_pos = find_player(env)
    boxes = find_boxes(env)
    box_targets = find_box_targets(env)
    
    # Convert boxes to a sorted tuple for consistent state representation
    initial_boxes = tuple(sorted(boxes))
    
    # BFS initialization
    visited = set()
    queue = deque()
    queue.append((player_pos, initial_boxes, []))
    visited.add((player_pos, initial_boxes))
    
    while queue:
        current_pos, current_boxes, path = queue.popleft()
        
        # Check if all box targets are covered or all boxes are placed
        if box_targets.issubset(current_boxes) or set(current_boxes).issubset(box_targets):
            return path
        
        for move, dx, dy, caption in ACTIONS:
            new_x = current_pos[0] + dx
            new_y = current_pos[1] + dy
            
            # Check if new position is within bounds and not a wall
            if pos_in_bound(env, new_x, new_y):
                if env.room_fixed[new_y][new_x] == WALL:
                    continue  # Wall, cannot move here
                
                # Check if the new position is a box
                if (new_x, new_y) in current_boxes:
                    # Calculate new box position
                    box_new_x = new_x + dx
                    box_new_y = new_y + dy
                    
                    # Check if new box position is valid
                    if pos_in_bound(env, box_new_x, box_new_y):
                        if env.room_fixed[box_new_y][box_new_x] != WALL and (box_new_x, box_new_y) not in current_boxes:
                            # Create new boxes tuple
                            new_boxes_list = list(current_boxes)
                            new_boxes_list.remove((new_x, new_y))
                            new_boxes_list.append((box_new_x, box_new_y))
                            new_boxes = tuple(sorted(new_boxes_list))
                            
                            # New player position is (new_x, new_y)
                            new_pos = (new_x, new_y)
                            
                            # Check if this state has been visited
                            state_key = (new_pos, new_boxes)
                            if state_key not in visited:
                                visited.add(state_key)
                                queue.append((new_pos, new_boxes, path + [move]))
                else:
                    # Move to empty space
                    new_pos = (new_x, new_y)
                    state_key = (new_pos, current_boxes)
                    if state_key not in visited:
                        visited.add(state_key)
                        queue.append((new_pos, current_boxes, path + [move]))
    
    # No solution found
    return None
                
def find_shortest_paths_to_place_remaining_boxes(env:SokobanEnvImpl) -> list:
    """
    Seraches the shortest paths to place every remaining box in the given enviroment individually.
    To find the shortest path for a box, the other boxes are considered as walls

    Args:
        env: The Sokoban environment.
    """
    result = []
    for y, row in enumerate(env.room_state):
        for x, val in enumerate(row):
            if val == BOX:
                search_env = _create_search_env(env, (x,y))
                path = np.array2string(np.vectorize(action_caption_dict.get)(breadth_first_search(search_env)), separator=", ", max_line_width=sys.maxsize)
                result.append({"caption":"Box [{x},{y}]".format(x=x, y=y), "x":x, "y":y, "shortest_path_to_place":path})
    result_sorted = sorted(result, key=lambda n: len(n['shortest_path_to_place']))
    return result_sorted

def _create_search_env(env:SokobanEnvImpl, target_box:tuple[int,int]) -> SokobanEnvImpl:
    room_state = copy.deepcopy(env.room_state)
    room_fixed = copy.deepcopy(env.room_fixed)

    for y, row in enumerate(room_state):
        for x, val in enumerate(row):
            if (val == BOX and not (x == target_box[0] and y == target_box[1])) or val == BOX_ON_TARGET:
                room_state[y][x] = WALL
                room_fixed[y][x] = WALL
    return SokobanEnvImpl(fixated_env=(room_fixed,room_state,{}))