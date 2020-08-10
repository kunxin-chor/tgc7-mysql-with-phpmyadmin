import pymysql
import os

conn = pymysql.connect(
    host=os.environ.get('IP'),
    user=os.environ.get('C9_USER'),
    password="",
    database="classicmodels"
)


def create_cursor():
    return conn.cursor(pymysql.cursors.DictCursor)


def get_all_employees():
    cursor = create_cursor()
    cursor.execute("select * from employees")
    return cursor
