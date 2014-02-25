__author__ = 'TurnTheTideTM'
__version__ = 0.1
# For Python 2.7

from collections import namedtuple
from itertools import count
from time import time

initial = list(
    "          " +
    "          " +
    " RNBQKBNR " +
    " PPPPPPPP " +
    " ........ " +
    " ........ " +
    " ........ " +
    " ........ " +
    " pppppppp " +
    " rnbqkbnr " +
    "          " +
    "          ")

A1, H1, A8, H8 = 21, 28, 91, 98

directions = dict(P=(10, 20, 9, 11),
                  N=(-19, -8, 12, 21, 19, 8, -12, -21),
                  B=(-9, 11, 9, -11),
                  R=(-10, 1, 10, -1),
                  Q=(-9, 11, 9, -11, -10, 1, 10, -1),
                  K=(-9, 11, 9, -11, -10, 1, 10, -1),
                  p=(10, 20, 9, 11),
                  n=(-19, -8, 12, 21, 19, 8, -12, -21),
                  b=(-9, 11, 9, -11),
                  r=(-10, 1, 10, -1),
                  q=(-9, 11, 9, -11, -10, 1, 10, -1),
                  k=(-9, 11, 9, -11, -10, 1, 10, -1))

put = lambda board, i, p: board[:i] + p + board[i + 1:]     # adds piece p at position i



class Position(namedtuple('Position', 'board wc bc ep kp')):
    """ A state of a chess game

    board -- a 120 char representation of the board
    wc -- the castling rights
    bc -- the opponent castling rights
    ep -- the en passant square
    kp -- the king passant square
    """

    def gen_moves(self):
        # Search for all possible moves
        # Only works for white pieces, rotate the board and upper/lower case
        # the figurines to search black moves
        
        #derefer all vars that don't change inside the loops
        if not "K" in self.board:
            return
        wc0 = self.wc[0]
        wc1 = self.wc[1]
        piecelist = ((i, p) for i, p in enumerate(self.board) if p.isupper())   # gets all white pieces
        for i, p in piecelist:  # i = position, p = piece
            for d in directions[p]:     # d = directions for piece p
                for j in count(i + d, d):   # generator that counts up/down from i+d until infinity, j = coordinate
                    q = self.board[j]       # checks what's on j
                    if q == ' ': break  # if j is out of the bounds: break
                    if i == A1 and q == 'K' and wc0: yield (j, j - 2)    # if a rook can reach the king
                    if i == H1 and q == 'K' and wc1: yield (j, j + 2)    # and castling is true, castle
                    if q.isupper(): break   # no friendly captures
                    # pawn is not allowed to:
                    if p == 'P':
                        # move diagonally if the target es empty
                        if d in (9, 11) and q == '.' and j not in (self.ep, self.kp): break
                        # move forward if the target is filled
                        if d in (10, 20) and q != '.': break
                        # double step if he's not on the b-row or the square in front is filed
                        if d == 20 and (i > 40 or self.board[j - 10] != '.'): break
                    
                    yield (i, j)    # move!
                    
                    if p in ('P', 'N', 'K'): break  # these are only allowed to single move
                    if q.islower(): break  # stop after capture
    
    def rotate(self):
        # Rotates the board, white becomes black and reverse
        return Position(
            self.board[::-1].swapcase(), self.bc, self.wc, 119 - self.ep, 119 - self.kp)
    
    def move(self, move):
        # Move a piece
        i, j = move     # start and target coordinates of the move
        p, q = self.board[i], self.board[j]     # what is on these positions
        # previous put location
        global put
        board = self.board                          # Copy variables and reset ep and kp
        wc, bc, ep, kp = self.wc, self.bc, 0, 0     # Copy variables and reset ep and kp
        
        board = put(board, j, p)     # do the move
        board = put(board, i, '.')          # do the move
        
        if i == A1: wc = (False, wc[1])     # if A1 rook moves, no long castling
        if i == H1: wc = (wc[0], False)     # if H1 rook moves, no short castling
        if j == A8: bc = (bc[0], False)     # if black rook is captured, no castling
        if j == H8: bc = (False, bc[1])     # if black rook is captured, no castling
        
        if p == 'K':
            wc = (False, False)             # if king moves, no castling any more
            if abs(j - i) == 2:             # if king moves two squares, he's castling
                kp = (i + j) // 2           # the king passant square is between the start and the target
                board = put(board, A1 if j < i else H1, '.')    # A1/H1 are empty
                board = put(board, kp, 'R')                     # the rook moves to the kp position
        
        if p == 'P':    # special pawn rules
            if 90 < j:    # if the pawn reaches the last row, he becomes a queen
                board = put(board, j, 'Q')  # TODO decide what the pawn becomes
            if (j - i) == 20:     # if the pawn double steps, an en passant square is created
                ep = i + 10
        
        return Position(board, wc, bc, ep, kp).rotate()  # the board is rotated for the next player


class PositionUndo():
    """ A state of a chess game

    board -- a 120 char representation of the board
    wc -- the castling rights
    bc -- the opponent castling rights
    ep -- the en passant square
    kp -- the king passant square
    """

    def __init__(self, board, wc, bc, ep, kp):
        self.history = []   # Stores all moves
        self.color = 1      # 1 = White 0 = Black
        self.board = board
        self.wc = wc
        self.bc = bc
        self.ep = ep
        self.kp = kp

    def gen_moves(self):
        # Search for all possible moves
        # Only works for white pieces, rotate the board and upper/lower case
        # the figurines to search black moves

        #derefer all vars that don't change inside the loops
        if not ("K" if self.color else "k") in self.board:
            return
        wc0 = self.wc[0] if self.color else self.bc[0]
        wc1 = self.wc[1] if self.color else self.bc[1]
        if self.color:
            piecelist = ((i, p) for i, p in enumerate(self.board) if p.isupper())   # gets all white pieces
        else:
            piecelist = ((i, p) for i, p in enumerate(self.board) if p.islower())   # gets all black pieces
        for i, p in piecelist:  # i = position, p = piece
            for d in directions[p]:     # d = directions for piece p
                if not self.color:
                    d *= -1
                for j in count(i + d, d):   # generator that counts up/down from i+d until infinity, j = coordinate
                    q = self.board[j]       # checks what's on j
                    if q == ' ': break  # if j is out of the bounds: break
                    if self.color:
                        if i == A1 and q == 'K' and wc0: yield (j, j - 2)    # if a rook can reach the king
                        if i == H1 and q == 'K' and wc1: yield (j, j + 2)    # and castling is true, castle
                        if q.isupper(): break   # no friendly captures
                        # pawn is not allowed to:
                        if p == 'P':
                            # move diagonally if the target es empty
                            if d in (9, 11) and q == '.' and j not in (self.ep, self.kp): break
                            # move forward if the target is filled
                            if d in (10, 20) and q != '.': break
                            # double step if he's not on the b-row or the square in front is filed
                            if d == 20 and (i > 40 or self.board[j - 10] != '.'): break
                    else:
                        if i == A8 and q == 'k' and wc0: yield (j, j - 2)    # if a rook can reach the king
                        if i == H8 and q == 'k' and wc1: yield (j, j + 2)    # and castling is true, castle
                        if q.islower(): break   # no friendly captures
                        # pawn is not allowed to:
                        if p == 'p':
                            # move diagonally if the target es empty
                            if d in (-9, -11) and q == '.' and j not in (self.ep, self.kp): break
                            # move forward if the target is filled
                            if d in (-10, -20) and q != '.': break
                            # double step if he's not on the b-row or the square in front is filed
                            if d == -20 and (i < 40 or self.board[j + 10] != '.'): break

                    yield (i, j)    # move!

                    if p in ('P', 'N', 'K', 'p', 'n', 'k'): break  # these are only allowed to single move
                    if self.color:
                        if q.islower(): break  # stop after capture
                    else:
                        if q.isupper(): break

    def rotate(self):
        # Rotates the board, white becomes black and reverse
        self.board = self.board.swapcase()

        return Position(
            self.board[::-1].swapcase(), self.bc, self.wc, 119 - self.ep, 119 - self.kp)

    def move(self, move):
        # Move a piece
        i, j = move     # start and target coordinates of the move
        p, q = self.board[i], self.board[j]     # what is on these positions

        self.history.append((i, j, p, q, self.wc, self.bc, self.ep, self.kp, self.color))

        # previous put location
        global put
        board = self.board                          # Copy variables and reset ep and kp
        wc, bc, ep, kp = self.wc, self.bc, 0, 0     # Copy variables and reset ep and kp

        board[j] = p
        board[i] = "."

        if i == A1: wc = (False, wc[1])     # if A1 rook moves, no long castling
        if i == H1: wc = (wc[0], False)     # if H1 rook moves, no short castling
        if i == A8: bc = (bc[0], False)
        if i == H8: bc = (False, bc[1])
        if j == A8: bc = (bc[0], False)     # if black rook is captured, no castling
        if j == H8: bc = (False, bc[1])     # if black rook is captured, no castling
        if j == A1: wc = (False, wc[1])
        if j == H1: wc = (wc[0], False)

        if p == 'K':
            wc = (False, False)             # if king moves, no castling any more
            if abs(j - i) == 2:             # if king moves two squares, he's castling
                kp = (i + j) // 2           # the king passant square is between the start and the target
                board[A1 if j < i else H1] = '.'    # A1/H1 are empty
                board[kp] = "R"                     # the rook moves to the kp position

        if p == 'k':
            bc = (False, False)             # if king moves, no castling any more
            if abs(j - i) == 2:             # if king moves two squares, he's castling
                kp = (i + j) // 2           # the king passant square is between the start and the target
                board[H1 if j > i else H8] = '.'    # A1/H1 are empty
                board[kp] = "r"                     # the rook moves to the kp position

        if p == 'P':    # special pawn rules
            if 90 < j:    # if the pawn reaches the last row, he becomes a queen
                board = put(board, j, 'Q')  # TODO decide what the pawn becomes
            if (j - i) == 20:     # if the pawn double steps, an en passant square is created
                ep = i + 10

        if p == "p":
            if 30 > j:    # if the pawn reaches the last row, he becomes a queen
                board[j] = 'Q'      # TODO decide what the pawn becomes
            if (j - i) == -20:      # if the pawn double steps, an en passant square is created
                ep = i - 10

        if self.color == 1: self.color = 0
        else: self.color = 1

    def undo(self):
        i,j,p,q,self.wc,self.bc,self.ep,self.kp, self.color = self.history[-1]
        self.board[i] = p
        self.board[j] = q
        del self.history[-1]

    def render(self, i):
        return chr(i%10 + ord('a') - 1) + str(i//10 - 1)

    def printmoves(self):
        white = 1
        print "-------------"
        temp = 1
        print 1,
        for entry in self.history:
            if entry[2] != "P" and entry[2] != "p":
                print entry[2].upper() + self.render(entry[1]),
            else:
                print self.render(entry[1]),
            if white == 1:
                print "\t",
            else:
                temp += 1
                print
                print temp,
            white *= -1
        print



# make this a generator increases performance by a bit
def next_layer(pos):
    for m in pos.gen_moves():
        yield pos.move(m)

LAYERCOUNT = {}

def layersUndo(field, depth, total):
    if depth > 0:
        n = 0
        for move in field.gen_moves():
            n += 1
            field.move(move)
            layersUndo(field, depth - 1, total)
            # if depth == 1:
            #     field.printmoves()
            field.undo()
        if total - depth + 1 in LAYERCOUNT:
            LAYERCOUNT[total - depth + 1] += n
        else:
            LAYERCOUNT[total - depth + 1] = n


def gengenerators(func, argGen):
    for gen in (func(arg) for arg in argGen):
        for i in gen:
            yield i


if __name__ == '__main__':
    start = time()

    depth = 6

    feld = PositionUndo(initial, (True, True), (True, True), 0, 0)
    layersUndo(feld, depth, depth)

    for i in LAYERCOUNT:
         print "DEPTH:", i, "   MOVES FOUND:", LAYERCOUNT[i]

    # positions = [Position(initial, (True, True), (True, True), 0, 0)]
    # for i in xrange(depth):
    #     temp = []
    #     counter = 0
    #     positions = gengenerators(next_layer, positions)
    #
    # counter = 0
    # for i in positions:
    #     counter += 1
    # print "DEPTH:", depth, "   MOVES FOUND:", counter

    timer = round(time() - start, 2)
    print "Needed", timer, "Seconds to calculate", depth, "Layers."