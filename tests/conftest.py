import pytest


class MockResponse:

    def __init__(self, json_data, **kwargs):
        self._json = json_data

    def json(self):
        return self._json


@pytest.fixture
def mock_response():
    def inner(json_data):
        return MockResponse(json_data)
    return inner
