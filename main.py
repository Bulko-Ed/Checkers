# неправильный победитель 
# дамка может ходить как угодно далеко
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.board import Board
from checkers.game import Game 
from mimimax.algorithm import minimax

FPS = 60    
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dáma') 

def main():
    run = True
    clock = pygame.time.Clock() 
    game = Game(WIN)
    
    while run:

        clock.tick(FPS)

        if game.turn == WHITE:
           value, new_board =  minimax(game.board, 3, WHITE)
           game.ai_move(new_board)
           #game.change_turn() # проверка зачем передавать аи борд

    
        for event in pygame.event.get(): #it check if any of the events have happened
            if event.type == pygame.QUIT: #pokud chceme skoncit hru
                run = False 

            if event.type == pygame.MOUSEBUTTONDOWN: # pokud jsme stisknuli jakekoliv tlacitko na mysi
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                if game.turn == RED:
                    game.select(row, col)
                    #print (game.board.get_valid_moves((game.board.board)[row][col]))



        if game.board.winner() != None:
            if game.board.winner() == RED:
                print ('you won!')
            else:
                print ('you lose')    
            break     
            

        game.update()
    
        
    pygame.quit()             


main()