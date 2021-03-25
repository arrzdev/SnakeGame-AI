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
curses.curs_set(False)
stdscr.keypad(True)
curses.noecho()
curses.cbreak()


screen_h, screen_w = stdscr.getmaxyx()

screen_h = int(screen_h)
screen_w = int(screen_w)

textpad.rectangle(stdscr, 3, 3, screen_h -3, screen_w -3)

score = 0

snk_x = random.randint(4, screen_w - 7)
snk_y = random.randint(4, screen_h - 7)

snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

stdscr.addstr(0, 0, 'Press Any Key To Start')

stdscr.getch()

stdscr.clear()
textpad.rectangle(stdscr, 3, 3, screen_h -3, screen_w -3)


stdscr.timeout(100)

#adds the first "food"

food = [random.randint(4, screen_h - 7), random.randint(4, screen_w - 7)]

stdscr.addch(int(food[0]), int(food[1]), 'o')

#sets the first 'pressed' key
key = curses.KEY_RIGHT
currentSnake_d = "right"

while  True:
    #quit if 'q' pressed
    if stdscr.getch() == 113:
        exit()

    #creats and adds the score text
    stdscr.addstr(0, 0, 'Score: {}'. format(score))

    #creats the snake head
    stdscr.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)


    distX = food[1] - snake[0][1]
    distY = food[0] - snake[0][0]

    score = f'X:{distX}; Y:{distY}'

    move = currentSnake_d

    #creats a new head
    new_Head = [snake[0][0], snake[0][1]]

    if move == 'up':
        new_Head[0] -= 1
        currentSnake_d = "up"
    elif move == 'down':
        new_Head[0] += 1
        currentSnake_d = "down"
    elif move == 'left':
        new_Head[1] -= 1
        currentSnake_d = "left"
    elif move == 'right':
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
        #score += 1

    else:
        s_tail = snake.pop()
        stdscr.addch(int(s_tail[0]), int(s_tail[1]), '')

    snake.insert(0, new_Head)
    stdscr.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)

    stdscr.refresh()