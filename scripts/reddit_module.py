import requests
from globals import CWD
import json

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
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}

    # Request the JSON data of user
    reddit_user_info = {'overview': requests.get(url=overview_url, headers=headers).json(),
                        'about': requests.get(url=about_url, headers=headers).json()}

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
