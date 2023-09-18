from urllib.parse import urlparse
import validators


class URL:
    def __init__(self, url):
        self.input_url = url
        self.url = self._format_url_for_db(url)

    def _format_url_for_db(self, url):
        return (
            urlparse(url)
            ._replace(path="")
            ._replace(params="")
            ._replace(query="")
            ._replace(fragment="")
            .geturl()
        )

    def is_valid(self):
        return validators.url(self.input_url) and len(self.input_url) < 256
