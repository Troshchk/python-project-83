import page_analyzer.app as app
import pytest
import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")
LOCAL = os.getenv("LOCAL_TESTS", default=False)


def set_path_to_fixture(LOCAL):
    if LOCAL:
        path_to_fixture = "tests/fixtures/"
    else:
        path_to_fixture = "code/tests/fixtures/"
    return path_to_fixture


def setup_module():
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


def teardown_module():
    if LOCAL:
        db = psycopg2.connect(DATABASE_URL)
        with open(f"{set_path_to_fixture(LOCAL)}test_teardown.sql") as f:
            teardown_sql = f.read()
        with db.cursor() as cursor:
            cursor.execute(teardown_sql)


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
