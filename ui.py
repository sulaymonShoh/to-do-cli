from getpass import getpass

import db
import models
import utils
from utils import print_menu, print_error, print_success
import service

session_user: models.User = None


def login():
    global session_user
    username = input("username: ")
    password = getpass("password: ")
    response: utils.ResponseDate = service.login_user(username, password)
    utils.print_response(response)
    session_user = response.data


def register():
    username = input("username: ")
    password1 = getpass("password: ")
    password2 = getpass("retype password: ")
    response: utils.ResponseDate = service.register_user(username, password1, password2)
    utils.print_response(response)


def logout():
    global session_user
    db.update_user_status_to_inactive(session_user.username)
    session_user = None


def create_todo():
    global session_user
    name = input("Todo name : ")
    print_menu("1.PERSONAL")
    print_menu("2.WORK")
    print_menu("3.STUDY")
    types = {"1": models.TodoType.PERSONAL.value, "2": models.TodoType.WORK.value, "3": models.TodoType.STUDY.value, }
    choice = input("choice")
    type = types[choice]
    response: utils.ResponseDate = service.create_todo_service(
        models.Todo(name=name, user_id=session_user.id, type=type))
    utils.print_response(response)


def update_todo():
    pass
    # update status to completed

def delete_todo():
    pass
    # check todo is completed


def todo_list():
    pass
    # show onlu one users todos


def block_user():
    pass


def unblock_user():
    pass


def block_admin():
    pass


def unblock_admin():
    pass


# divide menu according role
# login_menu()
# user_menu()
# admin_menu()
def menu():
    global session_user

    while True:
        if not session_user:
            print_menu("=> login")
            print_menu("=> register")
        elif session_user.role == models.UserRole.USER.value:
            print_menu("=> create_todo")
            print_menu("=> update_todo")
            print_menu("=> delete_todo")
            print_menu("=> todo_list")
            print_menu("=> logout")
        elif session_user.role == models.UserRole.ADMIN.value:
            print_menu("=> create_todo")
            print_menu("=> update_todo")
            print_menu("=> delete_todo")
            print_menu("=> todo_list")
            print_menu("=> block_user")
            print_menu("=> unblock_user")
            print_menu("=> logout")
        elif session_user.role == models.UserRole.SUPER_ADMIN.value:
            print_menu("=> create_todo")
            print_menu("=> update_todo")
            print_menu("=> delete_todo")
            print_menu("=> todo_list")
            print_menu("=> block_admin")
            print_menu("=> unblock_admin")
            print_menu("=> logout")
        print_menu("=> quit")
        choice = input("> ?: ")
        match choice:
            case "login":
                login()
            case "register":
                register()
            case "logout":
                logout()
            case "create_todo":
                create_todo()
            case "update_todo":
                update_todo()
            case "delete_todo":
                delete_todo()
            case "block_user":
                block_user()
            case "unblock_user":
                unblock_user()
            case "block_admin":
                block_admin()
            case "unblock_admin":
                unblock_admin()
            case "quit":
                exit(0)
            case _:
                print_error("Wrong choice")


if __name__ == '__main__':
    menu()
