import curses
import random

# Initialize the game window
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()  # Get height and width of window
w = curses.newwin(sh, sw, 0, 0)  # Create a new window
w.keypad(1)  # Enable keypad input
w.timeout(100)  # Set a timeout for input

# Initial snake and food setup
snk_x = sw // 4
snk_y = sh // 2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x - 1],
    [snk_y, snk_x - 2]
]
food = [sh // 2, sw // 2]  # Food position
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)  # Draw food

key = curses.KEY_RIGHT  # Initial direction

while True:
    next_key = w.getch()  # Get user input
    key = key if next_key == -1 else next_key  # Update key if pressed

    # Calculate new head position
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert new head
    snake.insert(0, new_head)

    # Check for collision with food
    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)  # Draw new food
    else:
        # Remove the last segment of the snake
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')

    # Check for collision with walls or self
    if (snake[0][0] in [0, sh] or
            snake[0][1] in [0, sw] or
            snake[0] in snake[1:]):
        curses.endwin()  # End the window
        quit()  # Exit the game

    # Draw the snake
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
