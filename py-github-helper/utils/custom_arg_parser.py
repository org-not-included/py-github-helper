from .commands import *


def parse_args():
    """
    Parses input arguments and formats parameters for generating specified command (API request).

    On error: prints expected syntax, list of commands, and error details.
    """
    parser = argparse.ArgumentParser(
        prog="py-github-helper",
        formatter_class=argparse.RawTextHelpFormatter,
        description="A python script that handles GitHub API calls.",
        epilog=format_epilog(),
    )

    parser.add_argument(
        "-o", "--organization", type=str, help="Owner of GitHub repository."
    )
    parser.add_argument(
        "-r", "--repository", type=str, help="Name of the GitHub repository."
    )
    parser.add_argument(
        "-t", "--token", type=str, help="User's GitHub Personal Access Token."
    )
    parser.add_argument(
        "-u", "--username", "--user", type=str, help="User's GitHub username."
    )
    parser.add_argument(
        "-p", "--password", "--pass", type=str, help="User's Github password."
    )
    parser.add_argument(
        "-l",
        "--pull_request_id",
        "--pull-request",
        type=str,
        help="The issue # of the Pull Request.",
    )
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help="Name of python function associated with API call being made.",
    )
    parser.add_argument(
        "-e", "--extras", type=str, help="Extra dictionary to allow for more arguments."
    )

    args = parser.parse_args()
    args = validate_args(args)

    parameters = {**vars(args), **json.loads(args.extras)}
    pretty_params = "\n".join(
        [f"{key:<20} {value}" for key, value in parameters.items()]
    )
    logging.info(f"\n\nParsed Parameters:\n{pretty_params}")
    logging.info("\n\n\n")

    return globals()[args.command](**parameters)
