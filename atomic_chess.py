# Author: Bryce Worley
# GitHub username: Bryce-Worley
# Date: 6/7/2024
# Description:  A program that allows the user to play console Atomic Chess against another local human player.
#       Program defines three classes: ChessVar, Board, and Piece (Piece serves as parent to several subclasses).
#       ChessVar largely defines methods that control the rules of the game. Board keeps track of the various
#       pieces on the board throughout play. Piece and it's subclasses define the allowed movement for chess pieces.

class ChessVar:
    """
    ChessVar class represents an Atomic Chess game played by two players.  It is responsible for establishing the game
    start, tracking the game state, moves made, verifying legal moves, and keeping track of turns.

    It will communicate with the Board, Player, and Pieces classes.  This is so that it can know the board lay out at a
    given turn, which player should move, and whether a move made by a piece is valid or not.
    """

    def __init__(self):
        """
        Constructor for ChessVar class. Takes no parameters.
        Initializes board, and initial setup of pieces and tracking of turns
        """
        self._board = Board()
        self._turns = 1

    def print_board(self):
        """
        Calls method in Board class to get current state
        :return: Unicode representation of chess board and game
        """
        print("         BLACK")
        print("  a　b　c　d　e　f　g　h")
        for i in range(8):
            print(str(8-i)+'|', end='')
            for j in range(8):
                if self._board.get_board()[i][j] is not None:
                    print(str(self._board.get_board()[i][j]) + ' |', end='')
                else:
                    print(chr(12288) + '|', end='')
            print(str(8-i))
        print("  a　b　c　d　e　f　g　h")
        print("         WHITE")

    def make_move(self, current_xy, finishing_xy):
        """
        Allows a specified player to move a Piece when given a valid starting location and ending position.
        Returns update position for Piece of object and updates turn-tracker for valid move.  Returns False for invalid
        moves.
        :param current_xy: Will be used to get Piece object information
        :param finishing_xy: Will determine valid moves for a Piece specified by current_xy
        """
        # converting user input str to int for indexing into matrix
        pos = [char for char in current_xy.lower()]
        mov = [char for char in finishing_xy.lower()]
        x1 = ord(pos[0])-97
        y1 = 8-int(pos[1])
        x2 = ord(mov[0])-97
        y2 = 8-int(mov[1])
        # Validating specified moves
        if 7 < x1 or x1 < 0 or 7 < x2 or x2 < 0 or 7 < y1 or y1 < 0 or 7 < y2 or y2 < 0:  # Verifying move is in bounds
            return False
        elif (self.get_game_state() is False or self.get_game_state() == 'WHITE_WON'  # Verifying game is 'UNFINISHED'
              or self.get_game_state() == 'BLACK_WON'):
            return False
        elif pos == mov:  # Verifying user input unique current_xy and finishing_xy values
            return False
        elif self._board.get_board()[y1][x1] is not None:  # Verifying current_xy specifies a Piece
            # Store values of specified elements in matrix in local variables to restore matrix if needed
            played_piece = self._board.get_board()[y1][x1]
            taken_piece = self._board.get_board()[y2][x2]
            if self._board.get_board()[y1][x1].move_rules(x1, x2, y1, y2, self._board) is True:
                # Check whose turn it is:
                turn = self.get_turns()
                if turn % 2 != 0:  # Odd count is White's turn
                    if self._board.get_board()[y1][x1].get_color() == 'WHITE':
                        # code to reassign value in matrix if moving into an empty space
                        if self._board.get_board()[y2][x2] is None:
                            self._board.get_board()[y2][x2] = self._board.get_board()[y1][x1]
                            self._board.get_board()[y1][x1] = None
                        # code to reassign value in matrix if capturing a piece
                        else:
                            self._board.get_board()[y1][x1] = None
                            self._board.captured_piece(x2, y2)  # Explosion
                        if self.get_game_state():  # Verifies both Kings are not taken
                            self._turns += 1
                            return True
                        else:  # Restore board if both Kings would've been taken
                            self._board.get_board()[y1][x1] = played_piece
                            self._board.get_board()[y2][x2] = taken_piece
                            return False
                    else:
                        return False
                else:  # Even count is Black's turn
                    if self._board.get_board()[y1][x1].get_color() == 'BLACK':
                        # code to reassign value in matrix (see above block of code for details)
                        if self._board.get_board()[y2][x2] is None:
                            self._board.get_board()[y2][x2] = self._board.get_board()[y1][x1]
                            self._board.get_board()[y1][x1] = None
                        else:
                            self._board.get_board()[y1][x1] = None
                            self._board.captured_piece(x2, y2)
                        if self.get_game_state():
                            self._turns += 1
                            return True
                        else:
                            self._board.get_board()[y1][x1] = played_piece
                            self._board.get_board()[y2][x2] = taken_piece
                            return False
                    else:
                        return False
            else:
                return False
        else:
            return False

    def get_game_state(self):
        """
        Takes no parameters. Checks for existence of Player's Piece 'King' and returns one of three strings:
        'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        """
        # Iterates through matrix and append Kings to list
        kings_left = []
        for i in range(8):
            for j in range(8):
                if type(self._board.get_board()[i][j]) is King:
                    kings_left.append(self._board.get_board()[i][j])
        if len(kings_left) == 2:
            return 'UNFINISHED'
        elif 0 < len(kings_left) < 2:
            if kings_left[0].get_color == 'WHITE':
                return 'WHITE_WON'
            else:
                return 'BLACK_WON'
        else:
            return False

    def get_turns(self):
        """Returns turns count"""
        return self._turns


class Board:
    """
    Represents a standard chessboard utilizing algebraic notation and ASCII characters for a visual output.
    It is responsible for tracking the layout, and boundaries for Piece objects. It also tracks current Piece positions.

    It will communicate with ChessVar and Pieces.  Board object will update whenever ChessVar calls make_move,
    and it will print ASCII representation whenever ChessVar calls print_board.
    It will also be used by Piece class when determining validity of moves.
    """

    def __init__(self):
        """
        Constructor for Board class.  Takes no parameter
        Initializes lay out and set up of pieces at start of game.
        """
        # Initialize a matrix representation of a chessboard
        self._chess_board = [[None for x in range(8)] for y in range(8)]
        # Populate 2d Array with Pieces in initial starting positions
        # Pawns
        for i in range(8):
            self._chess_board[1][i] = Pawn('BLACK')
            self._chess_board[6][i] = Pawn('WHITE')
        # Rooks
        self._chess_board[0][0] = Rook('BLACK')
        self._chess_board[0][7] = Rook('BLACK')
        self._chess_board[7][0] = Rook('WHITE')
        self._chess_board[7][7] = Rook('WHITE')
        # Knights
        self._chess_board[0][1] = Knight('BLACK')
        self._chess_board[0][6] = Knight('BLACK')
        self._chess_board[7][1] = Knight('WHITE')
        self._chess_board[7][6] = Knight('WHITE')
        # Bishops
        self._chess_board[0][2] = Bishop('BLACK')
        self._chess_board[0][5] = Bishop('BLACK')
        self._chess_board[7][2] = Bishop('WHITE')
        self._chess_board[7][5] = Bishop('WHITE')
        # Queens
        self._chess_board[0][3] = Queen('BLACK')
        self._chess_board[7][3] = Queen('WHITE')
        # Kings
        self._chess_board[0][4] = King('BLACK')
        self._chess_board[7][4] = King('WHITE')

    def get_board(self):
        """Returns Matrix of chess_board"""
        return self._chess_board

    def captured_piece(self, x, y):
        """
        If make_move sets a Piece finishing_xy on top of an occupied position, then this method will check for
        non-pawn Pieces in the perimeter around the xy coordinates provided and remove them from the matrix
        """
        self.get_board()[y][x] = None
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i > 7 or i < 0 or j > 7 or j < 0:  # ignores out of bounds indexes
                    continue
                elif type(self.get_board()[i][j]) is not Pawn:
                    self.get_board()[i][j] = None


class Piece:
    """
    Represents a Chess game piece. It is responsible for defining each piece on the board, their legal moves, and color
    It will communicate with ChessVar and Board classes to communicate possible moves for pieces, and positions.
    """
    def __init__(self, color):
        """
        Constructor for Piece class. Acts as parent class to the subclass of various pieces. Takes one parameter:
        :param color: 'black', 'white'
        """
        self._color = color
        self._name = None

    def __str__(self):
        """Returns unicode chess symbol"""
        return self._name

    def get_color(self):
        """Returns color"""
        return self._color

    def vertical_moves(self, x1, x2, y1, y2, board):
        """Defines vertical movement common to Queens and Rooks"""
        # Vertical moves
        if x1 == x2:
            # "Upward" movement
            if y1-y2 > 0:
                for i in range(y1-y2-1):
                    if board.get_board()[y1-i-1][x1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
            # "Downward" movement
            elif y1-y2 < 0:
                for i in range(y2-y1-1):
                    if board.get_board()[y1+i+1][x1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
        else:
            return False

    def horizontal_moves(self, x1, x2, y1, y2, board):
        """Defines horizontal movement common to Queens and Rooks"""
        # Horizontal moves
        if y1 == y2:
            # "Leftward" movement
            if x1-x2 > 0:
                for i in range(x1-x2-1):
                    if board.get_board()[y1][x1-i-1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
            # "Rightward" movement
            elif x1-x2 < 0:
                for i in range(x2-x1-1):
                    if board.get_board()[y1][x1+i+1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
        else:
            return False

    def diagonal_moves(self, x1, x2, y1, y2, board):
        """Defines diagonal movement common to Queens and Bishops"""
        if abs(x1-x2) == abs(y1-y2):
            # Upward rightward move
            if y1 - y2 > 0 > x1 - x2:
                for i in range(abs(x1-x2)-1):
                    if board.get_board()[y1-i-1][x1+i+1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
            # Upward leftward move
            if y1 - y2 > 0 > x2 - x1:
                for i in range(abs(x1-x2)-1):
                    if board.get_board()[y1-i-1][x1-i-1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
            # Downward leftward move
            if y2 - y1 > 0 > x2 - x1:
                for i in range(abs(x1-x2)-1):
                    if board.get_board()[y1+i+1][x1-i-1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
            # Downward rightward move
            if y2 - y1 > 0 > x1 - x2:
                for i in range(abs(x1-x2)-1):
                    if board.get_board()[y1+i+1][x1+i+1] is None:
                        continue
                    else:
                        return False
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
        else:
            return False


# Sub-classes for pieces
class King(Piece):
    """
    King is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2654, Black: 265A
        if color == 'BLACK':
            self._name = chr(9818)
        else:
            self._name = chr(9812)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for King Pieces
        """
        if abs(x1-x2) == 1 or abs(x1-x2) == 0:
            if abs(y1 - y2) == 1 or abs(y1 - y2) == 0:
                if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                    return True
        else:
            return False


class Queen(Piece):
    """
    Queen is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2655, Black: 265B
        if color == 'BLACK':
            self._name = chr(9819)
        else:
            self._name = chr(9813)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for Queen Pieces
        """
        if self.vertical_moves(x1, x2, y1, y2, board):
            return self.vertical_moves(x1, x2, y1, y2, board)
        elif self.horizontal_moves(x1, x2, y1, y2, board):
            return self.horizontal_moves(x1, x2, y1, y2, board)
        else:
            return self.diagonal_moves(x1, x2, y1, y2, board)


class Bishop(Piece):
    """
    Bishop is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2657, Black: 265D
        if color == 'BLACK':
            self._name = chr(9821)
        else:
            self._name = chr(9815)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for Bishop Pieces
        """
        return self.diagonal_moves(x1, x2, y1, y2, board)


class Knight(Piece):
    """
    Knight is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2658, Black: 265E
        if color == 'BLACK':
            self._name = chr(9822)
        else:
            self._name = chr(9816)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for Knight Pieces
        """
        if (abs(x1-x2) == 1 and abs(y1-y2) == 2) or (abs(x1-x2) == 2 and abs(y1-y2) == 1):
            if board.get_board()[y2][x2] is None or board.get_board()[y2][x2].get_color() != self.get_color():
                return True
        else:
            return False


class Rook(Piece):
    """
    Rook is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2656, Black: 265C
        if color == 'BLACK':
            self._name = chr(9820)
        else:
            self._name = chr(9814)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for Rook Pieces
        """
        if self.vertical_moves(x1, x2, y1, y2, board):
            return self.vertical_moves(x1, x2, y1, y2, board)
        else:
            return self.horizontal_moves(x1, x2, y1, y2, board)


class Pawn(Piece):
    """
    Pawn is-a Piece
    """
    def __init__(self, color):
        super().__init__(color)  # White unicode: 2659, Black: 265F
        if color == 'BLACK':
            self._name = chr(9823)
        else:
            self._name = chr(9817)

    def move_rules(self, x1, x2, y1, y2, board):
        """
        Defines the rules of movement for Pawn Pieces
        """
        # Black Moves
        if self._color == 'BLACK':
            # Vertical move
            if x1 == x2:
                # Opening moves
                if y1 == 1 and board.get_board()[y1+1][x2] is None and board.get_board()[y1+2][x2] is None:
                    if y1 + 1 == y2 or y1 + 2 == y2:
                        return True
                # Not opening moves
                elif y1 + 1 == y2 and board.get_board()[y2][x2] is None:
                    return True
                else:
                    return False
            # Diagonal Moves
            elif (abs(x1 - x2) == 1 and y1 + 1 == y2 and board.get_board()[y2][x2] is not None
                  and board.get_board()[y2][x2].get_color() == 'WHITE'):
                return True
            else:
                return False

        # White Moves
        elif self._color == 'WHITE':
            # Vertical move
            if x1 == x2:
                # Opening moves
                if y1 == 6 and board.get_board()[y1-1][x2] is None and board.get_board()[y1-2][x2] is None:
                    if y1 - 1 == y2 or y1 - 2 == y2:
                        return True
                # Not opening moves
                elif y1 - 1 == y2 and board.get_board()[y2][x2] is None:
                    return True
                else:
                    return False
            # Diagonal Moves
            elif (abs(x1 - x2) == 1 and y1 - 1 == y2 and board.get_board()[y2][x2] is not None
                  and board.get_board()[y2][x2].get_color() == 'BLACK'):
                return True
            else:
                return False


def main():
    game = ChessVar()
    while game.get_game_state() == 'UNFINISHED' or finishing_xy == 'q':
        game.print_board()
        if game.get_turns() % 2 == 0:
            player = "Black's"
        else:
            player = "White's"
        current_xy = input(f'It is {player} turn. Please enter the position of the piece you would like to move: ')
        finishing_xy = input("Please enter where you would like to move to, or enter 'q' to quit: ")
        if finishing_xy == 'q':
            break
        game.make_move(current_xy, finishing_xy)
    print(game.get_game_state())  # output UNFINISHED


if __name__ == '__main__':
    main()