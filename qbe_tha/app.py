import json

from flask import Flask

from .config import Config
from .redis_client import init_redis, redis_store
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    # Initialize Redis
    init_redis(app)

    # Register Blueprints
    app.register_blueprint(bp)

    # Load the JSON file and store it in Redis
    with app.app_context():
        with open("data.json", "r") as f:
            data_dct = json.load(f)

        data_lst = data_dct["data"]
        valid_var_names = {"country", "age_group"}
        for dct in data_lst:
            var_name = dct["var_name"]
            category = dct["category"]
            factor = dct["factor"]
            assert var_name in valid_var_names, f"{var_name=} is not valid"
            assert isinstance(factor, float), f"{factor=} is not a float"
            vnc = var_name + category
            already_exists = redis_store.exists(vnc)
            if already_exists:
                val = float(redis_store.get(vnc))
                assert (
                    val == factor
                ), f"{val=} =/= {factor=} for {var_name=} and {category=}"
            else:
                redis_store.set(vnc, factor)

    return app
