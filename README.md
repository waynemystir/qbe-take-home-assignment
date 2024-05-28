# qbe-take-home-assignment-03

## System requirementes

- Ubuntu 20.04 or later
- Python 3.8 or later
- Redis 7.0.15

To install Redis, follow [these steps](INSTALL_REDIS.md).

## Setup
Clone this repository. Then, from the root of this local repository, run this:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Run the API
From the root of this repository, run this:
```
. .venv/bin/activate
flask --app qbe_tha run
```

## Try out the API
From the subdirectory `tests-curl`, you can run this:
```
bash post-validate.sh
```
Or this:
```
bash post-get-factors.sh
```
You can also experiment with the file `data-wo-factors.json` to verify that the API returns appropriate errors.


## Run the tests
From the root of this repository, run this:
```
. .venv/bin/activate
coverage run -m pytest
```

To view the coverage of the tests:
```
coverage report
```

To view detailed coverage of the tests:
```
coverage html  # open htmlcov/index.html in a browser
```
You should achieve 99% test coverage.
