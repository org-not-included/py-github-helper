import argparse
import json
import re

base_url = "https://api.github.com"

available_commands = {
    "add_comment": [
        "Adds a single comment for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request, extras[message]",
    ],
    "add_labels": [
        "Adds a set of labels for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request, extras[labels]",
    ],
    "close_issue": [
        "Marks a specified issue as closed.",
        "Required parameters: organization, repository, token, extras[issue]",
    ],
    "delete_labels": [
        "Deletes a set of labels for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request, extras[labels]",
    ],
    "dimiss_single_review": [
        "Dismisses a specific review for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request, extras[review_id]",
    ],
    "dismiss_all_reviews": [
        "Dismisses all reviews for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request",
    ],
    "get_commit_message": [
        "Gets a commit message, using the commit_id.",
        "Required parameters: organization, repository, token, pull-request, extras[commit_id]",
    ],
    "get_deploy_issue_number": [
        "Parses for a Github issue titled 'Deploy Request: YYYY-MM-DD', and returns the associated issue id.",
        "Required parameters: organization, repository, token",
    ],
    "get_files_changed_during_pr": [
        "Gets a PR's details, and filters it for a list of file names",
        "Required parameters: organization, repository, pull-request, token",
    ],
    "get_pr_id_from_commit_id": [
        "Returns a PR number, for an associated commit SHA.",
        "Required parameters: organization, repository, token, extras[commit_id]",
    ],
    "get_prs_to_deploy": [
        "Parses for a Github issue titled 'Deploy Request: YYYY-MM-DD', and generates a list of mentioned PRs (in order of closed_at).",
        "Required parameters: organization, repository, token",
    ],
    "label_merged_pr": [
        "Adds and/or deletes a set of labels to a pull_request merged into develop or release.",
        "Required parameters: organization, repository, token, pull-request, extras[commit_id, labels_to_add, labels_to_delete]",
    ],
    "label_prs_mentioned_in_commits": [
        "Adds and/or deletes a set of labels to all PRs mentioned in the commit messages of specified pull_request.",
        "Required parameters: organization, repository, token, pull-request, extras[commit_id, labels_to_add, labels_to_delete]",
    ],
    "list_commits": [
        "Fetches a list of commits for a specified pull request.",
        "Required parameters: organization, repository, token, pull-request",
    ],
    "list_deleted_files": [
        "Fetches a list of deleted files for a specific commit.",
        "Required parameters: organization, repository, token, extras[commit_id]",
    ],
    "open_pr": [
        "Opens a PR, using the supplied head branch into base branch.",
        "Required parameters: organization, repository, token, extras[head, base, title]",
    ],
}
command_template = 'Expected Syntax:\n\tpython3 -m py-github-helper -o <Organization Name> -r <Repository> -t <O-Auth Token> -u <Github username> -p <Github password> -l <PR Number> -c <Github API Command> -e \'{"x": "sample", "y": 5, "z": "test}\'\n'


######################
#  HELPER FUNCTIONS  #
######################


def build_headers(token, username, password):
    """Format secret(s) for headers of API call."""
    if token:
        headers = {
            "Authorization": f"token {token}",
        }
    elif username and password:
        headers = {"Authorization": f"Basic {username}:{password}"}
    else:
        raise Exception(
            "Either Authentication Token or Username + Password need to be included in request."
        )
    return headers


def format_epilog():
    """Print available commands at end of help message."""
    epilog = command_template
    epilog += "\n\nAvailable Commands:\n"
    for key in available_commands.keys():
        curr_val = available_commands[key]
        curr_desc = f"\n\t- {key}:\n\t\t{curr_val[0]}\n\t\t{curr_val[1]}"
        epilog += curr_desc
    return epilog


def parse_commit_for_pr(commit):
    """
    Returns PR ID, for a given commit message (if exists).

    :param commit: A commit message.
    :type commit: str
    """

    pattern = r"\(#(.+?)\)"
    m = re.search(pattern, commit)
    if m:
        pr_id = m.group(1)
        return pr_id


def is_json(json_str):
    """
    Check if string is json-compatible.

    :param json_str: A json-formattable string.
    :type json_str: str
    """
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True


def validate_args(args):
    """
    Check the arguments formatting and syntax.

    :param args: Contains arguments passed through command line
    :type args: argparse.Namespace
    """

    if args.token and args.username:
        raise ValueError(
            "ERROR:\tOnly one form of authentication is required (either token or user/pass)."
        )
    if not args.token and not args.username:
        with open("secrets/gh_keyfile.json", "r") as gh_keyfile:
            args.token = gh_keyfile.read()

    if not is_json(args.extras):
        raise ValueError(
            f'\n\nERROR:\tParamater "extras" is not formatted correctly. Incorrect syntax:\n\t{args.extras}'
        )
    return args


def parse_message_for_prs(message):
    """
    Returns a list of all occurences of #PR in any message.

    :param message: A blob of text to parse.
    :type message: str
    """
    pattern = r"#\d+"
    prs = re.findall(pattern, message)
    return prs

