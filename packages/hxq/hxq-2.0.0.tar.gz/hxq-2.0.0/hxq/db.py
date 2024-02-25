# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 23:38
# @Author  : hxq
# @Software: PyCharm
# @File    : db.py
import time
from hxq.libs.db import DBHelper

__all__ = [
    "DBHelper",
]

if __name__ == '__main__':
    CONFIG = {
        'SQL_CREATOR': 'sqlite3',
        'SQL_DATABASE': r'blog.sqlite3'
    }
    db = DBHelper(config=CONFIG)
    # print(db.all("SHOW DATABASES;"))
    # print(db.all("select * from hxq"))
    create_table = '''
    CREATE TABLE hxq(
       ID INTEGER PRIMARY KEY AUTOINCREMENT,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL
    );
    '''
    start = time.time()
    data_list = []
    for i in range(1000000):
        data_list.append(('test', f'{i}'))
    sql = f"INSERT INTO hxq('NAME','AGE') VALUES ({db.get_placeholder()},{db.get_placeholder()})"
    db.executemany(sql, data_list)

    # print(db.execute(create_table))
    # with db.auto_commit(True) as cursor:
    #     for i in range(1000000):
    #         cursor.execute(f"INSERT INTO hxq('NAME','AGE') values('test','{i}')")

    print(db.execute("select count(*) from hxq"))
    # print(db.all("select * from hxq"))
    print(f"run time of the func is '%s' %.*f Ms{(time.time() - start) * 1000}")
    db.execute("DELETE FROM hxq;")
    db.execute("VACUUM ;")

    # print(db.execute(create_table))
    # print(db.execute(create_table1))
