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

def check_if_killed():
    if snake[0] in snake[1:]: 
        return True
    else:
        return False

def get_free_space(key):
    alive = 0

    possible_head = [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)]

    while possible_head not in snake and alive < (window.getmaxyx()[1] and window.getmaxyx()[0]): #se nao for instant death
        #after passing alive check adds 1 to alive state
        alive += 1

        possible_head = [possible_head[0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), possible_head[1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)]
        
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





console = curses.initscr() #initialize
screen_height, screen_width = console.getmaxyx()


window = curses.newwin(screen_height-6, screen_width-6, 3, 3)
window.keypad(True) #enable keypad
curses.noecho() #turn off automatic echoing of keys to the screen
curses.curs_set(0)
window.nodelay(True) #makes it possible to not wait for the user input

#initiate values
move = KEY_UP

#first snake head
spawn_x = random.randint(7, window.getmaxyx()[1]-10)
spawn_y = random.randint(1, window.getmaxyx()[0]-2)

#first food
food = [random.randint(1, window.getmaxyx()[0]-2),random.randint(1, window.getmaxyx()[1]-2)]

#build snake coords
snake = [[spawn_y, spawn_x], [spawn_y, spawn_x-1], [spawn_y, spawn_x-2]]

#draw first food
window.addch(food[0], food[1], curses.ACS_PI)

distX = food[1] - snake[0][1]
distY = food[0] - snake[0][0]

possible_moves = []
avaiable_moves = []
choosen = ''

score = 0

while True: # While they Esc move is not pressed
    window.border(0)

    #DEBUG
    p = []
    for i in possible_moves:
        p.append(str(i).replace('259', 'up').replace('260', 'left').replace('261', 'right').replace('258', 'down'))

    a = []
    for i in avaiable_moves:
        a.append(str(i).replace('259', 'up').replace('260', 'left').replace('261', 'right').replace('258', 'down'))

    window.addstr(0, 2, f'| SCORE:{score} | X:{distX} | Y:{distY} | A:{a} | OPTIMI: {choosen} |')

    '''
    #display the score and title
    window.addstr(0, 2, f'  Score: {score}  ')
    window.addstr(0, 27, ' SNAKE! ')
    '''

    #Make the snake faster as it eats more
    #window.timeout(int(140 - (len(snake)/5 + len(snake)/10)%120)) 
    window.timeout(10)
    
    distX = int(food[1] - snake[0][1])
    distY = int(food[0] - snake[0][0])

    event = window.getch() #refreshes the screen and then waits for the user to hit a key

    exit() if event == 113 else '' #if 'Q' is pressed

    ##AIII

    possible_moves = [KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_DOWN]
    avaiable_moves = possible_moves[::]

    #remove the action of going back to his body from the avaiable moves.
    if move == KEY_RIGHT:
        avaiable_moves.remove(KEY_LEFT)
    elif move == KEY_LEFT:
        avaiable_moves.remove(KEY_RIGHT)
    elif move == KEY_UP:
        avaiable_moves.remove(KEY_DOWN)
    elif move == KEY_DOWN:
        avaiable_moves.remove(KEY_UP)


    #DECIDE THE BEST MOVE JUST RELATIVE TO THE FRUIT
    if distY == 0:
        if distX < 0:
            if move != KEY_RIGHT:
                move = KEY_LEFT

        else:
            if move != KEY_LEFT:
                move = KEY_RIGHT

    elif distY < 0:
        if move != KEY_DOWN:
            move = KEY_UP

    else:
        if move != KEY_UP:
            move = KEY_DOWN

    #CREATES THE NEW HEAD TO THAT MOVE
    new_head = [snake[0][0] + (move == KEY_DOWN and 1) + (move == KEY_UP and -1), snake[0][1] + (move == KEY_LEFT and -1) + (move == KEY_RIGHT and 1)]

    if new_head in snake or get_free_space(move) < 6:
        max_score = 0
        for pmove in avaiable_moves:
            alive_score = get_free_space(pmove)

            if alive_score > max_score:
                max_score = alive_score
                move = pmove

        acc = []
        for i in avaiable_moves:
            acc.append(str(i).replace('259', 'up').replace('260', 'left').replace('261', 'right').replace('258', 'down'))
        
        print(f'SCORE:{score} POSSIVEIS:{acc} | ESCOLHIDO:{str(move).replace("259", "up").replace("260", "left").replace("261", "right").replace("258", "down")}')

        choosen = str(move).replace("259", "up").replace("260", "left").replace("261", "right").replace("258", "down")
    else:
        choosen = str(move).replace("259", "up").replace("260", "left").replace("261", "right").replace("258", "down")



    new_head = [snake[0][0] + (move == KEY_DOWN and 1) + (move == KEY_UP and -1), snake[0][1] + (move == KEY_LEFT and -1) + (move == KEY_RIGHT and 1)]

    if new_head in snake:
        while window.getch() != 113:
            time.sleep(1)

    #IF THAT COORDS OF THAT FICTIONAL HEAD CORRESPONDE TO ANY PART OF THE SNAKE B
    # ODY JUST CHOOSE A RANDOM MOVE FROM THE POSSIBLE MOVES UNTIL IT IS NOT "KILLABLE"

    #TELEPORT WHEN HITS WALLS
    if new_head[0] == 0:
        new_head = [window.getmaxyx()[0]-1, new_head[1]]
    elif new_head[0] == window.getmaxyx()[0]:
        new_head = [0, new_head[1]]

    elif new_head[1] == 0:
        new_head = [new_head[0], window.getmaxyx()[1]-1]
    elif new_head[1] == window.getmaxyx()[1]:
        new_head = [new_head[0], 0]


    '''
    #Exit if snake goes into a wall
    if snake[0][0] == 0 or snake[0][0] == (window.getmaxyx()[0]) or snake[0][1] == 0 or snake[0][1] == window.getmaxyx()[1]:
    '''


    #Exit if snake runs over itself
    if check_if_killed():
        print(f' | SCORE: {score} | ')
        break

    #INSERT HEAD
    snake.insert(0, new_head)

    # When snake eats the food
    if snake[0] == food:    
        score += 1                                        
        food = []
        while food == []:
            # Generate coordinates for next food
            food = [random.randint(1, window.getmaxyx()[0]-2), random.randint(1, window.getmaxyx()[1]-2)]                
            if food in snake: food = []
        window.addch(food[0], food[1], curses.ACS_PI) #display the food
    else:    
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

curses.endwin() #close the window and end the game

