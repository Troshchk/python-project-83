import page_analyzer.app as app
import pytest
import os
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")


def setup_module():
    db = psycopg2.connect(DATABASE_URL)
    setup_sql = """CREATE TABLE urls(
                            id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                            name varchar(255),
                            created_at date);


                        CREATE TABLE url_checks(
                            id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                            url_id bigint REFERENCES urls (id),
                            status_code int,
                            h1 varchar(255),
                            title varchar(255),
                            description text,
                            created_at date);


                        INSERT INTO urls(name, created_at) VALUES ('https://www.google.com', '2023-09-14');
                        INSERT INTO urls(name, created_at) VALUES ('http://docs.python.org:80', '2023-09-14');"""
    with db.cursor() as cursor:
        cursor.execute(setup_sql)
        db.commit()


def teardown_module():
    db = psycopg2.connect(DATABASE_URL)
    teardown_sql = """DROP TABLE IF EXISTS urls CASCADE;
                    DROP TABLE IF EXISTS url_checks;"""
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
    print(os.listdir())
    print(os.listdir("./tests"))
    print(os.listdir("./tests/fixtures"))
    response = app.test_client().post("/urls", data={"url": url})
    assert response.status_code == expected
