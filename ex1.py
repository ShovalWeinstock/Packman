import search
import math
import utils

id = "No numbers - I'm special!"

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

MOVES = [RIGHT, DOWN, LEFT, UP]


def tuple_state_to_list(tuple_state):
    return (list(row) for row in tuple_state)


def list_state_to_tuple(list_state):
    return tuple(tuple(row) for row in list_state)


class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""

    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman:
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman."""

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False
        self.state_rows = len(initial)
        self.state_cols = len(initial[0])

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    def successor(self, state):
        """ Generates the successor state """
        possible_moves = []
        for move in MOVES:
            move_result = self.result(state, move)
            if move_result is not None:
                possible_moves.append(tuple(move, move_result))
        return tuple(possible_moves)
#       utils.raiseNotDefined()

    def move_packman(self, state, move):
        pass

    def move_ghosts(self, state):
        pass

    def result(self, state, move):
        """given state and an action and return a new state"""
        list_state = tuple_state_to_list(state)
        self.move_packman(state, move)
        self.move_ghosts(state)
        return list_state_to_tuple(list_state)
#       utils.raiseNotDefined()

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        for row in state:
            for item in row:
                if item == PILL:
                    return False
        return True
#        utils.raiseNotDefined()

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        utils.raiseNotDefined()


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
