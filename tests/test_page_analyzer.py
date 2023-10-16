import datetime
from page_analyzer.url import URL
from page_analyzer.db_manager import DB_manager
from page_analyzer.page_analyser import Page_analyzer
import os
from conftest import db_setup, db_teardown
import pytest

DATABASE_URL = os.getenv("DATABASE_URL")


@pytest.fixture()
def db_resource():
    print("setup")
    db_setup()
    yield "db_resource"
    print("teardown")
    db_teardown()


class Test_page_analyzer:
    db_manager = DB_manager(DATABASE_URL=DATABASE_URL)
    page_analyzer = Page_analyzer(db_manager=db_manager)

    def test_starting_state(self, db_resource):
        all_urls = self.page_analyzer.format_all_urls_to_show()
        assert len(all_urls) == 2

    def test_adding_new_url(self, db_resource):
        self.page_analyzer.add_new_url_to_db(URL("https://www.google.de"))
        all_urls = self.page_analyzer.format_all_urls_to_show()
        assert len(all_urls) == 3
        last_url = all_urls[0]
        assert last_url.created_at == datetime.date.today()
        assert last_url.name == "https://www.google.de"

    def test_first_url_data(self, db_resource):
        all_urls = self.page_analyzer.format_all_urls_to_show()
        first_url_id = all_urls[-1].id
        first_url_with_all_info = self.page_analyzer.format_ind_url_to_show(first_url_id)
        first_url_info = first_url_with_all_info[0]
        first_url_checks = first_url_with_all_info[1]
        assert first_url_info.created_at == datetime.date(2023, 9, 14)
        assert first_url_info.name == "https://www.google.com"
        assert first_url_checks == []

    def test_adding_url_check(self, db_resource):
        all_urls = self.page_analyzer.format_all_urls_to_show()
        first_url_id = all_urls[-1].id
        status_code, response = self.page_analyzer.check_url(first_url_id)
        assert status_code == 200
        self.page_analyzer.insert_check_to_db(first_url_id, response)
        first_url_with_all_info = self.page_analyzer.format_ind_url_to_show(first_url_id)
        first_url_checks = first_url_with_all_info[1]
        check = first_url_checks[0]
        assert check.status_code == status_code
        assert check.title == "Google"

    def test_404_check_response(self, db_resource):
        self.page_analyzer.add_new_url_to_db(URL("http://www.studio404.net"))
        all_urls = self.page_analyzer.format_all_urls_to_show()
        last_url_id = all_urls[0].id
        status_code, _ = self.page_analyzer.check_url(last_url_id)
        assert status_code == 404

    def test_failed_check_output(self, db_resource):
        self.page_analyzer.add_new_url_to_db(URL("https://www.google.uk"))
        all_urls = self.page_analyzer.format_all_urls_to_show()
        last_url_id = all_urls[0].id
        status_code, response = self.page_analyzer.check_url(last_url_id)
        assert status_code is None
        assert response is None
