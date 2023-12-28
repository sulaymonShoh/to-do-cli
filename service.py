from db import commit
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
    user.status=models.UserStatus.ACTIVE.value
    return utils.ResponseDate(user)


def register_user(username: str, password1, password2):
    if password1 != password2:
        return utils.ResponseDate("Bad Reqeust password is not match", False)
    if db.check_username_unique(username):
        return utils.ResponseDate("Bad Request this username already taken", False)
    user = models.User(username, utils.encode_passrord(password1))
    db.register_user(user)
    return utils.ResponseDate("User Successfuly registered")


def create_todo_service(todo:models.Todo):
    db.insert_to_todo_item(todo)
    return utils.ResponseDate("Todo Successfully created")