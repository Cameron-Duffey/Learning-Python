from IPython.display import clear_output
import random

#DISPLAY TIC TAC TOE BOARD
def display_board(board):
    clear_output()
    print(board[7]+'|'+board[8]+'|'+board[9]+'|')
    print(board[4]+'|'+board[5]+'|'+board[6]+'|')
    print(board[1]+'|'+board[2]+'|'+board[3]+'|')

#CHOOSE WHO IS X OR O
def player_input():

    marker = ' '

    while marker != 'X' and marker != 'O':
        marker = input('Player 1: Choose X or O: ').upper()
    
    if marker == 'X':
        return('X','O')
    else:
        return('O','X')
    
#PLACE A MARKER ON THE BOARD
def place_marker(board,marker,position):
    board[position] = marker

#WIN CHECK
def win_check(board, mark):
     #ALL ROWS AND CHECK TO SEE IF THEY ALL SHARE THE SAME MARKER?
    return ((board[1] == mark and board[2] == mark and board[3] == mark) or
            (board[4] == mark and board[5] == mark and board[6] == mark) or 
            (board[7] == mark and board[8] == mark and board[9] == mark) or
    #ALL COLUMNS, CHECK TO SEE IF MARKER MATCHES
            (board[7] == mark and board[4] == mark and board[1] == mark) or
            (board[8] == mark and board[5] == mark and board[2] == mark) or
            (board[9] == mark and board[6] == mark and board[3] == mark) or
    #2 DIAGONALS, CHECK TO SEE MATCH
            (board[7] == mark and board[5] == mark and board[3] == mark) or
            (board[9] == mark and board[5] == mark and board[1] == mark))

#CHOOSE WHO GOES FIRST VIA A COIN FLIP
def choose_first():
    flip = random.randint(0,1)

    if flip == 0:
        return 'Player 1'
    else:
        return 'Player 2'
    
#CHECK TO SEE IF THE POSITION IS BLANK AND PLACE MARKER
def space_check(board,position):
    return board[position] == ' '

#CHECK TO SEE IF BOARD IS FULL AND RETURN A BOOLEAN
def full_board_check(board):
    for i in range(1,10):
        if space_check(board,i):
            return False
    #BOARD IS FULL IF WE RETURN TRUE
    return True

#ASK THE PLAYER'S NEXT POSITION AND CHECK IF THE SPACE IS FREE
def player_choice(board):
    position = 0

    while position not in [1,2,3,4,5,6,7,8,9] or not space_check(board,position):
        position = int(input('Choose a position(1-9): '))

    return position

#PLAY AGAIN? RETURN TRUE IF THEY DO
def replay():
    choice = input('Play again? Enter Yes or No: ')

    return choice == 'Yes'

#WHILE LOOP TO KEEP RUNNING THE GAME
print('Welcome to Tic Tac Toe')

#PLAY THE GAME
while True:
    ##SET UP EVERYTHING
    the_board = [' ']*10
    player1_marker, player2_marker = player_input()

    turn = choose_first()
    print(turn + ' will go first!')

    play_game = input('Ready to play? Y or N?: ').upper()

    if play_game == 'Y':
        game_on = True
    else:
        game_on = False
    
    ##GAMEPLAY
    while game_on:

        if turn == 'Player 1':
            ###SHOW THE BOARD
            display_board(the_board)
            ###CHOOSE A POSITION
            position = player_choice(the_board)
            ###PLACE MARKER ON THE POSITION
            place_marker(the_board,player1_marker,position)

            ###CHECK IF THEY WON
            if win_check(the_board,player1_marker):
                display_board(the_board)
                print('Player 1 has won!')
                game_on = False
            else:
            ###CHECK FOR TIE
                if full_board_check(the_board):
                    display_board(the_board)
                    print('Tie Game!')
                    game_on = False
                else:
                    turn = 'Player 2'
        else:
            ###SHOW THE BOARD
            display_board(the_board)
            ###CHOOSE A POSITION
            position = player_choice(the_board)
            ###PLACE MARKER ON THE POSITION
            place_marker(the_board,player2_marker,position)

            ####CHECK IF THEY WON
            if win_check(the_board,player2_marker):
                display_board(the_board)
                print('Player 2 has won!')
                game_on = False
            else:
            ###CHECK FOR TIE
                if full_board_check(the_board):
                    display_board(the_board)
                    print('Tie Game!')
                    game_on = False
                else:
                    turn = 'Player 1'
    #BREAK OUT OF THE WHILE LOOP ON replay()
    if not replay():
        break