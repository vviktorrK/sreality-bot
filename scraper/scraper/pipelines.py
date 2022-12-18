import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class SrealityPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(host='postgres_db', user='postgres', password='password')
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        self.cur = self.conn.cursor()

        self.cur.execute("DROP DATABASE IF EXISTS sreality_bot")
        self.cur.execute("CREATE DATABASE sreality_bot")
        self.cur.close()

        self.conn = psycopg2.connect(host='postgres_db', user='postgres', password='password', database='sreality_bot')
        self.cur = self.conn.cursor()

        self.cur.execute("DROP TABLE IF EXISTS apartments")
        self.cur.execute("""
        CREATE TABLE apartments(
            id serial PRIMARY KEY,
            title varchar (150),
            image_url varchar (200)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(""" INSERT INTO apartments (title, image_url) VALUES (%s,%s)""", (
            item["title"],
            item["image_url"]
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()