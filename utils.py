from colorama import Fore, Style
from bcrypt import hashpw, gensalt, checkpw
"""
blue - menu
green - succes
red - error
"""


class ResponseDate:
    def __init__(self, data, success:bool=True, status:int=200):
        self.data = data
        self.success = success
        self.status = status

    def __repr__(self):
        return f"{self.data}:{self.success}"

def print_menu(s: str):
    print(Fore.BLUE, s, Style.RESET_ALL)


def print_success(s: str):
    print(Fore.GREEN, s, Style.RESET_ALL)


def print_error(s: str):
    print(Fore.RED, s, Style.RESET_ALL)


def encode_password(pwd: str):
    pwd = pwd.encode("utf-8")
    salt = gensalt()
    password = hashpw(pwd, salt)
    encoded_password = password.decode("utf-8")
    return encoded_password


def match_password(password: str, encoded_password: str):
    password = password.encode("utf-8")
    encoded_password = encoded_password.encode("utf-8")
    return checkpw(password, encoded_password)


if __name__ == '__main__':
    print(match_password("hi", encode_password("hi")))
