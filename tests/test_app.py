import page_analyzer.app as app
import pytest
from conftest import db_setup, db_teardown


@pytest.fixture()
def db_resource():
    print("setup")
    db_setup()
    yield "db_resource"
    print("teardown")
    db_teardown()


def test_initial(db_resource):
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
def test_post_url(url, expected, db_resource):
    response = app.test_client().post("/urls", data={"url": url})
    assert response.status_code == expected
