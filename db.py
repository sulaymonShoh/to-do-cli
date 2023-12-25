import sqlite3
import time
from os.path import exists

db = "db.sqlite"
while not exists(db):
    print(db, "does not exist")
    time.sleep(1)

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
    id serial PRIMARY KEY,
    username varchar(60),
    password varchar(60),
    status varchar(20),
    role varchar(20),
    login_try_count int default 0
)
""" 

create_todo_sql = """
create table if not exists todos (
    id serial PRIMARY KEY,
    name varchar(30),
    type varchar(30),
    completer bool default false,
    user_id int references users(id)
)
"""


@commit
def init():
    cursor.execute(create_table_users_sql)
    cursor.execute(create_todo_sql)


if __name__ == '__main__':
    init()
