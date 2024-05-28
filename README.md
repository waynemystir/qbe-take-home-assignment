## System requirements

- Ubuntu 20.04 or later
- Python 3.8 or later
- Redis 7.0.15

To install Redis, follow [these steps](INSTALL_REDIS.md).

NOTE to M.M.: I actually developed this repository while working on my Chromebook because I'm not at home right now (where my Ubuntu desktop is). The developer mode on Chromebook uses a container that it calls `penguin`. It's Debian and seems very, very close to Ubuntu. The app and pytests work as expected on my Chromebook. I will be home in a couple days and will verify that the app and tests work on Ubuntu then. I don't expect any problems. I greatly appreciate you extending the deadline. I'm confident that this repository is ready for your evaluation and wanted to submit it ASAP.

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
You should see 19 tests passed successfully and no failures.

To view the coverage of the tests:
```
coverage report
```
You should achieve 99% test coverage.

To view detailed coverage of the tests:
```
coverage html  # open htmlcov/index.html in a browser
```


## Git commands and workflow

I implemented trunk-based development:
- Created a new repository in GitHub
- Created a main branch for the base code
- Created feature branches for each part of the assignment
- Merged small, frequent Pull Requests (PRs) to main
- For PRs, I typically like to follow [these best practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests).

To create the repository and initialize it, I selected `New` in GitHub, included a basic README, and finished the repository creation page. Once the remote repository was created in GitHub, I got the origin URL by selecting `Code` -> `SSH` -> and the copy icon. I then cloned this new repository to my local computer with this command:
```
git clone git@github.com:waynemystir/qbe-take-home-assignment.git
```
NOTE: using the SSH option works because I have previously [created an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and then [added it to my GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

To create a feature branch, I started at the main branch (at the root of the local repository) and ran commands such as this:
```
git status # make sure you're on the main branch
git pull # make sure you have the latest
git checkout -b feature/add-tests # create feature branch from main
```

I typically like to commit often throughout the day for a couple reasons. I can more easily track my progress and it makes `git diff` much smaller and easier to see where I might have made a recent mistake or created a bug (using TDD).

I used [black](https://pypi.org/project/black/) for code formatting with this command:
```
black .
```

To commit the latest from a local feature branch to the origin:
```
black .
git add .
git commit -m "write a short message to describe what you're committing"
git push origin HEAD
```

After the first commit for a new feature branch, I go to this repository in GitHub and create a Pull Request for that branch. GitHub makes this easy because it automatically detects that a branch has new commits. When creating the PR, I add a meaningful title and short description. I will typically also add the reviewers, assignees, and labels at this time. I then continue adding and pushing commits until I am done with the PR.

NOTE: Ordinarily I would delete the feature branches when they're merged to `main`. But I didn't do that here in order to keep the history for M.M. to review.
