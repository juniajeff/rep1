import sys #for quitting the application
import copy
import random
import pygame
import numpy as np
from pygame import mixer

from ttt1 import * #importing things from ttt1 file

#pygamecode and set up
pygame.init() #initializig pygame module
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #setting up the screen - width and height
pygame.display.set_caption("Tic Tac Toe game with minimax")
screen.fill(BACKCOLOR) #filling in the screen with a background colors
mixer.init()

font = pygame.font.Font('freesansbold.ttf', 64)
font2 = pygame.font.SysFont('comicsans', 50)
def over_text_show():
    pygame.display.update()
    pygame.time.delay(2000)
    text = font.render("GAME OVER", True, (255,255,255))
    text2 = font2.render("press r to restart", True, (255,255,255))
    text_rect = text.get_rect()
    text2_rect = text2.get_rect()
    text_rect.centerx = round(WIDTH/2)
    text2_rect.centerx = round(WIDTH/2)
    text_rect.y = 250
    text2_rect.y = 350
    screen.fill((100,150,255))
    screen.blit(text, text_rect)
    screen.blit(text2, text2_rect)
    pygame.display.flip()


class Board:

    def __init__(self): #2 dimensional array of 0-s
        self.squares = np.zeros( (ROWS, COLS) ) #parameters as tuple with 0-s, making empty squares
        #self.mark_squares(1, 2, 3) #for testing
        #print(self.squares) #return 0-s in terminal
        self.empty_list = self.squares #list of squares
        self.marked_square = 0  #state of a square

    def final_condition(self, show=False):
        #returning 0 if there is no win till now(not a draw condition), if player 1 wins - then returns 1; if player 2 wins returns 2
        #vertical winning situation
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE if self.squares[0][col] == 2 else CROSS
                    start_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    final_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
                    over = mixer.Sound('game_over.wav')
                    over.play()
                    over_text_show()
                return self.squares[0][col] #return any of column from previous if stat
        #horizontal winning situation
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE if self.squares[row][0] == 2 else CROSS
                    start_pos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    final_pos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, start_pos, final_pos, LINE_WIDTH)
                    over = mixer.Sound('game_over.wav')
                    over.play()
                    over_text_show()
                return self.squares[row][0]

        #going down diagonal winning situation
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE if self.squares[1][1] == 2 else CROSS
                start_pos = (20, 20)
                final_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, start_pos, final_pos, CROSS_WIDTH)
                over = mixer.Sound('game_over.wav')
                over.play()
                over_text_show()
            return self.squares[1][1] #11 is a common square between 2 diagonals so it's returning this one
        #going up diagonal winning situation
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE if self.squares[1][1] == 2 else CROSS
                start_pos = (20, HEIGHT - 20)
                final_pos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, start_pos, final_pos, CROSS_WIDTH)
                over = mixer.Sound('game_over.wav')
                over.play()
                over_text_show()
            return self.squares[1][1]
        
        return 0 #no winning yet

    def mark_squares(self, row, col, player): #for 2 players, one will be marked and zeros in tuple will be replaced in a square that was marked by a player with a player
        self.squares[row][col] = player
        #ach time square is marked it's gonna be increased by one
        self.marked_square += 1

    def empty_square(self, row, col): #checking if the square is empy or not
        return self.squares[row][col] == 0  #if return True than it's empty, if False than bot empty

    def get_empty(self):
        #square that is needed to be deleted from the empty squares
        empty_list = []
        for row in range(ROWS):
            for col in range(COLS): #2 dimentional array(matrix)
                #print( type(self.empty_square) ) testing
                if self.empty_square(row, col):
                    empty_list.append((row, col))
        return empty_list

    def isfull(self):
        return self.marked_square == 9 #max amount of squares when the board is full
    def isempty(self):
        return self.marked_square == 0 #return if the square is marked

class MinMax:
    def __init__(self, level=1, player=2): #level 0 is random ai and level 1 is minimax
        self.level = level #level of game inside of init method
        self.player = player #there are 2 players

    def random_choice(self, board): #random choice function, same as main board
        empty_list = board.get_empty() #getting list of empty squares - row, col part of matrix
        index = random.randrange(0, len(empty_list)) #gets random index and returns from 0 to len of empty squares in the position of the index

        return empty_list[index] #row and col

    def minmax(self, board, max):
        #checking terminal case
        case = board.final_condition() #case
        #player 1 wins
        if case == 1:
            return 1, None #evaluation, move

        #player 2 wins
        if case == 2:
            return -1, None
        #draw 
        elif board.isfull():
            return 0, None
        #coding the algorythm
        if max: #if player is maximizing
            max_eval = -100 #minimal eva;uation that player gets from a specific board
            best_move = None
            empty_list = board.get_empty()
            #loop each square inside of the list of empty squares
            for(row, col) in empty_list:
                temp_board = copy.deepcopy(board) #copying the board for testing on other boards
                temp_board.mark_squares(row, col, 1)#marking the square to a copy, not to the main board
                eval = self.minmax(temp_board, False)[0] #it's true because of changing the player, first position is an . move is row and col that is leading to evaluation. this block returns eval and move that leads to eval. returns 0 posiyion - evaluation
                if eval > max_eval: #if true eval saves to max eval
                    max_eval = eval #save eval into max eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not max: #if player is minimizing
            min_eval = 100 #minimal eva;uation that player gets from a specific board
            best_move = None
            empty_list = board.get_empty()
            #loop each square inside of the list of empty squares
            for(row, col) in empty_list:
                temp_board = copy.deepcopy(board) #copying the board for testing on other boards - a copy of the object is copied into another object
                temp_board.mark_squares(row, col, self.player)#marking the square to a copy
                eval = self.minmax(temp_board, True)[0] #it's true because of changing the player, first position is an evaluation
                if eval < min_eval: 
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move #returning the min eval with respect to best move

    def evaluation(self, main_board): #main function of minmax class, it's recieveing self and a board
        if self.level == 0: #if the lvl is 0 we can do random choice
            #random choice
            eval = 'random'
            move = self.random_choice(main_board) 
        else:
            #minmax alg choice
            eval, move = self.minmax(main_board, False)

        print(f'Minimax is chosen for marking the square in position {move} with an evaluation {eval}')
        return move #move is the row and the col

#drowing lines for game - lines of the grid
class TicTac:
    def __init__(self): #init method for the new game objects
        self.board = Board() #creating a new board class
        self.comp = MinMax()
        self.player = 1 #who is the next player to mark in the squares #player 1 is crosses and player 2 is circles
        self.gamemode = 'computer' #by human, or by computer (ai)
        self.run = True
        self.lines() #colling the method for showing the lines

    def lines(self): #defining the creating the grid function
        #background color after reseting
        screen.fill(BACKCOLOR)
        #vertical lines
        pygame.draw.line(screen, LINE_COLOR,(SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH) #first line
        pygame.draw.line(screen, LINE_COLOR,(WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH) #y axis is 0, x axis is first; second line
        #horizontal lines
        pygame.draw.line(screen, LINE_COLOR,(0,SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH) #first line
        pygame.draw.line(screen, LINE_COLOR,(0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH) #second line

    def draw_figure(self, row, col):
        if self.player == 1:
            #drawing the cross
            start_down_line = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET) #adjusting the down going line of the cross
            end_down_line = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS, start_down_line, end_down_line, CROSS_WIDTH) #drawing the cross
            #going up line
            start_up_line = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_up_line = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET) 
            pygame.draw.line(screen, CROSS, start_up_line, end_up_line, CROSS_WIDTH) #drawing the line

        elif self.player == 2:
            #drawing the circle
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2) #center position
            pygame.draw.circle(screen, CIRCLE, center, RADIUS, CIRCLE_WIDTH)


    def another_player(self): #chenging the player that is marking the square to the next one 
        self.player = self.player % 2 + 1 #first operation will return the remainder ((model)%2) if the player is 1, than it adds 1 and there is o a remainder so the player is changing 

    def make_move(self, row, col):
        self.board.mark_squares(row, col, self.player) #the last parameter changes from 1 to tictac.player
        #print(board.squares) #testing, return 0 and 1 in console whether it's empty or not
        self.draw_figure(row, col) #graphic displaying of the information
        self.another_player()
                    #print(board.squares) #checking the another player works or not, result in console

    def reset(self):
        self.__init__() #restarting all attributes to default values

    def change_gamemode(self):
        self.gamemode = 'computer' if self.gamemode == 'user' else 'user'
        
    
    def isover(self):
        return self.board.final_condition(show=True) != 0 or self.board.isfull()


def main(): #main function where the code will be executing
    #game object
    tictac = TicTac() #object and the class 
    board = tictac.board
    comp = tictac.comp

    #mainloop
    while True:
            #pygame events
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #event is any actin happening in the game(pressing the key etc)
                pygame.quit()
                sys.exit() #for exiting the game

            if event.type == pygame.KEYDOWN: #keydown event
                #g-gamemode
                if event.key == pygame.K_g:
                    tictac.change_gamemode()
                # r = restart
                if event.key == pygame.K_r:
                    tictac.reset()
                    board = tictac.board #board and ai will be reseted again and start from the initializing condition
                    comp = tictac.comp
                # 0 -random computer alg
                if event.key == pygame.K_0:
                    comp.level = 0
                    # 1 - random 
                if event.key == pygame.K_1:
                    comp.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN: #position of coursor in the pixels
                pos = event.pos #position of pixels
                row = pos[1]//SQUARE_SIZE #represents y axis of the board
                col = pos[0]//SQUARE_SIZE #position 0 of x axis
                #print(row, col) #testing
                if board.empty_square(row,col) and tictac.run:
                    tictac.make_move(row, col)

                    if tictac.isover():
                        tictac.run = False

                #board.mark_squares(row, col, 1) #in a position row col player number 1
                #print(tictac.board.squares) #testing the board, returns information to console
        if tictac.gamemode == 'computer' and tictac.player == comp.player and tictac.run:
            #update the screen
            pygame.display.update()

            #computer methods
            row, col = comp.evaluation(board)
            #board.mark_squares(row, col, comp.player)
            tictac.make_move(row, col)

            if tictac.isover():
                tictac.run = False


        pygame.display.update() #updating the screen
#minimax alg = 
""" terminal case and the base case - terminal case is when the game is over
3 situations: 1) player 1 wins, 2) player 2 wins, 3) draw //terminal cases
Circle player is minimizing his utilities for the winning (for example).
Cross player is maximizing utilities for winning.
1. Firstly checking whether board is on the terminal case or not. 2. Board not on a turminal case - looping through the board to get which squares are empty.
3. Minimizing player tries the circle. 4. Checking if the board is full. Repeating again.
5. Reaching a terminal case(player 1 wins) - negative number is returned.
For maximizing player returns positive number(+1). For Draw it returns 0.
Checking all the scenarios where min or max can win and define cases that are able to win
"""

if __name__ == "__main__":
    main()