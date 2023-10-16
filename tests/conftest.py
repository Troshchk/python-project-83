import psycopg2
import os


DATABASE_URL = os.getenv("DATABASE_URL")
LOCAL = os.getenv("LOCAL_TESTS", default=False)


def set_path_to_fixture(LOCAL):
    if LOCAL:
        path_to_fixture = "tests/fixtures/"
    else:
        path_to_fixture = "code/tests/fixtures/"
    return path_to_fixture


def db_setup():
    db = psycopg2.connect(DATABASE_URL)
    if LOCAL:
        with open(f"{set_path_to_fixture(LOCAL)}test_setup_create.sql") as f:
            setup_sql = f.read()
        with open(f"{set_path_to_fixture(LOCAL)}test_setup_insert.sql") as f:
            setup_sql = setup_sql + f.read()
    else:
        with open(f"{set_path_to_fixture(LOCAL)}test_setup_insert.sql") as f:
            setup_sql = f.read()
    with db.cursor() as cursor:
        cursor.execute(setup_sql)
        db.commit()


def db_teardown():
    if LOCAL:
        db = psycopg2.connect(DATABASE_URL)
        with open(f"{set_path_to_fixture(LOCAL)}test_teardown.sql") as f:
            teardown_sql = f.read()
        with db.cursor() as cursor:
            cursor.execute(teardown_sql)
            db.commit()
