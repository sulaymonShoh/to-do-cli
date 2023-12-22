from colorama import Fore, Style
"""
blue -> menu
green -> success
red -> error
"""

def print_menu(s):
    print(Fore.BLUE, s, Style.RESET_ALL)

if __name__ == '__main__':
    print_menu("Menu 1")