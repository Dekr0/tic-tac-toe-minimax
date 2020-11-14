from math import inf
from random import choice
from random import seed


class Interface(object):

    def __init__(self):
        self.type = str(self.__class__)

    def __new__(cls, *args, **kwargs):
        """
        Singleton, class Board and Event only have one instance each time
        the game run
        :param args:
        :param kwargs:
        """
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __str__(self):
        return self.type

    def __repr__(self):
        s = "<%d> %s" % (id(self), self.type)
        return s


class Board(Interface):

    def __init__(self):
        super().__init__()

        row = 3
        col = 3

        self.board = (row, col)

    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :return: a list of empty cells
        """
        empty_cells = []

        for row in self.board:
            for cell in row:
                if cell.state == State.EMPTY:
                    empty_cells.append(cell)

        return empty_cells

    def evaluate(self):
        """
        Function to heuristic evaluation of state.
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(State.COMP):
            score = +1
        elif self.wins(State.HUMAN):
            score = -1
        else:
            score = 0

        return score

    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.valid_move(x, y):
            self.board[x][y].state = player
            return True
        else:
            return False

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if self.board[x][y] in self.empty_cells():
            return True
        else:
            return False

    def wins(self, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [self.board[0][0].state, self.board[0][1].state, self.board[0][2].state],
            [self.board[1][0].state, self.board[1][1].state, self.board[1][2].state],
            [self.board[2][0].state, self.board[2][1].state, self.board[2][2].state],
            [self.board[0][0].state, self.board[1][0].state, self.board[2][0].state],
            [self.board[0][1].state, self.board[1][1].state, self.board[2][1].state],
            [self.board[0][2].state, self.board[1][2].state, self.board[2][2].state],
            [self.board[0][0].state, self.board[1][1].state, self.board[2][2].state],
            [self.board[2][0].state, self.board[1][1].state, self.board[0][2].state],
        ]

        if [player, player, player] in win_state:
            return True
        else:
            return False

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, size):
        r, c = size
        self.__board = []
        for x in range(r):
            row = []
            for y in range(c):
                row.append(State(x, y, State.EMPTY))
            self.__board.append(row)


class Event(Interface):

    def __init__(self):
        super().__init__()

        self.h_choice = ""
        self.c_choice = ""
        self.first = ""

    def ai_turn(self):
        """
        The Human plays choosing a valid move.
        :return:
        """
        depth = len(self.board.empty_cells())
        if depth == 0 or self.game_over():
            return

        print()
        print(f'Computer turn [{self.c_choice}]')
        self.render()

        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax(depth, State.COMP)
            x, y = move[0], move[1]

        self.board.set_move(x, y, State.COMP)

    def game_over(self):
        """
        This function test if the human or computer wins
        :return: True if the human or computer wins
        """
        return self.board.wins(State.HUMAN) or self.board.wins(State.COMP)
    
    def game_over_msg(self):
        """
        Game over message
        :return:
        """
        if self.board.wins(State.HUMAN):
            print()
            print(f'Human turn [{self.h_choice}]')
            self.render()
            print('YOU WIN!')
        elif self.board.wins(State.COMP):
            print()
            print(f'Computer turn [{self.c_choice}]')
            self.render()
            print('YOU LOSE!')
        else:
            print()
            self.render()
            print('DRAW!')

    def handle(self):
        """
        Main loop of this game
        :return:
        """
        while len(self.board.empty_cells()) > 0 and not self.game_over():
            if self.first == 'N':
                self.ai_turn()
                self.first = ''

            self.human_turn()
            self.ai_turn()

    def human_turn(self):
        """
        The Human plays choosing a valid move.
        :return:
        """
        depth = len(self.board.empty_cells())
        if depth == 0 or self.game_over():
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        print()
        print(f'Human turn [{self.h_choice}]')
        self.render()

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.board.set_move(coord[0], coord[1], State.HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == State.COMP:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]

        if depth == 0 or self.game_over():
            score = self.board.evaluate()
            return [-1, -1, score]

        for cell in self.board.empty_cells():
            x, y = cell.coordinate
            self.board.board[x][y].state = player
            score = self.minimax(depth - 1, -player)
            self.board.board[x][y].state = 0
            score[0], score[1] = x, y

            if player == State.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def pick_choice(self):
        """
        Loop of picking choice
        :return:
        """
        while self.h_choice != "O" and self.h_choice != "X":
            try:
                print("")
                self.h_choice = input("Choose X or O\nChosen: ").upper()
            except (EOFError, KeyboardInterrupt):
                print("Bye")
                exit()
            except (KeyError, ValueError):
                print("Bad choice")

        if self.h_choice == "X":
            self.c_choice = "O"
        else:
            self.c_choice = "X"
        print()

    def pick_first(self):
        """
        Loop of picking first to start
        :return:
        """
        while self.first != 'Y' and self.first != 'N':
            try:
                self.first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

    def render(self):
        """
        Print the board on console
        """
        str_line = '---------------'

        print('\n' + str_line)
        for row in self.board.board:
            for cell in row:
                symbol = self.chars[cell.state]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)

    def run(self):
        """
        Main process of the game
        :return:
        """
        seed(274 + 2020)
        print()

        self.pick_choice()
        self.pick_first()

        self.chars = {
            State.HUMAN: self.h_choice,
            State.COMP: self.c_choice,
            State.EMPTY: " "
        }
        self.board = Board()

        self.handle()
        self.game_over_msg()


class State(Interface):
    HUMAN = -1
    COMP = +1
    EMPTY = 0

    def __init__(self, x, y, state):
        super().__init__()

        self.coordinate = (x, y)
        self.state = state

    def __new__(cls, *args, **kwargs):
        pass

    @property
    def coordinate(self):
        return self.__coordinate

    @coordinate.setter
    def coordinate(self, coord):
        self.__coordinate = coord

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, cstate):
        self.__state = cstate


def main():
    """
    main function that calls all functions
    """
    event = Event()
    event.run()
    exit()


if __name__ == "__main__":
    main()
