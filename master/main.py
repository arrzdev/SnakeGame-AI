import os
import random
try:
    import curses
except:
    os.system('pip install windows-curses')
    import curses
from curses import textpad
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import time

'''
------------------------------------------------------------------------
TO PAST ME:
COORDENATES ARE CHANGED INSTEAD OF (x,y) WE USE (y,x) BECAUSE OF THE LIB
------------------------------------------------------------------------
'''

#DEFAULT CURRENT MOVE IS RIGHT (COULD BE CHANGED!)
def game(current_move='KEY_RIGHT'):
    global food
    global snake

    #START SCORE
    score = 0
    while True:
        #REFRESH THE WINDOW AND GET ANY PRESSED KEY
        event = window.getch() 

        #EXIT IF 'Q' IS PRESSED
        exit() if event == 113 else ''

        #UPDATE SNAKE SPEED
        #window.timeout(int(140 - (len(snake)/5 + len(snake)/10)%120)) 
        window.timeout(10)
        
        #GET AVAILABLE MOVES
        available_moves = get_available_moves(current_move)

        #DECIDE THE BEST MOVE JUST RELATIVE TO THE FRUIT
        distanceX = food[1] - snake[0][1]
        distanceY = food[0] - snake[0][0]

        fruit_best_move = get_best_move_fruit(dx=distanceX, dy=distanceY, current_move=current_move)

        #CREATES THE NEW HEAD TO THAT MOVE
        fruit_move_head = [snake[0][0] + (fruit_best_move == KEY_DOWN and 1) + (fruit_best_move == KEY_UP and -1), snake[0][1] + (fruit_best_move == KEY_LEFT and -1) + (fruit_best_move == KEY_RIGHT and 1)]

        #DEFINE TEMP BEST MOVE FROM "FRUIT_BEST_MOVE"
        best_move = fruit_best_move

        #IF THE FRUIT BEST MOVE HEAD IS A KILLABLE PLAY OR 6 CHUNKS AWAY FROM DIEING
        if fruit_move_head in snake or get_free_space(move=fruit_best_move) < random.randint(2, 6):
            best_move = get_best_move_sensors(available=available_moves)
            
        choosen = str(best_move).replace("259", "up").replace("260", "left").replace("261", "right").replace("258", "down")

        available_translated = []
        for i in available_moves:
            available_translated.append(str(i).replace('259', 'up').replace('260', 'left').replace('261', 'right').replace('258', 'down'))

        #CONSOLE-LOG THE DECISION MADE
        print(f'\n [DECISION]: state: {score}, available: {available_translated}, played: {choosen}]')

        #CREATE THE BEST HEAD
        best_head = [snake[0][0] + (best_move == KEY_DOWN and 1) + (best_move == KEY_UP and -1), snake[0][1] + (best_move == KEY_LEFT and -1) + (best_move == KEY_RIGHT and 1)]

        #CHECK IF HEAD IS IN THE BOARD AND IF IT IS TELEPORT IT
        final_head = teleport_snake_head(best_head)


        #Exit if snake runs over itself
        if check_if_killed():
            print(f'\n [LOST]: state: {score}')
            break

        #INSERT HEAD
        snake.insert(0, final_head)

        # When snake eats the food
        if snake[0] == food:    
            score += 1  
            food = []
            generate_food()                                      
        else:    
            last = snake.pop()
            window.addch(last[0], last[1], ' ')
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

        #DRAW BORDER
        window.border(0)

        #DISPLAY DEBUG INFORMATION
        display(available=available_translated, choosen=choosen, score=score, dx=distanceX, dy=distanceY)

    curses.endwin() #close the window and end the game

def display(available=[], choosen='???', score=0, dx=0, dy=0):
    window.addstr(0, 2, f'| SCORE:{score} | DX:{dx} | DY:{dy} | AV:{available} | BEST:{choosen} |')

def get_available_moves(current_move):
    available_moves = [KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_DOWN]

    if current_move == KEY_RIGHT:
        available_moves.remove(KEY_LEFT)
    elif current_move == KEY_LEFT:
        available_moves.remove(KEY_RIGHT)
    elif current_move == KEY_UP:
        available_moves.remove(KEY_DOWN)
    elif current_move == KEY_DOWN:
        available_moves.remove(KEY_UP)

    return available_moves

def get_best_move_fruit(dx=0, dy=0, current_move=''):
    best_move = current_move

    if dy == 0:
        if dx < 0: #fruta a esquerda
            if current_move != KEY_RIGHT:
                best_move = KEY_LEFT

        else: #fruta a direita
            if current_move != KEY_LEFT:
                best_move = KEY_RIGHT

    elif dy < 0:
        if current_move != KEY_DOWN:
            best_move = KEY_UP

    else:
        if current_move != KEY_UP:
            best_move = KEY_DOWN

    return best_move


    '''
    if abs(dy) > abs(dx):
        if dy == 0:
            if dx < 0: #fruta a esquerda
                if current_move != KEY_RIGHT:
                    best_move = KEY_LEFT

            else: #fruta a direita
                if current_move != KEY_LEFT:
                    best_move = KEY_RIGHT

        elif dy < 0: #fruta em cima
            if current_move != KEY_DOWN:
                best_move = KEY_UP

        else: #fruta em baixo
            if current_move != KEY_UP:
                best_move = KEY_DOWN
    
    else:
        if dx == 0:
            if dy < 0: #fruta em cima
                if current_move != KEY_DOWN:
                    best_move = KEY_UP

            else: #fruta em baixo
                if current_move != KEY_UP:
                    best_move = KEY_DOWN

        elif dx < 0: #fruta a esquerda
            if current_move != KEY_RIGHT:
                best_move = KEY_LEFT

        else: #fruta a direita
            if current_move != KEY_LEFT:
                best_move = KEY_RIGHT


    return best_move
    '''

def get_best_move_sensors(available=[]):
    max_score = 0

    #choose a random move at beggining
    best_move = random.choice(available)

    for spec_move in available:
        alive_score = get_free_space(spec_move)

        if alive_score > max_score:
            max_score = alive_score
            best_move = spec_move

    return best_move

def check_if_killed():
    if snake[0] in snake[1:]: 
        return True
    else:
        return False

def get_free_space(move=''):
    alive = 0

    possible_head = [snake[0][0] + (move == KEY_DOWN and 1) + (move == KEY_UP and -1), snake[0][1] + (move == KEY_LEFT and -1) + (move == KEY_RIGHT and 1)]

    while possible_head not in snake and alive < (window.getmaxyx()[1] and window.getmaxyx()[0]): #se nao for instant death
        #after passing alive check adds 1 to alive state
        alive += 1

        possible_head = [possible_head[0] + (move == KEY_DOWN and 1) + (move == KEY_UP and -1), possible_head[1] + (move == KEY_LEFT and -1) + (move == KEY_RIGHT and 1)]
        
        #TELEPORT THE HEAD IF IN THE BOARD LINES
        if possible_head[0] == 0:
            possible_head = [window.getmaxyx()[0]-1, possible_head[1]]
        elif possible_head[0] == window.getmaxyx()[0]:
            possible_head = [0, possible_head[1]]
        elif possible_head[1] == 0:
            possible_head = [possible_head[0], window.getmaxyx()[1]-1]
        elif possible_head[1] == window.getmaxyx()[1]:
            possible_head = [possible_head[0], 0]

    return alive

def teleport_snake_head(head=[]):
    #TELEPORT WHEN HITS WALLS
    if head[0] == 0:
        new_head = [window.getmaxyx()[0]-1, head[1]]
    elif head[0] == window.getmaxyx()[0]:
        new_head = [0, head[1]]
    elif head[1] == 0:
        new_head = [head[0], window.getmaxyx()[1]-1]
    elif head[1] == window.getmaxyx()[1]:
        new_head = [head[0], 0]
    else:
        new_head = head

    return new_head

def generate_food():
    global food
    while food == []:
        # Generate coordinates for next food
        #generate random coordinates to first food
        food = [random.randint(1, window.getmaxyx()[0]-2),random.randint(1, window.getmaxyx()[1]-2)]              
        if food in snake: food = []
    window.addch(food[0], food[1], curses.ACS_PI) #display the food

if __name__ == '__main__':
    #--SET INITIAL VARS
    console = curses.initscr() #initialize
    screen_height, screen_width = console.getmaxyx()

    window = curses.newwin(screen_height-6, screen_width-6, 3, 3)
    window.keypad(True) #enable keypad
    curses.noecho() #turn off automatic echoing of keys to the screen
    curses.curs_set(0)
    window.nodelay(True) #makes it possible to not wait for the user input

    #define initial movement direction
    move = KEY_RIGHT

    #generate random coordinates to first food
    food = [random.randint(1, window.getmaxyx()[0]-2),random.randint(1, window.getmaxyx()[1]-2)]
    window.addch(food[0], food[1], curses.ACS_PI)

    #generate random x and y coordinates for the snake head
    spawn_x = random.randint(7, window.getmaxyx()[1]-10)
    spawn_y = random.randint(1, window.getmaxyx()[0]-2)

    #build snake based on the head coordinates
    snake = [[spawn_y, spawn_x], [spawn_y, spawn_x-1], [spawn_y, spawn_x-2]]

    #START GAME
    game(current_move=move)