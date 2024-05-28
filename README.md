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


## Git commands and workflow

We implemented trunk-based development:
- Created a new repository in GitHub
- Created a main branch for the base code
- Created feature branches for each part of the assignment
- Merged small, frequent updates to main
- Merged to main via Pull Requests (PRs)

To create the repository and initialize it, I selected `New` in GitHub, included a basic README, and finished the repository creation page. Once the remote repository was created in GitHub, I got the origin URL by selecting `Code` -> `SSH` -> and the copy icon. I then cloned this new repository to my local computer with this command:
```
git clone git@github.com:waynemystir/qbe-take-home-assignment.git
```
NOTE: using the SSH option works because I have previously [created an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and then [added it to my GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
