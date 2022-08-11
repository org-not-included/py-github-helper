import logging
import requests
import pendulum

from .util import *


######################
#   HELPER COMMANDS  #
######################
def get_issue_close_date(
        issue,
        organization,
        repository,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Returns a string representing the datetime an issue was closed."""
    headers = build_headers(token, username, password)
    issue = issue.lstrip("#")
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues/{issue}"
    logging.info(f"URL: {curr_endpoint}")
    response = requests.get(curr_endpoint, headers=headers)
    response_dict = json.loads(response.text)
    date = response_dict["closed_at"]
    return date


def get_issues(
        organization,
        repository,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Returns a json object of all issues."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues"
    logging.info(f"URL: {curr_endpoint}")
    response = requests.get(curr_endpoint, headers=headers)
    response_dict = json.loads(response.text)
    logging.info("Issue Output:")
    logging.info(json.dumps(response_dict, indent=4, sort_keys=True))
    return response_dict


def get_pr_id_from_commit_id(
        organization,
        repository,
        commit_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Gets a pull_request id, by pulling PRs that include commit_id."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/commits/{commit_id}/pulls"
    logging.info(f"URL: {curr_endpoint}")
    response = requests.get(curr_endpoint, headers=headers)
    pr_id = json.loads(response.text)[0]["number"]
    logging.info(f"PR ID: {pr_id}")
    return pr_id

def get_files_changed_during_pr(
        organization,
        repository,
        pull_request_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Gets a pull_request id, by pulling PRs that include commit_id."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/pulls/{pull_request_id}/files"
    logging.info(f"URL: {curr_endpoint}")
    response = requests.get(curr_endpoint, headers=headers)
    json_response = json.loads(response.text)
    files = []
    for file in json_response:
        files.append(file['filename'])
    logging.info(f"files: {files}")
    return files


def parse_commit_message_for_mentioned_pr(
        organization,
        repository,
        commit_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Gets a pull_request id, by parsing commit for (#xxx)."""
    commit_message = get_commit_message(
        organization=organization,
        repository=repository,
        commit_id=commit_id,
        token=token,
        username=username,
        password=password,
    )
    pr_id = parse_commit_for_pr(commit_message)
    logging.info(pr_id)
    return pr_id


def get_target_branch(
        organization,
        repository,
        pull_request_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Returns the target branch for a specified pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = (
        f"{base_url}/repos/{organization}/{repository}/pulls/{pull_request_id}"
    )
    logging.info(f"Fetching Target Branch for PR #{pull_request_id}...")
    response = requests.get(
        curr_endpoint,
        headers=headers,
    )
    response_dict = json.loads(response.text)
    logging.info(json.dumps(response_dict, sort_keys=True, indent=4))
    target_branch = response_dict["base"]["ref"]
    return target_branch


######################
#      COMMANDS      #
######################


def add_comment(
        organization,
        repository,
        pull_request_id,
        message="automated message via Github API",
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Add a specified comment to a particular pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues/{pull_request_id}/comments"
    if "filename" in kwargs:
        with open(kwargs["filename"], "r") as file:
            message = f"{message}\n\n\n{file.read()}"
    logging.info(
        f"Adding comment for PR #{pull_request_id}...\n\tComment:\n\t'{message}' "
    )
    print(f"URL: {curr_endpoint}")
    print(f"headers: {headers}")
    print(f"body: {message}")
    response = requests.post(
        curr_endpoint, headers=headers, data=json.dumps({"body": message})
    )
    logging.info(response)


def add_labels(
        organization,
        repository,
        pull_request_id,
        labels=["test"],
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Add a set of labels to a particular pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues/{pull_request_id}/labels"
    logging.info(f"URL: {curr_endpoint}")
    logging.info(
        f"Adding labels for PR #{pull_request_id}...\n\tLabels:\n\t {', '.join(labels)}"
    )
    response = requests.post(
        curr_endpoint, headers=headers, data=json.dumps({"labels": labels})
    )
    logging.info(response)


def close_issue(
        issue,
        organization,
        repository,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Marks a specified issue as closed."""
    headers = build_headers(token, username, password)
    issue = issue.lstrip("#")
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues/{issue}"
    logging.info(f"URL: {curr_endpoint}")
    data = {
        "state": "closed",
    }
    response = requests.patch(curr_endpoint, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    logging.info("Response:")
    logging.info(json.dumps(response_dict, indent=4, sort_keys=True))
    return response_dict


def delete_labels(
        organization,
        repository,
        pull_request_id,
        labels=["test"],
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Deletes a set of specified labels from a particular pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/issues/{pull_request_id}/labels"
    logging.info(f"URL: {curr_endpoint}")
    logging.info(
        f"Removing labels for PR #{pull_request_id}...\n\tLabels:\n\t {', '.join(labels)}"
    )
    for label in labels:
        response = requests.delete(
            f"{curr_endpoint}/{label}",
            headers=headers,
        )
        logging.info(f"Label: {label}\n\tResponse: {response}")


def dismiss_single_review(
        organization,
        repository,
        pull_request_id,
        review_id,
        message="automated dismissal via Github API",
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Dismiss a specified review for a particular pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/pulls/{pull_request_id}/reviews/{review_id}/dismissals"
    logging.info(f"Dismissing Review '{review_id}' for PR #{pull_request_id}")
    response = requests.put(
        curr_endpoint, headers=headers, data=json.dumps({"message": message})
    )
    logging.info(response)


def dismiss_all_reviews(
        organization,
        repository,
        pull_request_id,
        message="automated dismissal via Github API",
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Dismiss all reviews for a particular pull request."""
    headers = build_headers(token, username, password)
    logging.info(
        f"Fetching list of reviews for {organization}/{repository}/{pull_request_id}."
    )
    response = requests.get(
        f"{base_url}/repos/{organization}/{repository}/pulls/{pull_request_id}/reviews",
        headers=headers,
    )
    body = json.loads(response.text)
    review_ids = []
    for review in body:
        if "id" in review:
            curr_id = review["id"]
            logging.info(f"current ID: {curr_id}")
            review_ids.append(curr_id)

    logging.info(
        f"Dismissing all reviews by ID for {organization}/{repository}/{pull_request_id}."
    )
    for review_id in review_ids:
        dismiss_single_review(
            organization, repository, token, pull_request_id, review_id
        )


def get_commit_message(
        organization,
        repository,
        commit_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Gets a commit message, using the commit_id."""
    headers = build_headers(token, username, password)
    curr_endpoint = (
        f"{base_url}/repos/{organization}/{repository}/commits/{commit_id}"
    )
    response = requests.get(
        curr_endpoint,
        headers=headers,
    )
    json_response = json.loads(response.text)
    commit_message = json_response["commit"]["message"]
    logging.info(commit_message)
    return commit_message


def get_deploy_issue_number(
        organization,
        repository,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """
    Grabs a list of all open issues.
    Filters for an issue titled "Deploy Request: YYYY-MM-DD".
    Returns an associated issue number.
    """
    issues = get_issues(organization, repository, token, username, password)
    for issue in issues:
        expected_issue_name = "Deploy Request: %s" % pendulum.now().format("YYYY-MM-DD")
        if issue["title"].startswith(expected_issue_name):
            logging.info(
                f"Current issue: {issue['title']} matches {expected_issue_name}."
            )
            return issue["number"]


def get_prs_to_deploy(
        organization,
        repository,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """
    Grabs a list of all open issues.
    Filters for an issue titled "Deploy Request: YYYY-MM-DD".
    Parses the issue's body for all instances of #PR.
    Parses the issue's comments for all instances of #PR.
    Sorts the issues by closed_at datetime (most recent last).
    Returns the list of issues.
    """
    headers = build_headers(token, username, password)
    issues = get_issues(organization, repository, token, username, password)
    pr_list = []
    for issue in issues:
        expected_issue_name = "Deploy Request: %s" % pendulum.now().format("YYYY-MM-DD")
        if issue["title"].startswith(expected_issue_name):
            logging.info(
                f"Current issue: {issue['title']} matches {expected_issue_name}."
            )
            prs_mentioned = parse_message_for_prs(issue["body"])
            pr_list.extend(prs_mentioned)

            comments_url = issue["comments_url"]
            if comments_url:
                comment_response = requests.get(comments_url, headers=headers)
                comment_dict = json.loads(comment_response.text)
                logging.info("Comment Output:")
                logging.info(json.dumps(comment_dict, indent=4, sort_keys=True))
                for comment in comment_dict:
                    prs_mentioned = parse_message_for_prs(comment["body"])
                    pr_list.extend(prs_mentioned)
    pr_tup_list_with_dates = [
        (
            pr,
            get_issue_close_date(
                pr, organization, repository, token, username, password
            ),
        )
        for pr in pr_list
    ]
    pr_tup_list_with_dates = sorted(pr_tup_list_with_dates, key=lambda x: x[1])
    logging.info(f"Tuples (PR#, closed_at): {pr_tup_list_with_dates}")
    sorted_pr_list = [x[0].strip("#") for x in pr_tup_list_with_dates]
    return sorted_pr_list


def label_merged_pr(
        organization,
        repository,
        commit_id,
        labels_to_add=["release"],
        labels_to_delete=["in_development"],
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Adds and/or deletes a set of labels for a pull_request (which was merged into develop or release)."""
    commit_message = get_commit_message(
        organization=organization,
        repository=repository,
        commit_id=commit_id,
        token=token,
        username=username,
        password=password,
    )
    pr_id = parse_commit_for_pr(commit_message)
    logging.info(f"PR IDs parsed from commit:\n\t{pr_id}")
    if pr_id:
        add_labels(
            organization=organization,
            repository=repository,
            pull_request_id=pr_id,
            labels=labels_to_add,
            token=token,
            username=username,
            password=password,
        )
        delete_labels(
            organization=organization,
            repository=repository,
            pull_request_id=pr_id,
            labels=labels_to_delete,
            token=token,
            username=username,
            password=password,
        )


def label_prs_mentioned_in_commits(
        organization,
        repository,
        pull_request_id=None,
        commit_id=None,
        labels_to_add=["deployed"],
        labels_to_delete=["undeployed"],
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Adds and/or deletes a set of labels to all PRs mentioned in the commit messages of specified pull_request."""
    if pull_request_id is None:
        pull_request_id = parse_commit_message_for_mentioned_pr(
            organization=organization,
            repository=repository,
            commit_id=commit_id,
            token=token,
            username=username,
            password=password,
        )

    commits = list_commits(
        organization=organization,
        repository=repository,
        pull_request_id=pull_request_id,
        token=token,
        username=username,
        password=password,
    )
    dirty_pr_ids = [parse_commit_for_pr(commit) for commit in commits]
    pr_ids = [pr_id for pr_id in dirty_pr_ids if pr_id]
    logging.info(f"PR IDs parsed from commits:\n\t{pr_ids}")

    for pr_id in pr_ids:
        add_labels(
            organization=organization,
            repository=repository,
            pull_request_id=pr_id,
            labels=labels_to_add,
            token=token,
            username=username,
            password=password,
        )
        delete_labels(
            organization=organization,
            repository=repository,
            pull_request_id=pr_id,
            labels=labels_to_delete,
            token=token,
            username=username,
            password=password,
        )


def list_commits(
        organization,
        repository,
        pull_request_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Returns a list of all commit messages for a specified pull request."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/pulls/{pull_request_id}/commits"
    logging.info(f"Fetching commits for PR #{pull_request_id}...")
    response = requests.get(
        curr_endpoint,
        headers=headers,
    )
    commit_dict = json.loads(response.text)
    commit_messages = []
    for commit in commit_dict:
        commit_messages.append(str(commit["commit"]["message"]))
    logging.info(f"Commit Messages:\n\t{commit_messages}")
    return commit_messages


def list_deleted_files(
        organization,
        repository,
        commit_id,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Gets a list of files deleted from a commit, using the commit_id."""
    headers = build_headers(token, username, password)
    curr_endpoint = (
        f"{base_url}/repos/{organization}/{repository}/commits/{commit_id}"
    )
    response = requests.get(
        curr_endpoint,
        headers=headers,
    )
    json_response = json.loads(response.text)
    logging.info(json_response)
    files_modified = json_response["files"]
    deleted_files = []
    logging.info("\n\nRaw dump of json response:")
    logging.info(json.dumps(files_modified, indent=4, sort_keys=True))
    logging.info("\n\nList of all files modified:")
    for file in files_modified:
        file_name = file["filename"]
        status = file["status"]
        logging.info(f"Filename: {file_name}. Status: {status}")

    logging.info("\n\nExplanation of what's being deleted:")
    # Only delete files if they have been renamed or removed
    for file in files_modified:
        file_name = file["filename"]
        status = file["status"]
        if status == "removed":
            deleted_files.append(file_name)
            logging.info(f"Deleting {file_name}.")
        if status == "renamed":
            old_file_name = file["previous_filename"]
            logging.info(f"Deleting {old_file_name} (renamed to {file_name})")
            deleted_files.append(old_file_name)
    logging.info("\n\n List of files to be deleted:\n" + "\n".join(deleted_files))
    return deleted_files


def open_pr(
        organization,
        repository,
        head,
        base,
        title,
        token=None,
        username=None,
        password=None,
        **kwargs,
):
    """Opens a PR to merge head branch into base branch."""
    headers = build_headers(token, username, password)
    curr_endpoint = f"{base_url}/repos/{organization}/{repository}/pulls"
    logging.info(f"URL: {curr_endpoint}")
    data = {
        "head": head,
        "base": base,
        "title": title,
    }
    response = requests.post(curr_endpoint, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    logging.info("Response:")
    logging.info(json.dumps(response_dict, indent=4, sort_keys=True))
    return response_dict

