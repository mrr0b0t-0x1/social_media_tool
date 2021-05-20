import requests
from globals import *
import json
from random import randint
# from colorama import Fore
import time

# Start a logger
logger = logging.getLogger('reddit module')

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
    logger.info("Fetching Reddit data...")

    # Target directory
    result_dir = ROOT_DIR / "scripts" / "results" / username / "reddit"

    # Target URLs and headers
    reddit_user_info = {}
    posts_url = 'https://www.reddit.com/user/' + username + '/submitted/.json'
    about_url = 'https://www.reddit.com/user/' + username + '/about/.json'
    headers = generate_headers()

    try:
        # Request the JSON data of user
        logger.info("Fetching Reddit posts data...")
        reddit_user_info['posts'] = requests.get(url=posts_url, headers=headers).json()
        logger.info("Fetched Reddit posts data")
        # Sleep for 2 seconds to avoid getting banned
        time.sleep(2)
        logger.info("Fetching Reddit about data...")
        reddit_user_info['about'] = requests.get(url=about_url, headers=headers).json()
        logger.info("Fetched Reddit about data")

        # Store result data to respective files
        logger.info("Storing Reddit about data to file...")
        with open(result_dir / (username + "-about-reddit.json"), "w+", encoding='utf-8') as handle:
            json.dump(reddit_user_info['about'], handle, indent=2)
        logger.info("Stored Reddit about data to file")

        logger.info("Storing Reddit posts data to file...")
        with open(result_dir / (username + "-posts-reddit.json"), "w+", encoding='utf-8') as handle:
            json.dump(reddit_user_info['posts'], handle, indent=2)
        logger.info("Stored Reddit posts data to file")

        # TODO: Remove this in final build
        # Print result data
        # print('\nReddit Data:')
        # print(json.dumps(reddit_user_info, indent=2))
        print(json.dumps({"INFO": "Reddit data fetched"}))
        logger.info("Fetched Reddit data")

    except Exception as err:
        logger.exception("Exception occurred")
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": "Error occurred while fetching Reddit data, see logs for more details."}))
