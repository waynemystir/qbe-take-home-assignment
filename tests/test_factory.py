"""Pytest for the Flask app factory"""

from qbe_tha.app import create_app


def test_config():
    """Test create_app without and with passing test config."""
    assert create_app().testing is False
    assert create_app({"TESTING": True}).testing is True
