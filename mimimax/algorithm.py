from copy import deepcopy
import pygame
from checkers.board import Board
from checkers.constants import RED, WHITE

def minimax(position: Board, depth, max_player): #position - board with certain position 
    # max_player - boolean, are we minimazing or maximazing the value 
    
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(position, WHITE)  # seznam desek s moznymi pozici
        for move in moves:
            evaluation = minimax(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move

    else:
        minEval = float('+inf')
        best_move = None
        moves = get_all_moves(position, RED)
        for move in moves:
            evaluation = minimax(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color): 
    moves = [] 
    pieces = board.get_all_pieces(color)
    for piece in pieces:
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board) # i dont wont to modify the same board, the next piece has a fresh board 
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    
    return moves # board with possible moves on it


