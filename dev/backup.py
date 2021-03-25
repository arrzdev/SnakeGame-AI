import os
import random
try:
    import curses
except:
    os.system('pip install windows-curses')
    import curses
from curses import textpad
import time

stdscr = curses.initscr()
curses.curs_set(0)
stdscr.keypad(1)
screen_h, screen_w = stdscr.getmaxyx()
textpad.rectangle(stdscr, 3, 3, screen_h -3, screen_w -3)
score = 1

snk_x = (screen_w -3)/4
snk_y = (screen_h -3)/2

snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

stdscr.addstr(int(screen_h/2), (int(screen_w/2)) - 12, 'Press Any Key To Start')
stdscr.getch()
#cleans the screen
stdscr.addstr(int(screen_h/2), (int(screen_w/2)) - 12, '                      ')
textpad.rectangle(stdscr, 3, 3, screen_h -3, screen_w -3)

stdscr.timeout(100)
#adds the first "food"
food = [int(screen_h/2), int(screen_w/2)]
stdscr.addch(int(food[0]), int(food[1]), curses.ACS_PI)
#sets the first 'pressed' key
key = curses.KEY_RIGHT
currentSnake_d = "right"

while  True:
    #creats and adds the score text
    stdscr.addstr(int((screen_h - (screen_h - 3))/2), (int(screen_w/2)) - 3, 'Score: {}'. format(score))

    #creats the snake head
    stdscr.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
    next_key = stdscr.getch()
    #gets the pressed key and assigns it
    if next_key != -1:
        if currentSnake_d == "right":
            key = key if next_key == curses.KEY_LEFT else next_key
        elif currentSnake_d == "left":
            key = key if next_key == curses.KEY_RIGHT else next_key
        elif currentSnake_d == "up":
            key = key if next_key == curses.KEY_DOWN else next_key
        elif currentSnake_d == "down":
            key = key if next_key == curses.KEY_UP else next_key

    #verification to see if the player was lost the game
    if (int(snake[0][0]) in [3, screen_h-3]
        or int(snake[0][1]) in [3, screen_w-3] or snake[0] in snake[1:]):
        curses.endwin()
        quit()

    #creats a new head
    new_Head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_UP:
        new_Head[0] -= 1
        currentSnake_d = "up"
    elif key == curses.KEY_DOWN:
        new_Head[0] += 1
        currentSnake_d = "down"
    elif key == curses.KEY_LEFT:
        new_Head[1] -= 1
        currentSnake_d = "left"
    elif key == curses.KEY_RIGHT:
         new_Head[1] += 1
         currentSnake_d = "right"

    if int(snake[0][0]) == int(food[0]) and int(snake[0][1]) == int(food[1]):
        food = None
        while food is None:
            n_food = [
                  (int(random.randint(4, screen_h-4))),
                  (int(random.randint(4, screen_w-4)))
            ]
            #creats the new food
            food = n_food if n_food not in snake else None
        stdscr.addch(food[0], food[1], curses.ACS_PI)
        score += 1

    else:
        s_tail = snake.pop()
        stdscr.addch(int(s_tail[0]), int(s_tail[1]), ' ')

    snake.insert(0, new_Head)
    stdscr.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
