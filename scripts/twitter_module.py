import subprocess
import json
from colorama import Fore
from globals import CWD
import time
# import tweepy

def gather_info(username):
    """
    Gathers information about a user from his Twitter profile
    :param username:
    :return:
    """

    print('Fetching Twitter Data...\n')

    # Target directory
    result_dir = CWD / "scripts" / "results" / username / "twitter"

    # Using official Twitter API
    # API Keys
    # consumer_key = 'ALqGFzqfDfSIUhW5m0qJgvefD'
    # consumer_secret = 'XRG32CuSgnOLfR3WNf0yrBkGd6h6ayBcRtRxtm5tPVowvYNtzt'
    #
    # auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    # api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    #
    # try:
    #     # Get user info
    #     twitter_user_info = api.get_user(id=username)
    #
    #     print('Twitter Data:')
    #     print(json.dumps(twitter_user_info, indent=2))
    #     # for info in twitter_user_info:
    #     #     print( f'{info} : {twitter_user_info[info]}' )
    #
    # except BaseException as e:
    #     print('failed on_status,', str(e))

    #########################################################

    # Using Twint
    # Imp command for Twint to work - pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

    # Run twint as a subprocess
    # subprocess.run("twint -u " + username + " --user-full --json -o " + username + "-about-twitter.json", shell=True)
    subprocess.run([
        "python", CWD / "venv/bin/twint",
        "--username", username,
        "--user-full",
        "--json",
        "--output", result_dir / (username + "-about-twitter.json")
    ], shell=False)

    # Sleep for 5 seconds to avoid getting banned
    time.sleep(5)

    subprocess.run([
        "python", CWD / "venv/bin/twint",
        "--username", username,
        "--timeline",
        "--limit", "5",
        "--json",
        "--output", result_dir / (username + "-timeline-twitter.json")
    ], shell=False)

    # Read data from result files and store in twitter_user_info
    twitter_user_info = []

    try:
        with open(result_dir / (username + "-about-twitter.json"), "r") as about:
            twitter_user_info.append('About User')
            for line in about:
                temp_dict = json.loads(line)
                twitter_user_info.append(temp_dict)
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))

    try:
        with open(result_dir / (username + "-timeline-twitter.json"), 'r') as timeline:
            twitter_user_info.append('Timeline')
            for line in timeline:
                temp_dict = json.loads(line)
                twitter_user_info.append(temp_dict)
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))

    # TODO: Remove this in final build
    # Print result data
    # print('\nTwitter Data:')
    # print(json.dumps(twitter_user_info, indent=2))
    print('Twitter data fetched\n')
