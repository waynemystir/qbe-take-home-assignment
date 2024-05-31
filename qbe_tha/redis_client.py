"""Instantiate and initialize the Redis Store"""

from flask_redis import FlaskRedis

redis_store = FlaskRedis()


def init_redis(app):
    """
    Initialize the Flask app with the Redis store
    """
    redis_store.init_app(app)
