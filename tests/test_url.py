import pytest
from page_analyzer.url import URL
import validators


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
    assert (
        isinstance(URL(url).is_valid(), validators.utils.ValidationError)
        == expected
    )
