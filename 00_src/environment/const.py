WALL, FLOOR, BOX_TARGET, BOX_ON_TARGET, BOX, PLAYER = 0, 1, 2, 3, 4, 5
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
ACTIONS = [(UP, 0, -1, "Up"), (DOWN, 0, 1, "Down"), (LEFT, -1, 0, "Left"), (RIGHT, 1, 0, "Right")] #(action_id, dx, dy, caption)
action_caption_dict = {0: "WAIT", UP:"UP", DOWN:"DOWN", LEFT:"LEFT", RIGHT:"RIGHT"}
caption_action_dict = {"UP":UP, "DOWN":DOWN, "LEFT":LEFT, "RIGHT":RIGHT}