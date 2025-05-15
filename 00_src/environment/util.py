from collections import deque
from environment.const import *
from environment.environment import SokobanEnvImpl
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation, PillowWriter
from functools import partial

find_player = lambda env: next((x, y) for y, row in enumerate(env.room_state) for x, val in enumerate(row) if val == PLAYER)
find_boxes = lambda env: [(x, y) for y, row in enumerate(env.room_state) for x, val in enumerate(row) if val == BOX_ON_TARGET or val == BOX]
find_box_targets = lambda env: set((x, y) for y, row in enumerate(env.room_fixed) for x, val in enumerate(row) if val == BOX_TARGET)
in_bound = lambda array, n: n >= 0 and n < len(array)
pos_in_bound = lambda env, x, y: in_bound(env.room_state, y) and in_bound(env.room_state[0], x)

def breadth_first_search(env: SokobanEnvImpl) -> list:
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
        
        # Check if all box targets are covered
        if box_targets.issubset(current_boxes):
            return path
        
        for move, dx, dy, tag in ACTIONS:
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

def render_path(env: SokobanEnvImpl, path:list[int], dpi=300, save_fig=None, show_fig=True):
    """
    Renders the Sokoban environment and overlays the path with arrows and step numbers.

    Args:
        env: The Sokoban environment.
        path: List of actions [UP, DOWN, LEFT, RIGHT] representing the agent's trajectory.
        dpi : float, default: :rc:`figure.dpi` The resolution of the figure in dots-per-inch.
        save_fig: Saves the plot in the given path.
        show_fig: Shows the figure
    """
    image = env.render("rgb_array")

    plt.figure(dpi=dpi)
    plt.imshow(image, origin='upper')
    plt.axis('off')

    # Convert path to coordinates
    initBoxes = find_boxes(env)
    player_coordinates = []
    directions = {UP:(0,-1), DOWN:(0,1), LEFT:(-1,0), RIGHT:(1,0)}
    for action in path:
        start = find_player(env)
        env.step(action)
        end = find_player(env)
        if start == end:
            dx = start[0] + directions.get(action)[0]
            dy = start[1] + directions.get(action)[1]
            end = (dx, dy)
        player_coordinates.append((start,end,action))

    # Scaling for element positions in plot
    scale_begin = lambda a : a * 16
    scale = lambda a : scale_begin(a) + 8

    # Draw final boxes
    for box_coordinate in find_boxes(env):
        img = mpimg.imread('./environment/elements/box.png')
        img_box = plt.imshow(img, alpha=0.3, zorder=1)
        transform = mpl.transforms.Affine2D().translate(scale_begin(box_coordinate[0]), scale_begin(box_coordinate[1]))
        img_box.set_transform(transform + plt.gca().transData)

    # Mark the final position
    final = find_player(env)
    if final not in initBoxes:
        img = mpimg.imread('./environment/elements/player.png')
        img_player = plt.imshow(img, alpha=0.3, zorder=2)
        transform = mpl.transforms.Affine2D().translate(scale_begin(final[0]), scale_begin(final[1]))
        img_player.set_transform(transform + plt.gca().transData)

    # Draw Arrows
    mid_points = []
    arrow_scale = 1
    action_arrow_x = {UP:0, DOWN:0, LEFT:-arrow_scale, RIGHT:arrow_scale}
    action_arrow_y = {UP:-arrow_scale, DOWN:arrow_scale, LEFT:0, RIGHT:0}
    for coordinates in player_coordinates:
        start = coordinates[0]
        end = coordinates[1]
        action = coordinates[2]

        scale_d = lambda a,b : scale(a) - scale(b)
        scale_mid = lambda a,b: (scale(a) + scale(b)) / 2
        plt.arrow(
            scale(start[0]) + action_arrow_x.get(action), 
            scale(start[1]) + action_arrow_y.get(action),
            scale_d(end[0], start[0]) - (2*action_arrow_x.get(action)), 
            scale_d(end[1], start[1]) - (2*action_arrow_y.get(action)),
            head_width=2,
            head_length=2,
            fc='green',
            ec='green',
            length_includes_head=True
        )

        mid_points.append((scale_mid(end[0], start[0]), scale_mid(end[1], start[1])))

    # Add step numbers
    mid_index_dict = {}
    for i, mid in enumerate(mid_points):
        mid_index_dict.setdefault(mid, []).append(i) 
    for mid, indexes in mid_index_dict.items():
        limited = indexes[:4]
        parts = []

        for i, num in enumerate(limited):
            parts.append(str(num+1))
            if i % 2 == 1 and i != len(limited) - 1:
                parts.append('\n')
            elif i != len(limited) - 1:
                parts.append(', ')

        if len(indexes) > 4:
            parts.append('...')

        step_numbers = ''.join(parts)
        plt.text(mid[0], mid[1], step_numbers, color='white', fontsize=4,
                 ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="none", alpha=0.7))

    if save_fig is not None:
        plt.savefig(save_fig , bbox_inches='tight', pad_inches = 0)

    if show_fig:
        plt.show()

def animate_path(env:SokobanEnvImpl, path:list[int], save_ani:str, draw_arrows=True, dpi=300) -> None:
    """
    Renders the Sokoban environment and overlays the path with arrows and step numbers.

    Args:
        env: The Sokoban environment.
        path: List of actions [UP, DOWN, LEFT, RIGHT] representing the agent's trajectory.
        save_ani: Saves the animation in the given path.
        draw_arrows: Draws arrows of the trajectory.
        dpi : float, default: :rc:`figure.dpi` The resolution of the figure in dots-per-inch.
    """
    fig = plt.figure(figsize=(5, 5), dpi=dpi, frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.]) 
    ax.set_axis_off()
    fig.add_axes(ax)

    image = env.render("rgb_array")
    im = plt.imshow(image)
    plt.axis('off')
    
    ani = FuncAnimation(fig, partial(_animate, env=env, path=path, im=im, fig=fig, draw_arrows=draw_arrows), frames=len(path)+1)
    ani.save(save_ani, dpi=dpi, writer=PillowWriter(fps=3), savefig_kwargs={"pad_inches":0})

    plt.close()

def _animate(frame, env, path, im, fig, draw_arrows=False):
    if frame==0:
        env.reset()
    else:
        _take_step(env, path, frame-1, fig, draw_arrows)

    im.set_array(env.render("rgb_array"))
    return [im]

def _take_step(env, path, step, fig, draw_arrows):
    if not draw_arrows:
        env.step(path[step])
        return
    
    # reset
    for text in fig.gca().texts:
        text.remove()
    env.reset()

    # Convert path to coordinates
    player_coordinates = []
    directions = {UP:(0,-1), DOWN:(0,1), LEFT:(-1,0), RIGHT:(1,0)}
    for action in path[0:step+1]:
        start = find_player(env)
        env.step(action)
        end = find_player(env)
        if start == end:
            dx = start[0] + directions.get(action)[0]
            dy = start[1] + directions.get(action)[1]
            end = (dx, dy)
        player_coordinates.append((start,end,action))

    # Draw Arrows
    mid_points = []
    arrow_scale = 1
    action_arrow_x = {UP:0, DOWN:0, LEFT:-arrow_scale, RIGHT:arrow_scale}
    action_arrow_y = {UP:-arrow_scale, DOWN:arrow_scale, LEFT:0, RIGHT:0}
    for coordinates in player_coordinates:
        start = coordinates[0]
        end = coordinates[1]
        action = coordinates[2]

        scale_begin = lambda a : a * 16
        scale = lambda a : scale_begin(a) + 8
        scale_d = lambda a,b : scale(a) - scale(b)
        scale_mid = lambda a,b: (scale(a) + scale(b)) / 2
        plt.arrow(
            scale(start[0]) + action_arrow_x.get(action), 
            scale(start[1]) + action_arrow_y.get(action),
            scale_d(end[0], start[0]) - (2*action_arrow_x.get(action)), 
            scale_d(end[1], start[1]) - (2*action_arrow_y.get(action)),
            head_width=2,
            head_length=2,
            fc='green',
            ec='green',
            length_includes_head=True
        )

        mid_points.append((scale_mid(end[0], start[0]), scale_mid(end[1], start[1])))

    # Add step numbers
    mid_index_dict = {}
    for step, mid in enumerate(mid_points):
        mid_index_dict.setdefault(mid, []).append(step) 
    for mid, indexes in mid_index_dict.items():
        limited = indexes[:4]
        parts = []

        for step, num in enumerate(limited):
            parts.append(str(num+1))
            if step % 2 == 1 and step != len(limited) - 1:
                parts.append('\n')
            elif step != len(limited) - 1:
                parts.append(', ')

        if len(indexes) > 4:
            parts.append('...')

        step_numbers = ''.join(parts)
        plt.text(mid[0], mid[1], step_numbers, color='white', fontsize=6,
                 ha='center', va='center', bbox=dict(boxstyle="round,pad=0.2", fc="black", ec="none", alpha=0.7))