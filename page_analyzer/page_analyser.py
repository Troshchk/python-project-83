import requests
from bs4 import BeautifulSoup
from collections import namedtuple

URL_TO_SHOW = namedtuple(
    "URL",
    [
        "id",
        "name",
        "created_at",
        "last_check_created_at",
        "last_check_status_code",
    ],
)


class Page_analyzer:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def url_in_db(self, url):
        record = self.db_manager.get_record_by_url_name(url.url)
        if record:
            return record.id
        return None

    def add_new_url_to_db(self, url):
        self.db_manager.insert_url_to_db(url.url)
        record = self.db_manager.get_record_by_url_name(url.url)
        return record.id

    def format_all_urls_to_show(self):
        urls = self.db_manager.get_all_urls()
        urls_to_show = []
        for url in urls:
            check = self.db_manager.get_last_check(url)
            if check:
                check_created_at = check.created_at or ""
                check_status_code = check.status_code or ""
            else:
                check_created_at = ""
                check_status_code = ""
            urls_to_show.append(
                URL_TO_SHOW(
                    url.id,
                    url.name,
                    url.created_at,
                    check_created_at,
                    check_status_code,
                )
            )
        return urls_to_show

    def format_ind_url_to_show(self, id):
        url_to_show = self.db_manager.get_record_by_url_id(id)
        checks = self.db_manager.get_checks_info_by_url_id(id)
        return (url_to_show, checks)

    def check_url(self, id):
        url_to_query = self.db_manager.get_record_by_url_id(id)
        url_to_query = url_to_query.name
        try:
            response = requests.get(url_to_query)
            status_code = response.status_code
        except:
            response = None
            status_code = 404
        return status_code, response

    def _format_reponse_for_db(self, response):
        response_text = BeautifulSoup(response.text, "html.parser")
        title = response_text.title.string if response_text.title else ""
        h1 = response_text.h1.string if response_text.h1 else ""
        description = (
            response_text.meta.get("content", "") if response_text.meta else ""
        )
        return h1, title, description

    def insert_check_to_db(self, id, response):
        h1, title, description = self._format_reponse_for_db(response)
        self.db_manager.insert_check_to_db(
            id, response.status_code, h1, title, description
        )