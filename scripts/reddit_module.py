import requests
from globals import *
import json
from random import randint
from colorama import Fore
import time

# Generate random headers
def generate_headers():
    headers = HEADERS

    headers['Host'] = 'www.reddit.com'
    headers['User-Agent'] = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
    headers['Referer'] = REFERERS[randint(0, len(REFERERS) - 1)]

    return headers


def gather_info(username):
    """
    Gathers information about a user from his Reddit profile
    :param username:
    :return:
    """

    print(json.dumps({"INFO": "Fetching Reddit Data..."}))

    # Target directory
    result_dir = ROOT_DIR / "scripts" / "results" / username / "reddit"

    # Target URLs and headers
    reddit_user_info = {}
    overview_url = 'https://www.reddit.com/user/' + username + '/overview/.json'
    about_url = 'https://www.reddit.com/user/' + username + '/about/.json'
    headers = generate_headers()

    try:
        # Request the JSON data of user
        reddit_user_info['overview'] = requests.get(url=overview_url, headers=headers).json()
        # Sleep for 2 seconds to avoid getting banned
        time.sleep(2)
        reddit_user_info['about'] = requests.get(url=about_url, headers=headers).json()

        # Store result data to respective files
        with open(result_dir / (username + "-about-reddit.json"), "w+") as handle:
            json.dump(reddit_user_info['about'], handle, indent=2)
        with open(result_dir / (username + "-overview-reddit.json"), "w+") as handle:
            json.dump(reddit_user_info['overview'], handle, indent=2)

        # TODO: Remove this in final build
        # Print result data
        # print('\nReddit Data:')
        # print(json.dumps(reddit_user_info, indent=2))
        print(json.dumps({"INFO": "Reddit data fetched"}))

    except Exception as err:
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": str(err)}))
