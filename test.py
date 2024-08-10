
import curses

# Define your buttons with their positions and labels
buttons = [
    {"label": "Button1", "x": 5, "y": 5},
    {"label": "Button2", "x": 10, "y": 3},
    {"label": "Button3", "x": 15, "y": 7},
]

# Initialize the current selected button index
selected_button = 0

def draw_buttons(stdscr, buttons, selected_button):
    stdscr.clear()
    for i, button in enumerate(buttons):
        x, y = button['x'], button['y']
        label = button['label']
        if i == selected_button:
            stdscr.addstr(y, x, label, curses.A_REVERSE)  # Highlight selected button
        else:
            stdscr.addstr(y, x, label)
    stdscr.refresh()

def main(stdscr):
    global selected_button
    curses.curs_set(0)  # Hide the cursor

    while True:
        draw_buttons(stdscr, buttons, selected_button)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_button = (selected_button + 1) % len(buttons)
        elif key == curses.KEY_DOWN:
            selected_button = (selected_button - 1) % len(buttons)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(20, 0, f"You pressed {buttons[selected_button]['label']}!")
            stdscr.refresh()
            stdscr.getch()
        elif key == 27:  # Escape key to exit
            break

curses.wrapper(main)