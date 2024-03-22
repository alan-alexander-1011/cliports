"""
additional from my own cpu benchmark

----------------------------------------------------------------
LICENSE For software code and distribution and advertising materials:
 
MIT/GU-NNoA-PEC License

Copyright (c) 2023 alan_alexander

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

After the MIT License terms, the name of alan_alexander SHALL NOT be used in advertising
or to promote the sale, to use or other dealings in this Software without the prior written
of authorization and acceptance from alan_alexander.

The Distributor of this Software is required to provide a clear explanation and conspicuous notice
of any modification made to the original code (the "Software") when distributing their modified version.
This notice should clearly indicate the changes made and provide proper attribution and provide proper
explanation of the changes made to the original version of the Software. And the Distributor may give credits
to the original owner.

----------------------------------------------------------------
"""
import sys
try:
    import msvcrt
except ImportError:
    pass
try:
    import colorama
except ImportError:
    supports_colorama = False
else: supports_colorama = True
import curses,typing

def arrow_key_menu(options: list, start_message:str = ""):
    """
    Displays a menu with the given options and allows the user to navigate using arrow keys.\n
    Returns the index of the selected option.
    """
    selected_option = 0

    if sys.platform.startswith('win'):
        while True:
            # Clear the console screen
            sys.stdout.write("\033[H\033[J")
            sys.stdout.write(start_message+"\n")
            # Print the menu options
            for i, option in enumerate(options):
                if i == selected_option:
                    sys.stdout.write("-> "); sys.stdout.write(colorama.Fore.GREEN + option + colorama.Fore.RESET + "\n") if supports_colorama else sys.stdout.write(option + "\n")
                else:
                    sys.stdout.write("   "); sys.stdout.write(option + "\n")

            # Wait for user input
            key = msvcrt.getch()

            # Handle arrow key input
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H' and selected_option > 0:
                    # Up arrow key
                    selected_option -= 1
                elif key == b'P' and selected_option < len(options) - 1:
                    # Down arrow key
                    selected_option += 1
            elif key == b'\r':
                # Enter key
                return selected_option
    else:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        try:
            while True:
                stdscr.clear()
                stdscr.addstr(start_message+"\n")
                # Print the menu options
                for i, option in enumerate(options):
                    if i == selected_option:
                        stdscr.addstr("-> " + option + "\n", curses.A_REVERSE)
                    else:
                        stdscr.addstr("   " + option + "\n")

                # Get user input
                key = stdscr.getch()

                # Handle arrow key input
                if key == curses.KEY_UP and selected_option > 0:
                    selected_option -= 1
                elif key == curses.KEY_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif key == ord('\n'):
                    # Enter key
                    return selected_option
        finally:
            # Clean up curses
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
