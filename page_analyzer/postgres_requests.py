from dotenv import load_dotenv
import datetime
import psycopg2
from psycopg2.extras import NamedTupleCursor
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


# добавляем ссылки в базу и возвращаем ее id
def add_url(url: str) -> int:
    with conn.cursor() as cur:
        sql = """INSERT INTO urls (name, created_at) 
                 VALUES (%s, %s)
                 RETURNING id;"""
        cur.execute(sql, (url, datetime.date.today()))
        conn.commit()
        return cur.fetchone()[0]


# возвращаем id сайта если он существует в базе данных
def check_url(url: str) -> (int, None):
    with conn.cursor() as cur:
        sql = """SELECT id
                 FROM urls
                 WHERE name = %s;"""
        cur.execute(sql, (url,))
        result = cur.fetchone()
        if result:
            return result[0]


def get_url_info_by_id(url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        sql = """SELECT name, created_at
                 FROM urls
                 WHERE id = %s;"""
        cur.execute(sql, (url_id,))
        return cur.fetchone()


def get_all_urls():
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
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
    return result


def add_check(url_id, status_code):
    with conn.cursor() as cur:
        sql = """INSERT INTO urls_checks (url_id, status_code, created_at) 
                 VALUES (%s, %s, %s);"""
        cur.execute(sql, (url_id, status_code, datetime.date.today()))
        conn.commit()


def get_all_checks_for_url(url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        sql = "SELECT * FROM urls_checks WHERE url_id = %s ORDER BY id DESC;"
        cur.execute(sql, (url_id,))
        result = []
        result.extend(cur.fetchall())
    return result
