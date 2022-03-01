import pygame

from .constants import  RED, SQUARE_SIZE, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}  
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()  



    def select(self, row, col):
        if self.selected: # pokud jsme předem už vybrali nějaký kámen a chceme ho posunout
            result = self._move(row, col) # try to move it to row, col
            self.selected = None 

            if not result: 
                self.select(row,col) # bude fungovat, pokud jsme rozhodli vybrat jiný kámen
            
        else:
            piece = self.board.get_piece(row, col) #vybírame kámen proto, abychom ho pak posunuli
            if piece != 0 and piece.color == self.turn: 
                self.selected = piece 
                self.valid_moves = self.board.get_valid_moves(piece)   
          


    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()  
            return True  
        
        return False

    def draw_valid_moves(self, moves):
        for move in moves: #moves - dictionary, it will look through all the keys in dictionary 
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)


    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED    

    
    def ai_move(self, board):
        self.board = board
        self.change_turn()    


          