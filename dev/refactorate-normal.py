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

console = curses.initscr() #initialize
screen_height, screen_width = console.getmaxyx()


window = curses.newwin(screen_height-6, screen_width-6, 3, 3)
window.keypad(True) #enable keypad
curses.noecho() #turn off automatic echoing of keys to the screen
curses.curs_set(0)
window.nodelay(True) #makes it possible to not wait for the user input

#initiate values
current_key = KEY_RIGHT
score = 0

#initialize first food and snake coordinates
snake = [[5,8], [5,7], [5,6]]
food = [10,25]

#display the first food
window.addch(food[0], food[1], curses.ACS_PI)

distX = food[1] - snake[0][1]
distY = food[0] - snake[0][0]

while True: # While they Esc current_key is not pressed
    window.border(0)
    #display the score and title
    window.addstr(0, 2, f'  X: {distX}; Y: {distY}  ')
    window.addstr(0, 27, ' SNAKE! ')
    #Make the snake faster as it eats more
    window.timeout(int(140 - (len(snake)/5 + len(snake)/10)%120)) 
    
    distX = int(food[1] - snake[0][1])
    distY = int(food[0] - snake[0][0])

    event = window.getch() #refreshes the screen and then waits for the user to hit a key

    exit() if event == 113 else '' #if 'Q' is pressed

    if event != -1:
        if current_key == KEY_RIGHT:
            current_key = current_key if event == KEY_LEFT else event
        elif current_key == KEY_LEFT:
            current_key = current_key if event == KEY_RIGHT else event
        elif current_key == KEY_UP:
            current_key = current_key if event == KEY_DOWN else event
        elif current_key == KEY_DOWN:
            current_key = current_key if event == KEY_UP else event

    # Calculates the new coordinates of the head of the snake.
    snake.insert(0, [snake[0][0] + (current_key == KEY_DOWN and 1) + (current_key == KEY_UP and -1), snake[0][1] + (current_key == KEY_LEFT and -1) + (current_key == KEY_RIGHT and 1)])

    #Exit if snake goes into a wall
    if snake[0][0] == 0 or snake[0][0] == (window.getmaxyx()[0]) or snake[0][1] == 0 or snake[0][1] == window.getmaxyx()[1]: break

    #Exit if snake runs over itself
    if snake[0] in snake[1:]: break

    # When snake eats the food
    if snake[0] == food:                                            
        food = []
        score += 1
        while food == []:
            # Generate coordinates for next food
            food = [random.randint(7, screen_height-7), random.randint(7, screen_width-7)]                
            if food in snake: food = []
        window.addch(food[0], food[1], curses.ACS_PI) #display the food
    else:    
        last = snake.pop()
        window.addch(last[0], last[1], ' ')
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
    

curses.endwin() #close the window and end the game
print("\nScore: " + str(score))