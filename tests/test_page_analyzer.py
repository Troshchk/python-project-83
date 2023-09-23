import pytest
import datetime
from page_analyzer.url import URL
from page_analyzer.db_manager import DB_manager
from page_analyzer.page_analyser import Page_analyzer
import psycopg2
from pytest_postgresql.janitor import DatabaseJanitor
import os

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
            db.commit()


def test_page_analyzer():
    db_manager = DB_manager(connection=psycopg2.connect(DATABASE_URL), DATABASE_URL=DATABASE_URL)
    page_analyzer = Page_analyzer(db_manager=db_manager)
    all_urls = page_analyzer.format_all_urls_to_show()
    assert len(all_urls) == 2
    page_analyzer.add_new_url_to_db(URL("https://www.google.de"))
    all_urls = page_analyzer.format_all_urls_to_show()
    assert len(all_urls) == 3
    last_url = all_urls[0]
    assert last_url.created_at == datetime.date.today()
    assert last_url.name == "https://www.google.de"
    first_url_id = all_urls[-1].id
    first_url_with_all_info = page_analyzer.format_ind_url_to_show(first_url_id)
    first_url_info = first_url_with_all_info[0]
    first_url_checks = first_url_with_all_info[1]
    assert first_url_info.created_at == datetime.date(2023, 9, 14)
    assert first_url_info.name == "https://www.google.com"
    assert first_url_checks == []
    status_code, response = page_analyzer.check_url(first_url_id)
    assert status_code == 200
    page_analyzer.insert_check_to_db(first_url_id, response)
    first_url_with_all_info = page_analyzer.format_ind_url_to_show(first_url_id)
    first_url_checks = first_url_with_all_info[1]
    check = first_url_checks[0]
    assert check.status_code == status_code
    assert check.title == "Google"
    page_analyzer.add_new_url_to_db(URL("http://www.studio404.net"))
    all_urls = page_analyzer.format_all_urls_to_show()
    last_url_id = all_urls[0].id
    status_code, response = page_analyzer.check_url(last_url_id)
    assert status_code == 404
    page_analyzer.add_new_url_to_db(URL("https://www.google.uk"))
    all_urls = page_analyzer.format_all_urls_to_show()
    last_url_id = all_urls[0].id
    status_code, response = page_analyzer.check_url(last_url_id)
    assert status_code == None
    assert response == None
