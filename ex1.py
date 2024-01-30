import search
import math
import utils

id = "209540731"

# todo what is an invalid action? eaten? pacman go to wall/end of screen?

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77

WALL = 99
EATEN = 88
EMPTY = 10
PILL = 11
# pill adds 1 to ghost or empty

RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"
STAY = "S"

MOVES = [RIGHT, DOWN, LEFT, UP]

ILLEGAL_MOVE = -1
LEGAL_MOVE = 0



def tuple_state_to_list(tuple_state):
    return (list(row) for row in tuple_state)


def list_state_to_tuple(list_state):
    return tuple(tuple(row) for row in list_state)


def manhattan_distance(point1, point2):
    return sum(abs(val1-val2) for val1, val2 in zip(point1, point2))


def get_new_location(old_location, move):
    new_row = old_location[0]
    new_col = old_location[1]
    if move == UP:
        new_row -= 1
    elif move == DOWN:
        new_row += 1
    elif move == RIGHT:
        new_col += 1
    elif move == LEFT:
        new_col -= 1
    return [new_row, new_col]


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman:
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False
        self.state_n_rows = len(initial)
        self.state_n_cols = 0
        if self.state_n_rows > 0:
            self.state_n_cols = len(initial[0])

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        possible_moves = []
        for move in MOVES:
            move_result = self.result(state, move)
            if move_result is not None:
                possible_moves.append((move, move_result))
        return tuple(possible_moves)

    def get_location(self, state, character):
        for row_i in range(self.state_n_rows):
            for col_i in range(self.state_n_cols):
                if state[row_i][col_i] == character:
                    return [row_i, col_i]
        return None

    def is_legal_location(self, state, location):
        row = location[0]
        col = location[1]
        # check if the location is out of the board
        if (row < 0 or row >= self.state_n_rows) or (col < 0 or col >= self.state_n_cols):
            return False
        # the location is in the board. check that the location is free
        in_cell = state[row][col]
        if in_cell != EMPTY and in_cell != PILL:
            return False

        return True

    def move_pacman(self, state, move):
        # todo fill (is wall / end of board an illegal action, or no move?)
        # get pacman's old location
        pacman_old_location = self.get_location(state, PACMAN)
        if pacman_old_location is None:
            return ILLEGAL_MOVE

        pacman_new_location = get_new_location(pacman_old_location, move)
        if not self.is_legal_location(state, pacman_new_location):
            return ILLEGAL_MOVE

        # move pacman
        state[pacman_old_location[0]][pacman_old_location[1]] = EMPTY
        pacman_new_row = pacman_new_location[0]
        pacman_new_col = pacman_new_location[1]
        state[pacman_new_row][pacman_new_col] = PACMAN
        # 7 is magic number for pacman
        self.locations[7] = [pacman_new_row, pacman_new_col]
        return LEGAL_MOVE

    def move_ghosts(self, state):
        pass #todo fill

    def result(self, state, move):
        """given state and an action and return a new state"""
        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False
        list_state = tuple_state_to_list(state)
        pacman_move = self.move_pacman(list_state, move)
        # todo maybe I can loose the ILLEGAL MOVE and use self.dead_end instead
        if pacman_move == ILLEGAL_MOVE:
            return None
        self.move_ghosts(list_state)
        if self.dead_end:
            return None
        return list_state_to_tuple(list_state)

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        for row in state:
            if PILL in row:
                return False
        return True

    def h(self, node): #todo check
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        remaining_pills = 0
        for row in state:
            remaining_pills += row.count(PILL)
        return remaining_pills


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
