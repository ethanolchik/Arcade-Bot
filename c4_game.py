from typing import Union
from itertools import groupby, chain


class Board(list):
    __slots__ = frozenset({"width", "height"})

    # board initialization func.
    def __init__(self, width, height, player1_name=None, player2_name=None):
        self.width = width # set the board width to the given width.
        self.height = height # set the board height to the given height
        [self.append([0] * height) for x in range(width)] # <| found this on stack overflow, idek what this does.

    # yay, a getter.
    def __getitem__(self, pos: Union[int, tuple]):
        if isinstance(pos, int):
            return list(self)[pos]
        elif isinstance(pos, tuple):
            x, y = pos
            return list(self)[x][y]
        else:
            raise TypeError('Variable "pos" must be of type int or tuple')

    # yay, a setter.
    def __setitem__(self, pos: Union[int, tuple], new_value):
        x, y = self._xy(pos)

        if self[x, y] != 0:
            raise IndexError("there's already a move at that position")

        self[x][y] = new_value

    # get the `x` and `y` axes.
    def _xy(self, pos):
        if isinstance(pos, tuple):
            return pos[0], pos[1]
        elif isinstance(pos, int):
            x = pos
            return x, self._y(x)
        else:
            raise TypeError('Variable "pos" must be of type int or tuple')

    # check the `y` axis.
    def _y(self, x):
        for y in range(self.height - 1, -1, -1):
            if self[x, y] == 0:
                return y
        raise ValueError("Looks like that column is full!")

    # check the diagonal positions.
    def _pos_diagonals(self):
        for di in (
            [(j, i - j) for j in range(self.width)]
            for i in range(self.width + self.height - 1)
        ):
            yield [
                self[i, j]
                for i, j in di
                if i >= 0 and j >= 0 and i < self.width and j < self.height
            ]

    # 
    def _neg_diagonals(self):
        for di in (
            [(j, i - self.width + j + 1) for j in range(self.height)]
            for i in range(self.width + self.height - 1)
        ):
            yield [
                self[i, j]
                for i, j in di
                if i >= 0 and j >= 0 and i < self.width and j < self.height
            ]

    # 
    def _full(self):
        for x in range(self.width):
            if self[x, 0] == 0:
                return False
        return True


# the actual game
class Connect4Game:
    __slots__ = frozenset({"board", "turn_count", "_whomst_forfeited", "names"})

    FORFEIT = -2
    TIE = -1
    NO_WINNER = 0

    PIECES = "⬛" "\N{large red circle}" "\N{large blue circle}" # game pieces.

    # initialize all the things we need to get this thing going.
    def __init__(self, player1_name=None, player2_name=None):
        if player1_name is not None and player2_name is not None:
            self.names = (player1_name, player2_name)
        else:
            self.names = ("Player 1", "Player 2")

        self.board = Board(7, 6)
        self.turn_count = 0
        self._whomst_forfeited = 0

    # move func. we use this to put a piece in a certain column.
    def move(self, column):
        self.board[column] = self.get_turn()
        self.turn_count += 1

    # forfeit func. we use this to end the game and return the current player.
    # the current player is the forfeiter and therefore making the other player the winner.
    def forfeit(self):
        self._whomst_forfeited = self.get_cur_plr_name()

    # forfeit status func. the name speaks for itself so im not gonna really explain this.
    def _get_forfeit_status(self):
        if self._whomst_forfeited:
            status = "{} has forfeited, making {} the Winner!\n"

            return status.format(self.get_cur_plr_name(), self.get_plr2_name())

        raise ValueError("Nobody has forfeited")
    
    # format this class so we can use this in the embed
    def __str__(self):
        win_status = self.get_winner()
        status = self._get_status()
        instructions = ""

        if win_status == self.NO_WINNER:
            instructions = self._get_instructions()
        elif win_status == self.FORFEIT:
            status = self._get_forfeit_status()

        return (
            status
            + instructions
            + "\n".join(self._format_row(y) for y in range(self.board.height))
        )

    # get status func. this also speaks for itself, not gonna explain this one either. sorry :p.
    def _get_status(self):
        win_status = self.get_winner()

        if win_status == self.NO_WINNER:
            status = self.get_cur_plr_name() + "'s turn" + self.PIECES[self.get_turn()]
        elif win_status == self.TIE:
            status = "It's a tie!"
        elif win_status == self.FORFEIT:
            status = self._get_forfeit_status()
        else:
            status = self._get_player_name(win_status) + " won!"
        return status + "\n"

    # you know what, this one is also not hard to undersand.
    def _get_instructions(self):
        instructions = ""
        for i in range(1, self.board.width + 1):
            instructions += str(i) + "\N{combining enclosing keycap}"
        return instructions + "\n"

    # yeah. this one is simple as f.
    # btw sorry im not explaining alot of these, im just doing it asap so i will have time to submit.
    def _format_row(self, y):
        return "".join(self[x, y] for x in range(self.board.width))

    # another getter
    def __getitem__(self, pos):
        x, y = pos
        return self.PIECES[self.board[x, y]]

    # get_winner func. here, we return the player,
    # a forfeit status, a tie status or a no_winner status.
    def get_winner(self):
        lines = (
            self.board,
            zip(*self.board),
            self.board._pos_diagonals(),
            self.board._neg_diagonals(),
        )

        if self._whomst_forfeited:
            return self.FORFEIT

        for line in chain(*lines):
            for player, group in groupby(line):
                if player != 0 and len(list(group)) >= 4:
                    return player

        if self.board._full():
            return self.TIE
        else:
            return self.NO_WINNER

    # speaks for itself...
    def get_plr2_name(self):
        self.turn_count += 1
        other_player_name = self.get_cur_plr_name()
        self.turn_count -= 1
        return other_player_name

    # speaks for itself...
    def get_cur_plr_name(self):
        return self._get_player_name(self.get_turn())

    # speaks for itself...
    def get_turn(self):
        return self.turn_count % 2 + 1

    # speaks for itself...
    def _get_player_name(self, player_number):
        player_number -= 1

        return self.names[player_number]
