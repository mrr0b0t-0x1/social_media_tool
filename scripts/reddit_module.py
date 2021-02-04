import requests
from globals import *
import json
from random import randint

# Generate random headers
def generate_headers():
    headers = {
        'Host': 'www.reddit.com',
        'User-Agent': USER_AGENTS[randint(0, len(USER_AGENTS) - 1)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Referer': REFERERS[randint(0, len(REFERERS) - 1)],
        'Connection': 'keep-alive',
        'DNT': '1',
        "Upgrade-Insecure-Requests": "1"
    }
    return headers


def gather_info(username):
    """
    Gathers information about a user from his Reddit profile
    :param username:
    :return:
    """

    # Target directory
    result_dir = CWD / "scripts" / "results" / username / "reddit"

    # Target URLs and headers
    overview_url = 'https://www.reddit.com/user/' + username + '/overview/.json'
    about_url = 'https://www.reddit.com/user/' + username + '/about/.json'
    headers = generate_headers()

    # Request the JSON data of user
    reddit_user_info = {
        'overview': requests.get(url=overview_url, headers=headers).json(),
        'about': requests.get(url=about_url, headers=headers).json()
    }

    # Store result data to file
    try:
        with open(result_dir / (username + ".json"), "w+") as handle:
            json.dump(reddit_user_info, handle, indent=2)

        # TODO: Remove this in final build
        # Print result data
        print('\nReddit Data:')
        print(json.dumps(reddit_user_info, indent=2))
    except OSError as err:
        print(err)
