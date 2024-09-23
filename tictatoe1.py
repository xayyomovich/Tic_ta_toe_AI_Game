# '''
#      press 'g' to change gamemode (pvp or ai)
#      press '0' to change ai level to 0 (random)
#      press '1' to change ai level to 1 (impossible)
#      press 'r' to restart the game

# '''


import sys     # to quit application
import pygame 
import numpy as np       # A library for numerical operations, used here for creating arrays.
import random
import copy

WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20


RADIUS = SQSIZE // 4

OFFSET = 50

#COLORS

BG_COLOR = (72,61,139)
LINE_COLOR = (106,90,205)
CIRC_COLOR = 	(0,128,128)
CROSS_COLOR = (0,0,128)


# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TA TOE AI')
screen.fill( BG_COLOR )


class Board:   # Defines a class Board to represent the Tic Tac Toe game board. 
               # It has methods to check for a final game state, mark a square, check if a square is empty, and more.

     def __init__(self):
          self.squares = np.zeros( (ROWS, COLS) )
          self.empty_sqrs = self.squares
          self.marked_sqr = 0
          

     def final_state(self, show = False):
          '''
          @ return 0 if there is no win yet
          @ return 1 if player 1 wins
          @ return 2 if player 2 wins
          '''

          # vertical wins
          for col in range(COLS):
               if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                    if show:
                         color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                         iPos = (col * SQSIZE + SQSIZE // 2, 20)
                         fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                         pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                    return self.squares[0][col]
               

          # horizontal wins
          for row in range(ROWS):
               if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                    if show:
                         color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                         iPos = (20, row * SQSIZE + SQSIZE // 2)
                         fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                         pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                    return self.squares[row][0]
               

          # desc diagonal
          if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
               if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
               return self.squares[1][1]
          

          # asc diagonal
          if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
               if show:
                    color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (20, HEIGHT - 20)
                    fPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
               return self.squares[1][1]
          
          # no win yet
          return 0


     def mark_sqr(self, row, col, player):
          self.squares[row][col] = player
          self.marked_sqr += 1


     def empty_sqr(self, row, col):
          return self.squares[row][col] == 0
     

     def get_empty_sqrs(self):
          empty_sqrs = []          # coordinates of all the empty squares on the board.
          for row in range(ROWS):
               for col in range(COLS):
                    if self.empty_sqr(row, col):
                         empty_sqrs.append( (row, col) )
          return empty_sqrs

     
     def isfull(self):
          return self.marked_sqr == 9


     def isempty(self):
          return self.marked_sqr == 0

# start 1:13

class AI:      # Defines a class AI representing the computer player. It has methods for making random moves (rnd), 
               # implementing the minimax algorithm (minimax), and evaluating the best move (eval).

     def __init__(self, level = 1, player = 2):      
          self.level = level                         # level 0 is random AI, level 1 is minimax AI
          self.player = player                       # player specifies whether the AI is player 1 or player 2

     # --- RANDOM ---
     
     def rnd(self, board):
          empty_sqrs = board.get_empty_sqrs()
          idx = random.randrange(0, len(empty_sqrs))

          return empty_sqrs[idx]   # row, col

     # --- MINIMAX ---

     def minimax(self, board, maximizing):
          
          # terminal case
          case = board.final_state()    # checks the current state of the game 

          # player 1 wins
          if case == 1:
               return 1, None   # eval, move
          
          # player 2 wins
          if case == 2:
               return -1, None     # here minimazing. this is AI
          
          # draw
          elif board.isfull():
               return 0, None
          
          if maximizing:
               # maximizing player (AI)
               max_eval = -100
               best_move = None
               empty_sqrs = board.get_empty_sqrs()

               for (row, col) in empty_sqrs:
                    temp_board = copy.deepcopy(board)
                    temp_board.mark_sqr(row, col, 1)
                    eval = self.minimax(temp_board, False)[0]
                    if eval >  max_eval:
                         max_eval = eval
                         best_move = (row, col)

               return max_eval, best_move               


          elif not maximizing:
               # minimizing player (human or opponent)
               min_eval = 100
               best_move = None
               empty_sqrs = board.get_empty_sqrs()

               for (row, col) in empty_sqrs:
                    temp_board = copy.deepcopy(board)
                    temp_board.mark_sqr(row, col, self.player)
                    eval = self.minimax(temp_board, True)[0]
                    if eval < min_eval:
                         min_eval = eval
                         best_move = (row, col)

               return min_eval, best_move          
     
     # --- MAIN EVAL ---

     def eval(self, main_board):
          if self.level == 0:
               # random choice
               eval = 'random'
               move = self.rnd(main_board)

          else:
               # minimax algo choice
               eval, move = self.minimax(main_board, False)

          print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

          return move  # row, col
     


class Game:    # Defines a class Game to manage the overall game. It has methods for drawing lines, drawing game figures, 
               # making moves, changing game mode, checking if the game is over, and resetting the game.

     def __init__(self):  #  
          self.board = Board()
          # self.ai1 = AI(level=ai1_level, player=1)
          # self.ai2 = AI(level=ai2_level, player=2)
          self.ai = AI()
          self.player = 1     # player 1 = crosses. player 2 = circles
          self.gamemode = 'ai' # pvp or ai
          self.running = True
          self.show_lines()


# def play_ai_vs_ai(self):
          # while self.running and not self.board.isfull() and not self.board.final_state(show=False):
          #      # AI 1
          #      row, col = self.ai1.eval(self.board)
          #      self.make_move(row, col)
            
          #      if self.isover():
          #           break

          #      # AI 2
          #      row, col = self.ai2.eval(self.board)
          #      self.make_move(row, col)

          # self.display_result()
          
     # --- DRAW METHODS ---
     def show_lines(self):
          screen.fill( BG_COLOR )
          
          # vertical
          pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
          pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

          #horizontal
          pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
          pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT -SQSIZE), LINE_WIDTH)


     def draw_fig(self,row,col):

          if self.player == 1:
               #draw cross
               # desc line
               start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
               end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE -OFFSET)
               pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
               # easc_line
               start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
               end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
               pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
               
          
          elif self.player == 2:
               # draw circle
               center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
               pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

     # -------OTHER METHODS---------

     def make_move(self, row, col): 
          self.board.mark_sqr(row, col, self.player)
          self.draw_fig(row, col)
          self.next_turn()

     def next_turn(self):
          self.player = self.player % 2 + 1


     def change_gamemode(self):
          self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

     def isover(self):
          return self.board.final_state(show = True) != 0 or self.board.isfull()

     def reset(self):
          self.__init__()



def main():    # The main function initializes the game and enters the main game loop. It handles events such as quitting, 
               # key presses, and mouse clicks. It also updates the display and allows the player and AI to take turns making moves.

     #-----OBJECTS------ 

     game = Game()
     board = game.board  
     ai = game.ai
     # game = Game(ai1_level=1, ai2_level=1)

     # --- MAINLOOP ---

     while True:

          for event in pygame.event.get():
               # quit event

               if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

               # keydown event
               if event.type == pygame.KEYDOWN:

                    # if event.key == pygame.K_a:
                    #      game.change_gamemode()

                    # g-gamemode
                    if event.key == pygame.K_g:
                         game.change_gamemode() 

                    # r-restart    
                    if event.key == pygame.K_r:
                         game.reset()
                         board = game.board  
                         ai = game.ai


                    # 0-random ai
                    if event.key == pygame.K_0:
                         ai.level = 0

                    # 1-random ai
                    if event.key == pygame.K_1:
                         ai.level = 1


               if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE
                    
                    # human mark
                    if board.empty_sqr(row,col) and game.running:
                         game.make_move(row, col)
                         # print(board.squares)

                         if game.isover():
                              game.running = False

          # AI initial call
          if game.gamemode == 'ai' and game.player == ai.player and game.running:
               
               # update the screen
               pygame.display.update()

               # ai methods
               row, col = ai.eval(board)
               game.make_move(row, col)

               if game.isover():
                    game.running = False
                    

          pygame.display.update()

main()