from datetime import date
from psycopg2.extras import NamedTupleCursor
import psycopg2


class DB_manager:
    def __init__(self, DATABASE_URL):
        self.db_url = DATABASE_URL

    def connect(self):
        return psycopg2.connect(self.db_url)

    def get_record_by_url_name(self, url_name):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE name=%s", (url_name,))
            result = curs.fetchone()
        conn.close()
        return result

    def get_all_urls(self):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT id,name,created_at FROM urls ORDER BY id DESC")
            urls = curs.fetchall()
        conn.close()
        return urls

    def get_last_check(self, url_id):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "SELECT created_at,status_code FROM url_checks WHERE \
                     url_id=%s ORDER BY id DESC",
                (url_id,),
            )
            check = curs.fetchone()
        conn.close()
        return check

    def get_url_info_by_id(self, id):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM urls WHERE id=%s", (id,))
            url_to_show = curs.fetchall()
        conn.close()
        return url_to_show

    def get_checks_info_by_url_id(self, id):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT * FROM url_checks WHERE url_id=%s", (id,))
            checks = curs.fetchall()
        conn.close()
        return checks

    def get_record_by_url_id(self, id):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute("SELECT name,created_at FROM urls WHERE id=%s", (id,))
            name = curs.fetchone()
        conn.close()
        return name

    def insert_url_to_db(self, url):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "INSERT INTO urls(name, created_at) \
                        VALUES (%s, %s)",
                (
                    url,
                    date.today().isoformat(),
                ),
            )
        conn.commit()
        conn.close()

    def insert_check_to_db(self, id, status_code, h1, title, description):
        conn = self.connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                "INSERT INTO url_checks(url_id, created_at, \
                     status_code, h1, title, description) \
                     VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    id,
                    date.today().isoformat(),
                    status_code,
                    h1,
                    title,
                    description,
                ),
            )
        conn.commit()
        conn.close()
