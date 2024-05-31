"""Define and implement the pytest fixtures needed by the tests"""

import json

import pytest

from qbe_tha.app import create_app


@pytest.fixture
def app():
    """Create a new app instance for each test."""
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def src_data():
    """The data from data.json"""
    with open("data.json", "r") as f:
        data = json.load(f)
    return data


@pytest.fixture
def src_data_wo_factors():
    """The data from data.json without the factors"""
    with open("data.json", "r") as f:
        data = json.load(f)

    dwf_data = []
    data_without_factors = {"data": dwf_data}
    for dj in data["data"]:
        assert isinstance(dj, dict)
        assert "factor" in dj
        dj.pop("factor")
        dwf_data.append(dj)
    return data_without_factors
