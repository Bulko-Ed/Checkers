import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE #. from the same package 
from .piece import Piece
class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

        
                    # where to draw, what color, x, y, height, width
    
    def evaluate(self):
        return self.white_left - self.red_left + self.white_kings - self.red_kings     


    def get_all_pieces(self, color): 
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces            


    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if not piece.king and (row == ROWS - 1 or row == 0):
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self): # vnější seznam – řádky, vnitřní – sloupce
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
       
    def draw(self, win): # where do we use that??
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range (row % 2, COLS, 2):
                    pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self): #Выигрывает та сторона, которой удалось уничтожить или заблокировать движение всех шашек противника
        if self.red_left == 0:
            return WHITE

        if self.white_left == 0:
            return RED 

        elif self.red_left != 0:
            red_pieces = self.get_all_pieces(RED)
            possible_moves = []
            for piece in red_pieces:
                possible_moves.append(self.get_valid_moves(piece))
                if possible_moves != []:
                    break
            else:
                return WHITE  

        elif self.white_left != 0:   
            white_pieces = self.get_all_pieces(WHITE)
            possible_moves = []
            for piece in white_pieces:
                possible_moves.append(self.get_valid_moves(piece))
                if possible_moves != []:
                    break
            else:
                return RED   
        
        return None 

    def get_valid_moves(self, piece):
        moves = {} 
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king: #why such a strange condition
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left)) # we are giving a function row - 1 in order to check the current, left etc
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))

            # row - 1 = если мы красные, нужно подняться на один ряд вверх
            # max(row-3, -1) = how far up are we going to look, how many rows up am i looking
            # -1 both in left trverse right and left, because for red ones we are decreasing their row
            # max(row-3, -1) part - мы используем это в r in range 9 (strart, stop), до стопа не доходим, то есть на нужно или -1 или ряд - 3,
            # из-за того, что это красные, мы идем от большего к меньшему используя грубо говоря for i in range (10, 1, -1), 
            # остановимся мы или на нуле включая, если ряд например 1, потому что большей будет -1, или на опред. ряду, если он не слишком маленький    

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):

        # skipped - we are going to call this method recursively, have we skipped any pieces yet?
        # if we have, we can only move two squares when we skip another piece 
        moves = {}
        last = []
        for r in range(start, stop, step): # r - row
            if left < 0:   
                break
            
            current = self.board[r][left] 
            if current == 0:
                if skipped and not last: # мы перепрыгнули одного противника, и дальше ходить нельзя, нет других его шашек
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped # когда мы уже прыгали, но остались еще шашки, через которые можно преепрыгнуть (возможно)
                else:
                    moves[(r, left)] = last # когда мы еще не ходили, и нет через кого можно перепрыгнуть или перепрыгнули через одну
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                    
                break # если это пустое поле, мы по любому останавливаемся в конце

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1
        
        return moves
