from db import commit
from prettytable import PrettyTable
import db
import utils
import models


@commit
def login_user(username, password):
    user_data = db.get_user_by_username(username)
    if not user_data:
        return utils.ResponseDate("Bad Request user not found", False)
    user = models.User.from_tuple(user_data)
    if user.status == "BLOCKED":
        return utils.ResponseDate("Bad Credintials", False)
    if user.login_try_count >= 3:
        db.block_user(username)
        return utils.ResponseDate("Bad Credintials user tried 3 times", False)
    if not utils.match_password(password, user.password):
        db.increase_user_try_count(username)
        return utils.ResponseDate("Bad Credintials password wrong", False)
    if user.login_try_count != 0:
        db.update_to_zero_login_try_count(username)
    db.update_user_status(username)
    user.status = models.UserStatus.ACTIVE.value
    return utils.ResponseDate(user)


def register_user(username: str, password1, password2):
    if password1 != password2:
        return utils.ResponseDate("Bad Reqeust password is not match", False)
    if db.check_username_unique(username):
        return utils.ResponseDate("Bad Request this username already taken", False)
    user = models.User(username, utils.encode_passrord(password1))
    db.register_user(user)
    return utils.ResponseDate("User Successfuly registered")


def create_todo_service(todo: models.Todo):
    db.insert_to_todo_item(todo)
    return utils.ResponseDate("Todo Successfully created")


def todo_list_service(user_id):
    result = PrettyTable(["No", "ID", "Title", "Type", "Completed"])
    todos = db.get_todo_list(user_id)
    for i in range(len(todos)):
        result.add_row([i + 1, todos[i][0], todos[i][1], todos[i][2], todos[i][3]])

    return result


def block_user_service(username):
    userdata = db.get_user_by_username(username)
    user = models.User.from_tuple(userdata)
    if isinstance(user, models.User):
        if user.status == models.UserStatus.BLOCKED.value:
            response = utils.ResponseDate("User already blocked", False)
            return response

        db.block_user(user.username)
        response = utils.ResponseDate("User blocked")
        return response
    else:
        response = utils.ResponseDate("User does not exist", False)
        return response


def unblock_user_service(username):
    userdata = db.get_user_by_username(username)
    user = models.User.from_tuple(userdata)
    if isinstance(user, models.User):
        if user.status != models.UserStatus.BLOCKED.value:
            response = utils.ResponseDate("User is not blocked", False)
            return response

        db.unblock_user(user.username)
        db.update_to_zero_login_try_count(user.username)
        response = utils.ResponseDate("User unblocked")
        return response
    else:
        response = utils.ResponseDate("User does not exist", False)
        return response


def get_todo_info_service(user_id, todo_id):
    return models.Todo.from_tuple(db.get_todo_info(user_id, todo_id))


def check_todo_status(user_id, todo_id):
    response = db.check_todo_completed(user_id, todo_id)
    if response is None:
        return utils.ResponseDate("Todo does not exist", False)

    return response[0]


def update_todo_service(user_id, todo_id):
    todo_details = db.get_todo_info(user_id, todo_id)
    if not todo_details:
        return utils.ResponseDate("Todo does not exist", False)
    todo_details = db.get_todo_info(user_id, todo_id)
    todo = models.Todo.from_tuple(todo_details)
    if todo.completed:
        return utils.ResponseDate("Todo already completed", False)
    else:
        db.update_todo_status(user_id, todo_id)
        print(todo)
        return utils.ResponseDate(f'Todo "{todo.name}" completed successfully', True)


def delete_todo_service(user_id, todo_id):
    todo_details = db.get_todo_info(user_id, todo_id)
    if not todo_details:
        return utils.ResponseDate("Todo does not exist", False)
    todo = models.Todo.from_tuple(todo_details)
    if todo.completed:
        print(todo)
        db.delete_todo(user_id, todo_id)
        return utils.ResponseDate(f'Todo "{todo.name}" successfully deleted')
    else:
        return utils.ResponseDate("Bad Request you cannot delete this todo before it is completed", False)


def block_admin_service(username):
    admin = models.User.from_tuple(db.get_user_by_username(username))
    if admin is None:
        return utils.ResponseDate("User not found", False)
    elif admin.role == models.UserRole.ADMIN.value:
        if admin.status != models.UserStatus.BLOCKED.value:
            db.block_admin(username)
            return utils.ResponseDate("Admin blocked successfully")

        return utils.ResponseDate("Bad Request admin is already blocked", False)

    elif admin.role != models.UserRole.ADMIN.value:
        return utils.ResponseDate("Bad Request this user does not have admin rights", False)


def unblock_admin_service(username):
    admin = models.User.from_tuple(db.get_user_by_username(username))
    if admin is None:
        return utils.ResponseDate("Bad request ser not found", False)
    elif admin.role == models.UserRole.ADMIN.value:
        if admin.status == models.UserStatus.BLOCKED.value:
            db.unblock_admin(username)
            return utils.ResponseDate("Admin is unblocked succefully")

        return utils.ResponseDate("Bad Request admin is not blocked", False)

    elif admin.role != models.UserRole.ADMIN.value:
        return utils.ResponseDate("Bad Request this user does not have admin rights", False)
