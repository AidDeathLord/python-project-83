import psycopg2
from dotenv import load_dotenv
import datetime
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db():
    try:
        con = connect(DATABASE_URL)
    except psycopg2.OperationalError:
        return None
    return con


# добавляем ссылки в базу и возвращаем ее id
def add_url(url: str) -> int:
    con = connect_db()
    cur = con.cursor()
    sql = """INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id;"""
    cur.execute(sql, (url, datetime.date.today()))
    result = cur.fetchone()[0]
    cur.close()
    con.commit()
    con.close()
    return result


# возвращаем id сайта если он существует в базе данных
def check_url(url: str) -> (int, None):
    con = connect_db()
    cur = con.cursor()
    sql = """SELECT id
             FROM urls
             WHERE name = %s;"""
    cur.execute(sql, (url,))
    result = cur.fetchone()
    cur.close()
    con.close()
    if result:
        return result[0]


# получаем инфу из таблицы urls по id ссылки
def get_url_info_by_id(url_id):
    con = connect_db()
    cur = con.cursor(cursor_factory=NamedTupleCursor)
    sql = "SELECT name, created_at FROM urls WHERE id = %s;"
    cur.execute(sql, (url_id,))
    result = cur.fetchone()
    cur.close()
    con.close()
    return result


# получаем все ссылки
# сгруппированные по последней проверке
def get_all_urls():
    con = connect_db()
    cur = con.cursor(cursor_factory=NamedTupleCursor)
    result = []
    sql = """SELECT
                urls.id AS id,
                urls.name AS name,
                MAX(checks.created_at) AS last_check,
                checks.status_code
            FROM urls
            LEFT JOIN urls_checks AS checks
                ON urls.id = checks.url_id
            GROUP BY urls.id, checks.status_code
            ORDER BY id DESC;"""
    cur.execute(sql)
    result.extend(cur.fetchall())
    cur.close()
    con.close()
    return result


# записываем результат проверки
def add_check(url_id, status_code, h1, title, content):
    con = connect_db()
    cur = con.cursor()
    sql = """INSERT INTO urls_checks
             (url_id, status_code, created_at, h1, title, description)
             VALUES
             (%s, %s, %s, %s, %s, %s);"""
    cur.execute(sql, (url_id,
                      status_code,
                      datetime.date.today(),
                      h1,
                      title,
                      content))
    cur.close()
    con.commit()
    con.close()


# получаем все проверки по id
def get_all_checks_for_url(url_id):
    con = connect_db()
    cur = con.cursor(cursor_factory=NamedTupleCursor)
    sql = "SELECT * FROM urls_checks WHERE url_id = %s ORDER BY id DESC;"
    cur.execute(sql, (url_id,))
    result = []
    result.extend(cur.fetchall())
    cur.close()
    con.close()
    return result
