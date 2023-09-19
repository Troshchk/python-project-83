import pytest
import datetime
from page_analyzer.url import URL
from page_analyzer.db_manager import DB_manager
from page_analyzer.page_analyser import Page_analyzer
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
    yield db
    janitor.drop()


@pytest.mark.parametrize("url", ["https://www.google.de"])
def test_page_analyzer(url, database):
    db_manager = DB_manager(connection=database)
    page_analyzer = Page_analyzer(db_manager=db_manager)
    all_urls = page_analyzer.format_all_urls_to_show()
    assert len(all_urls) == 2
    assert page_analyzer.add_new_url_to_db(URL(url)) == 3
    all_urls = page_analyzer.format_all_urls_to_show()
    print(all_urls)
    assert len(all_urls) == 3
    assert all_urls[0].created_at == datetime.date.today()
    assert all_urls[0].name == "https://www.google.de"
    ind_url = page_analyzer.format_ind_url_to_show(1)
    assert ind_url[0].created_at == datetime.date(2023, 9, 14)
    assert ind_url[0].name == "https://www.google.com"
    assert ind_url[1] == []
    status_code, response = page_analyzer.check_url(1)
    assert status_code == 200
    page_analyzer.insert_check_to_db(1, response)
    ind_url = page_analyzer.format_ind_url_to_show(1)
    checks = ind_url[1][0]
    assert checks.status_code == status_code
    assert checks.url_id == 1
    assert checks.title == "Google"
    page_analyzer.add_new_url_to_db(URL("http://www.studio404.net"))
    status_code, response = page_analyzer.check_url(4)
    assert status_code == 404
    page_analyzer.add_new_url_to_db(URL("https://www.google.uk"))
    status_code, response = page_analyzer.check_url(5)
    assert status_code == 404
    assert response == None
