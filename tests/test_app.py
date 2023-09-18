import page_analyzer.app as app
import pytest


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
