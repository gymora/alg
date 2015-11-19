from copy import copy
from const import BISHOP, KNIGHT, QUEEN, ROOK, DIRECTIONS, KNIGHT_DIRECTIONS
from const import KING


class Figure(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rook(Figure):
    def is_safe(self, other_x, other_y):
        return self.x != other_x and self.y != other_y

    def calculate_delta(self, other_x, other_y):
        delta_x, delta_y = abs(self.x - other_x), abs(self.y - other_y)
        return delta_x, delta_y


class King(Figure):
    def is_safe(self, other_x, other_y):
        delta_x, delta_y = abs(self.x - other_x), abs(self.y - other_y)
        return delta_x != 0 and delta_y != 0


class Queen(Figure):
    def is_safe(self, other_x, other_y):
        delta_x, delta_y = self.calculate_delta(other_x, other_y)
        return delta_x > 0 and delta_y > 0 and not (delta_x / delta_y == 0 and delta_x % delta_y == 0)


class Bishop(Figure):
    def is_safe(self, other_x, other_y):
        delta_x, delta_y = self.calculate_delta(other_x, other_y)
        return not (delta_x / delta_y == 0 and delta_x % delta_y == 0)


class Knight(Figure):
    def is_safe(self, other_x, other_y):
        delta_x, delta_y = self.calculate_delta(other_x, other_y)
        return not ((delta_x == 1 and delta_y == 2) or (delta_x == 2 and delta_y == 1))


FIGURE_TYPE_MAP = {
    BISHOP: Bishop,
    KING: King,
    KNIGHT: Knight,
    QUEEN: Queen,
    ROOK: Rook,
}


def recursive(board, memory, pieces):
    good_configurations = set()
    for x in range(board.width):
        for y in range(board.height):
            all_empty = True
            for figure_type, figure_num in pieces.iteritems():
                if figure_num > 0:
                    all_empty = False
                    figure = FIGURE_TYPE_MAP[figure_type](x, y)
                    if memory.add_figure_if_never_happened(figure):
                        board.add_figure(figure)
                        remaining_pieces = copy(pieces)
                        remaining_pieces[figure_type] = figure_num - 1

                        good_configurations.union(recursive(board, memory, remaining_pieces))

                        board.remove_figure(figure)
                        memory.forget_if_happened(figure)
            if all_empty:
                good_configurations.add(board.represent())
    return good_configurations




def solve_board(input_problem):
    board = Board(input_problem["board_width"], input_problem["board_height"])
    pieces = input_problem["pieces"]

    memory = Memory()
    return recursive(board, memory, pieces,)


class Memory(object):
    def __init__(self):
        self.memory = {}

    def add_figure_if_never_happened(self, figure):
        figure_type = type(figure)
        figure_positions = self.memory.get(figure_type) or set()
        position = (figure.x, figure.y)
        if position in figure_positions:
            return False
        figure_positions.add((figure.x, figure.y))
        self.memory[figure_type] = figure_positions
        return True

    def forget_if_happened(self, figure):
        figure_type = type(figure)
        figure_positions = self.memory.get(figure_type)
        if figure_positions:
            position = (figure.x, figure.y)
            if position in figure_positions:
                del figure_positions[position]
                return True
        return False


class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.figures_by_x = {}
        self.figures_by_y = {}

    def represent(self):
        {}asasasa
        figure_pairs = [[ ,figure for y, figure in row.iteritems()] for x, row in self.figures_by_x.iteritems()]


    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y <= self.height

    def get_figure_at(self, x, y):
        row = self.figures_by_x.get(x)
        return row.get(y) if row else None

    def remove_figure(self):
        pass

    def is_safe_to_add(self, new_figure):
        if self.get_figure_at(new_figure.x, new_figure.y):
            return False
        for x_direction in DIRECTIONS:
            for y_direction in DIRECTIONS:
                if not x_direction == y_direction == 0:
                    if self._search_for_danger(new_figure, (x_direction, y_direction), 1, True):
                        return False
        for x_direction, y_direction in KNIGHT_DIRECTIONS:
            if self._search_for_danger(new_figure, (x_direction, y_direction), 1, False):
                return False
        return True

    def _search_for_danger(self, new_figure, direction, distance, distance_increment):
        new_x, new_y = self.step(new_figure, direction, distance)
        if self.is_valid_position(new_x, new_y):
            other_figure = self.get_figure_at(new_x, new_y)
            if other_figure:
                # is this figure dangerous or not
                return not (other_figure.is_safe(new_figure.x, new_figure.y) and new_figure.is_safe(new_x, new_y))
            else:
                # no figure there -> go further
                if distance_increment:
                    return self._search_for_danger(new_figure, direction, distance + 1)
                else:
                    # if not going further it is safe
                    return False
        else:
            # we are out of the board -> nobody can hit us
            return False


    @staticmethod
    def step(new_figure, direction, distance):
        return new_figure.x + distance * direction[0], new_figure.y + distance * direction[1]

    def add_figure(self, figure):
        row = self.figures_by_x.get(figure.x) or {}
        row[figure.y] = figure
        self.figures_by_x[figure.x] = row


