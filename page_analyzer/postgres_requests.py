from dotenv import load_dotenv
import datetime
import psycopg2
from psycopg2.extras import DictCursor
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


def get_url_info_by_id(url_id: str) -> tuple:
    with conn.cursor() as cur:
        sql = """SELECT name, created_at
                 FROM urls
                 WHERE id = %s;"""
        cur.execute(sql, (url_id,))
        result = cur.fetchone()
        return result


def get_all_urls():
    with conn.cursor(cursor_factory=DictCursor) as cur:
        sql = "SELECT * FROM urls ORDER BY id DESC;"
        cur.execute(sql)
        result = []
        for row in cur:
            result.append({'id': row['id'], 'name': row['name']})

    return result
