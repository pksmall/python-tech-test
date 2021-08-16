import re
import sqlite3

from flask import current_app

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_short_url_popular():
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('SELECT original_url, count(distinct original_url) as cnt FROM urls '
              'GROUP BY original_url order by cnt LIMIT 10')
  rows = cur.fetchall()

  conn.commit()
  conn.close()

  populars = []
  for row in rows:
    populars.append(row['original_url'])

  return populars


def get_short_url_count():
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('SELECT  count(DISTINCT original_url)  as cnt FROM urls')
  rows = cur.fetchall()

  conn.commit()
  conn.close()

  count = 0
  for row in rows:
    count = row['cnt']
  return count


def get_short_url(url):
  conn = get_db_connection()

  url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
  conn.commit()
  conn.close()

  hashids = current_app.config['hashids']
  url_id = url_data.lastrowid
  hashid = hashids.encode(url_id)
  print(hashid)

  return hashid


def get_db_connection():
  conn = sqlite3.connect('../database.db')
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  connection = sqlite3.connect('../database.db')

  with open('./tools/shorten.sql') as f:
    connection.executescript(f.read())

  connection.commit()
  connection.close()
