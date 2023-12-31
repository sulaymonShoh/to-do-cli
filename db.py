import sqlite3
import time
from os.path import exists

import models
import utils

# import models

db = "db.sqlite"
while not exists(db):
    print(db, "-- > doesnot exists")
    time.sleep(1)

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        connection.commit()
        return result

    return wrapper


create_user_table_sql = """
    create table if not exists users(
        id integer primary key autoincrement,
        username varchar(40) unique not null,
        password varchar(60) not null,
        status varchar(20) not null,
        role varchar(20) not null,
        login_try_count int default 0
    )
"""
create_todo_sql = """
    create table if not exists todos(
        id integer primary key autoincrement,
        name varchar(30) not null,
        type varchar(20) not null,
        completed bool default false,
        user_id int references users(id)
)
"""


@commit
def create_todo_init():
    insert_todo_sql = """
    insert into todos(name, type,user_id) values (?,?,?);
    """
    cursor.execute(insert_todo_sql, ('Study English', "STUDY", 1))


@commit
def init():
    cursor.execute(create_user_table_sql)
    cursor.execute(create_todo_sql)


inser_into_sql = """
    insert into users(username, password, status, role) values (?,?,?,?)
"""


@commit
def create_admin():
    cursor.execute(inser_into_sql, ("john",
                                    utils.encode_passrord("123"),
                                    models.UserStatus.ACTIVE.value,
                                    models.UserRole.ADMIN.value
                                    ))


@commit
def update_to_zero_login_try_count(username: str):
    update_to_zero = "update users set login_try_count=0 where username=?"
    cursor.execute(update_to_zero, (username,))


@commit
def increase_user_try_count(username):
    increase_try_count_sql = """update users set login_try_count=login_try_count+1 where username=? """
    cursor.execute(increase_try_count_sql, (username,))


def check_username_unique(username) -> bool:
    check_sql_unique = """select count(*) from users where username= ?;"""
    cursor.execute(check_sql_unique, (username,))
    return cursor.fetchone()[0]


def get_user_by_username(username: str):
    get_user_sql = "select id, username, password, status, role, login_try_count from users where username=?"
    cursor.execute(get_user_sql, (username,))
    user_data = cursor.fetchone()
    return user_data


@commit
def update_user_status(username: str):
    update_user_status_to_active = """update users set status=? where username=?"""
    cursor.execute(update_user_status_to_active, (models.UserStatus.ACTIVE.value, username))


@commit
def update_user_status_to_inactive(username: str):
    update_user_status_to_inactive_sql = """update users set status=? where username=?"""
    cursor.execute(update_user_status_to_inactive_sql, (models.UserStatus.IN_ACTIVE.value, username))


@commit
def block_user(username: str):
    block_user_sql = """update users set status=? where username=?"""
    cursor.execute(block_user_sql, (models.UserStatus.BLOCKED.value, username))


@commit
def register_user(user):
    inser_into_user_sql = """insert into users(id, username, password,status, role, login_try_count) values (?,?,?,?,?,?)"""
    cursor.execute(inser_into_user_sql,
                   (user.id, user.username, user.password, user.status, user.role, user.login_try_count))


def get_user_id():
    user_id_seqence = """select seq from sqlite_sequence where name ='users';"""
    cursor.execute(user_id_seqence)
    id = 1 + cursor.fetchone()[0]
    return id


def get_todo_id():
    user_id_seqence = """select seq from sqlite_sequence where name ='todos';"""
    cursor.execute(user_id_seqence)
    id = 1 + cursor.fetchone()[0]
    return id


@commit
def insert_to_todo_item(todo):
    insert_todo_sql = """insert into todos(id,name, type, completed, user_id ) values (?,?,?,?,?)"""
    cursor.execute(insert_todo_sql, (todo.id, todo.name, todo.type, todo.completed, todo.user_id))


def get_todo_info(user_id, todo_id):
    get_todo_info_sql = """select * from todos where id=? and user_id=?"""
    cursor.execute(get_todo_info_sql, (todo_id, int(user_id),))
    return cursor.fetchone()


def get_todo_title(user_id, todo_id):
    get_todo_title_sql = """select name from todos where id=? and user_id=?"""
    cursor.execute(get_todo_title_sql, (todo_id, user_id))
    return cursor.fetchone()[0]


def check_todo_completed(user_id, todo_id):
    check_todo_completed_sql = """select completed from todos where user_id = ? and id = ?"""
    cursor.execute(check_todo_completed_sql, (user_id, todo_id))
    return cursor.fetchone()


@commit
def update_todo_status(user_id, todo_id):
    update_todo_status_sql = """update todos set completed=? where user_id=? and id=?"""
    cursor.execute(update_todo_status_sql, (True, user_id, todo_id))


def get_todo_list(user_id):
    get_todo_list_sql = """select id, name, type, completed from todos where user_id=?"""
    cursor.execute(get_todo_list_sql, (user_id,))
    todos = cursor.fetchall()
    return todos


@commit
def unblock_user(username):
    unblock_user_sql = """update users set status=? where username=?"""
    cursor.execute(unblock_user_sql, (models.UserStatus.IN_ACTIVE.value, username))


# if __name__ == '__main__':
# create_todo_init()
# init()
# create_admin()
# print(get_user_by_username("john"))
@commit
def delete_todo(user_id, todo_id):
    delete_todo_sql = """delete from todos where user_id=? and id=?"""
    cursor.execute(delete_todo_sql, (user_id, todo_id))


# def check_user_role(username):
#     check_user_role_sql = """select role from users where username=?"""
#     cursor.execute(check_user_role_sql, (username,))
#     return cursor.fetchone()[0]


@commit
def block_admin(username):
    block_admin_sql = """update users set status=? where username=?"""
    cursor.execute(block_admin_sql, (models.UserStatus.BLOCKED.value, username))

@commit
def unblock_admin(username):
    unblock_admin_sql = """update users set status=? where username=?"""
    cursor.execute(unblock_admin_sql, (models.UserStatus.IN_ACTIVE.value,))
