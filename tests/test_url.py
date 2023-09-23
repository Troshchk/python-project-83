import pytest
from page_analyzer.url import URL
import validators
import psycopg2
from pytest_postgresql.janitor import DatabaseJanitor
import os

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


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.google.com", False),
        ("not_valid", True),
        (
            "https://www.goooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooogle.com",
            True,
        ),
    ],
)
def test_url_formatting(url, expected):
    print(type(URL(url).is_valid()))
    assert (
        isinstance(URL(url).is_valid(), validators.utils.ValidationError)
        == expected
    )
