import page_analyzer.app as app
import pytest
import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")


def setup_module():
    db = psycopg2.connect(DATABASE_URL)
    with open("./tests/fixtures/test_setup.sql") as f:
        setup_sql = f.read()
    with db.cursor() as cursor:
        cursor.execute(setup_sql)
        db.commit()


def teardown_module():
    db = psycopg2.connect(DATABASE_URL)
    with open("./tests/fixtures/test_teardown.sql") as f:
        teardown_sql = f.read()
    with db.cursor() as cursor:
        cursor.execute(teardown_sql)
        db.commit()


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
    print(os.listdir("./tests"))
    print(os.listdir("./tests/fixtures"))
    response = app.test_client().post("/urls", data={"url": url})
    assert response.status_code == expected
