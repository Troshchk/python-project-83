import page_analyzer.app as app
import pytest


def test_initial():
    response = app.test_client().get('/')
    assert response.status_code == 200
