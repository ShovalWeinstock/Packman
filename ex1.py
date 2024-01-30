import search
import math
import utils

id = "209540731"

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
GHOSTS = [RED, BLUE, YELLOW, GREEN]

# todo delete
# ILLEGAL_MOVE = -1
# LEGAL_MOVE = 0


def tuple_state_to_list(tuple_state):
    return [list(row) for row in tuple_state]


def list_state_to_tuple(list_state):
    return tuple(tuple(row) for row in list_state)


def manhattan_distance(point1, point2):
    return sum(abs(val1-val2) for val1, val2 in zip(point1, point2))


def calc_new_location(old_location, move):
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

    def get_ghost_location(self, state, ghost):
        location = self.get_location(state, ghost)
        if location is None:
            # ghost on pill
            location = self.get_location(state, ghost+1)
        return location

    def is_in_board(self, location):
        row = location[0]
        col = location[1]
        return 0 <= row < self.state_n_rows and 0 <= col < self.state_n_cols

    def is_legal_location(self, state, location):
        if not self.is_in_board(location):
            return False
        # the location is in the board. check that the location is free
        in_cell = state[location[0]][location[1]]
        if in_cell != EMPTY and in_cell != PILL and in_cell != PACMAN:
            return False

        return True

    def move_pacman(self, state, move):
        # get pacman's old location
        pacman_old_location = self.get_location(state, PACMAN)
        if pacman_old_location is None:
            self.dead_end = True
            return #todo
            #return ILLEGAL_MOVE

        pacman_new_location = calc_new_location(pacman_old_location, move)
        if not self.is_legal_location(state, pacman_new_location):
            self.dead_end = True
            return  # todo
            #return ILLEGAL_MOVE

        # move pacman
        state[pacman_old_location[0]][pacman_old_location[1]] = EMPTY
        pacman_new_row = pacman_new_location[0]
        pacman_new_col = pacman_new_location[1]
        state[pacman_new_row][pacman_new_col] = PACMAN
        # 7 is magic number for pacman
        self.locations[7] = [pacman_new_row, pacman_new_col]
        #return LEGAL_MOVE todo

    def move_ghost(self, state, old_location, new_location, ghost):
        old_row = old_location[0]
        old_col = old_location[1]
        new_row = new_location[0]
        new_col = new_location[1]

        pill_old_loc = state[old_row][old_col] % 10
        pill_new_loc = state[new_row][new_col] % 10

        if pill_old_loc:
            state[old_row][old_col] = PILL
        else:
            state[old_row][old_col] = EMPTY

        if pill_new_loc:
            state[new_row][new_col] = ghost + 1
        else:
            state[new_row][new_col] = ghost

    def move_ghosts(self, state):
        pacman_location = self.locations[7]
        for ghost in GHOSTS:
            old_location = self.get_ghost_location(state, ghost)
            if old_location is None:
                continue
            action = STAY
            min_manhattan = math.inf
            new_location = []
            for move in MOVES:
                potential_location = calc_new_location(old_location, move)
                if not self.is_legal_location(state, potential_location):
                    continue
                manhattan = manhattan_distance(potential_location, pacman_location)
                if manhattan < min_manhattan:
                    min_manhattan = manhattan
                    action = move
                    new_location = potential_location
            if action != STAY:
                # check if the ghost will eat pacman
                if min_manhattan == 0:
                    self.dead_end = True
                    break
                self.move_ghost(state, old_location, new_location, ghost)

    def result(self, state, move):
        """given state and an action and return a new state"""
        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False
        list_state = tuple_state_to_list(state)
        #pacman_move = self.move_pacman(list_state, move)
        self.move_pacman(list_state, move)
        # todo maybe I can loose the ILLEGAL MOVE and use self.dead_end instead
        if self.dead_end:
            return None
        # if pacman_move == ILLEGAL_MOVE:
        #     return None
        self.move_ghosts(list_state)
        if self.dead_end:
            return None
        return list_state_to_tuple(list_state)

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        for row in state:
            for item in row:
                # if there is pill on the board
                if item % 10 == 1:
                    return False
        return True

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        remaining_pills = 0
        for row in state:
            for item in row:
                if item % 10 == 1:
                    remaining_pills += 1
        return remaining_pills


def create_pacman_problem(game):
    print("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)


game = ()

create_pacman_problem(game)
