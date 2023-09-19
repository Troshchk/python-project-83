import page_analyzer.app as app
import pytest
import os
from pytest_postgresql.janitor import DatabaseJanitor
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture
def database(postgresql_proc):
    janitor = DatabaseJanitor(
        postgresql_proc.user,
        postgresql_proc.host,
        postgresql_proc.port,
        "my_test_database",
        postgresql_proc.version,
        password="secret_password",
    )
    janitor.init()
    db = psycopg2.connect(DATABASE_URL)
    with open("test.sql") as f:
        setup_sql = f.read()
    with db.cursor() as cursor:
        cursor.execute(setup_sql)
        db.commit()
    yield db
    janitor.drop()


def test_initial():
    response = app.test_client().get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.google.com", 302),
        ("https://www.google.com/?page", 302),
        (
            "https://www.goooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooogle.com",
            422,
        ),
        ("https://www.google.de", 302),
    ],
)
def test_post_url(url, expected):
    response = app.test_client().post("/urls", data={"url": url})
    assert response.status_code == expected
