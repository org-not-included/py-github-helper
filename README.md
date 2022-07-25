# github_api
Python Script for interacting with Github API.

## Example
```shell
python3 helpers/make_api_call.py \
        -t $GH_TOKEN -o org-not-included -r github_api -l 1 -c add_comment \
        -e '{"message": "This message was successfully posted via gitub_api."}'
```