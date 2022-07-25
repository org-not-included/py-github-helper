# github_api
Python Script for interacting with Github API.

## Example
```shell
python3 helpers/make_api_call.py \
        -t $GH_TOKEN -o org-not-included -r github_api -l 1 -c add_comment \
        -e '{"message": "This message was successfully posted via gitub_api."}'
```

## Docs
```shell
python3 helpers/make_api_call.py --help
```


```text
usage: github_api_call [-h] [-o ORGANIZATION] [-r REPOSITORY] [-t TOKEN] [-u USERNAME] [-p PASSWORD] [-l PULL_REQUEST_ID] [-c COMMAND] [-e EXTRAS]

A python script that handles GitHub API calls.

optional arguments:
  -h, --help            show this help message and exit
  -o ORGANIZATION, --organization ORGANIZATION
                        Owner of GitHub repository.
  -r REPOSITORY, --repository REPOSITORY
                        Name of the GitHub repository.
  -t TOKEN, --token TOKEN
                        User's GitHub Personal Access Token.
  -u USERNAME, --username USERNAME, --user USERNAME
                        User's GitHub username.
  -p PASSWORD, --password PASSWORD, --pass PASSWORD
                        User's Github password.
  -l PULL_REQUEST_ID, --pull_request_id PULL_REQUEST_ID, --pull-request PULL_REQUEST_ID
                        The issue # of the Pull Request.
  -c COMMAND, --command COMMAND
                        Name of python function associated with API call being made.
  -e EXTRAS, --extras EXTRAS
                        Extra dictionary to allow for more arguments.

Expected Syntax:
        python3 github_api_call.py -o <Organization Name> -r <Repository> -t <O-Auth Token> -u <Github username> -p <Github password> -l <PR Number> -c <Github API Command> -e '{"x": "sample", "y": 5, "z": "test}'

Available Commands:

        - add_comment:
                Adds a single comment for a specified pull request.
                Required parameters: organization, repository, token, pull-request, extras[message]
        - add_labels:
                Adds a set of labels for a specified pull request.
                Required parameters: organization, repository, token, pull-request, extras[labels]
        - close_issue:
                Marks a specified issue as closed.
                Required parameters: organization, repository, token, extras[issue]
        - delete_labels:
                Deletes a set of labels for a specified pull request.
                Required parameters: organization, repository, token, pull-request, extras[labels]
        - dimiss_single_review:
                Dismisses a specific review for a specified pull request.
                Required parameters: organization, repository, token, pull-request, extras[review_id]
        - dismiss_all_reviews:
                Dismisses all reviews for a specified pull request.
                Required parameters: organization, repository, token, pull-request
        - get_commit_message:
                Gets a commit message, using the commit_id.
                Required parameters: organization, repository, token, pull-request, extras[commit_id]
        - get_deploy_issue_number:
                Parses for a Github issue titled 'Deploy Request: YYYY-MM-DD', and returns the associated issue id.
                Required parameters: organization, repository, token
        - get_prs_to_deploy:
                Parses for a Github issue titled 'Deploy Request: YYYY-MM-DD', and generates a list of mentioned PRs (in order of closed_at).
                Required parameters: organization, repository, token
        - label_merged_pr:
                Adds and/or deletes a set of labels to a pull_request merged into develop or release.
                Required parameters: organization, repository, token, pull-request, extras[commit_id, labels_to_add, labels_to_delete]
        - label_prs_mentioned_in_commits:
                Adds and/or deletes a set of labels to all PRs mentioned in the commit messages of specified pull_request.
                Required parameters: organization, repository, token, pull-request, extras[commit_id, labels_to_add, labels_to_delete]
        - list_commits:
                Fetches a list of commits for a specified pull request.
                Required parameters: organization, repository, token, pull-request
        - list_deleted_files:
                Fetches a list of deleted files for a specific commit.
                Required parameters: organization, repository, token, extras[commit_id]
        - open_pr:
                Opens a PR, using the supplied head branch into base branch.
                Required parameters: organization, repository, token, extras[head, base, title]
```