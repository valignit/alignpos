#! c:\\Users\\ghouseam\\AppData\\Local\\Programs\\Python\\Python37\\pythonw.exe
import sys
from main_menu import MainMenu
from common import Signin


######
# Wrapper function for main menu  
def main_menu(user_id, terminal_id):

    main_menu = MainMenu(user_id, terminal_id)


######
# Main function
def main():
    while True:
        signin = Signin()
        if signin.ok:
            main_menu(signin.user_id, signin.terminal_id)
        else:
            break
    
    
######
# Entry point
if __name__ == "__main__":
    main()