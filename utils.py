from bcrypt import hashpw, gensalt, checkpw
from colorama import Fore, Style

"""
blue -> menu
green -> success
red -> error
"""


class ResponseDate:
    def __init__(self, data: str, success: bool = True, status: int = 200, ):
        self.data = data
        self.success = success or True
        self.status = status

    def __repr__(self):
        return f"{self.data}:{self.success}"


def print_menu(s: str):
    print(Fore.BLUE, s, Style.RESET_ALL)


def print_success(s: str):
    print(Fore.GREEN, s, Style.RESET_ALL)


def print_error(s: str):
    print(Fore.RED, s, Style.RESET_ALL)


def encode_passrord(pwd: str):
    pwd = pwd.encode("utf-8")
    salt = gensalt()
    password = hashpw(pwd, salt)
    encoded_pwd = password.decode("utf-8")
    return encoded_pwd


def print_response(response: ResponseDate):
    color = Fore.GREEN if response.success else Fore.RED
    print(color, response.data, Style.RESET_ALL)


def match_password(passs: str, hpasss: str):
    passs = passs.encode("utf-8")
    hpasss = hpasss.encode("utf-8")
    return checkpw(passs, hpasss)
