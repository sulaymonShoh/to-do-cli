import sqlite3
import time
import utils, models
from os.path import exists

db = "db.sqlite"
# while not exists(db):
#     print(db, "does not exist")
#     time.sleep(1)

connection = sqlite3.connect(db)
cursor = connection.cursor()


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        connection.commit()
        return result

    return wrapper


create_table_users_sql = """
create table if not exists users (
    id integer primary key autoincrement,
    username varchar(60) unique not null,
    password varchar(60) not null,
    status varchar(20) not null,
    role varchar(20) not null,
    login_try_count int default 0
)
"""

create_todo_sql = """
create table if not exists todos (
    id integer PRIMARY KEY AUTOINCREMENT,
    name varchar(30) not null,
    type varchar(30) not null,
    completer bool default false,
    user_id int references users(id)
)
"""

insert_into_sql = """
    insert into users (username, password, status, role) values (?, ?, ?, ?)
"""


@commit
def init():
    cursor.execute(create_table_users_sql)
    cursor.execute(create_todo_sql)


@commit
def create_admin():
    cursor.execute(insert_into_sql, ("john",
                                     utils.encode_password("123"),
                                     models.UserStatus.ACTIVE.value,
                                     models.UserRole.ADMIN.value
                                     ))


def get_user_by_username(username):
    get_user_sql = """
        select id, username, status, role, login_try_count from users where username=?
"""
    cursor.execute(get_user_sql, (username,))
    user_data = cursor.fetchone()
    return user_data


if __name__ == '__main__':
    # init()
    # create_admin()
    print(get_user_by_username("john"))
