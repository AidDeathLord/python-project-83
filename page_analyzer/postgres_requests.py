from dotenv import load_dotenv
import datetime
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
CONN = psycopg2.connect(DATABASE_URL)
CURS = CONN.cursor()


def add_url(url):
    insert_query = """INSERT INTO urls (name, created_at) 
                      VALUES (%s, %s)
                      RETURNING id"""
    item_create_time = datetime.date.today()
    item_tuple = (url, item_create_time)
    CURS.execute(insert_query, item_tuple)
    result = CURS.fetchone()
    return result


def check_url(url):
    insert_query = """SELECT id
                      FROM urls
                      WHERE name = %s"""
    item_tuple = url
    CURS.execute(insert_query, item_tuple)
    result = CURS.fetchone()
    return result


def get_url_info_by_id(url_id):
    insert_query = """SELECT name, created_at
                      FROM urls
                      WHERE id = %s"""
    CURS.execute(insert_query, (url_id,))
    result = CURS.fetchone()
    print(result)
    return result
