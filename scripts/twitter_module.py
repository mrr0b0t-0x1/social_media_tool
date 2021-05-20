import subprocess
import json
# from colorama import Fore
from globals import ROOT_DIR, scripts_path
import time
import logging
# import tweepy
import os
import platform

# Start a logger
logger = logging.getLogger('twitter module')

def fix_timeline_file(file):
    """
    Fixes the format of JSON data stored in the Twitter timeline file
    :param file:
    :return:
    """
    logger.info("Fixing Twitter timeline file formatting")

    timeline_data = {}

    i = 0
    try:
        logger.info("Fixing Twitter timeline file...")
        with open(file, 'r', encoding='utf-8') as handle:
            lines = handle.readlines()

            for line in lines:
                # Keep only latest 10 tweets
                if i < 10:
                    timeline_data[i] = json.loads(line)
                    i += 1
                else:
                    break
        with open(file, 'w', encoding='utf-8') as handle:
            handle.write(json.dumps(timeline_data, indent=2))
        logger.info("Fixed Twitter timeline file")

    except Exception:
        logger.exception("Exception occurred")
        print(json.dumps({"ERROR": "Error occurred while fixing Twitter timeline file, see logs for more details."}))


def gather_info(username):
    """
    Gathers information about a user from his Twitter profile
    :param username:
    :return:
    """

    logger.info("Fetching Twitter data...")
    print(json.dumps({"INFO": "Fetching Twitter Data..."}))

    # Target directory
    result_dir = ROOT_DIR / "scripts" / "results" / username / "twitter"

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
    logger.info("Fetching Twitter about data...")
    try:
        logger.info("Removing previous twint about results...")
        if (result_dir / (username + "-about-twitter.json")).exists():
            (result_dir / (username + "-about-twitter.json")).unlink()

        logger.info("Running twint...")
        subprocess.run([
            os.path.join(scripts_path, "twint.exe") if platform.system() == "Windows" else os.path.join(scripts_path, "twint"),
            "--username", username,
            "--user-full",
            "--json",
            "--output", os.path.join(str(result_dir), username + "-about-twitter.json")
        ], shell=False, stdout=subprocess.DEVNULL, check=True)
        logger.info("Fetched Twitter about data")
    except Exception as err:
        logger.exception("Exception occurred")
        print(json.dumps({"ERROR": "Error occurred while fetching Twitter about data, see logs for more details."}))

    try:
        # Check if user is verified
        logger.info("Checking if Twitter about file exists")
        if (result_dir / (username + "-about-twitter.json")).exists():
            logger.info("Twitter about file exists")

            with open(result_dir / (username + "-about-twitter.json"), "r", encoding='utf-8') as handle:
                logger.info("Opened Twitter about file")

                about = json.load(handle)
                logger.info("Loaded Twitter about data from file")

                # If not verified, remove the fetched file and exit
                logger.info("Checking if Twitter user is verified...")
                if not about['verified']:
                    logger.error("Twitter user is not verified")
                    print(json.dumps({"ERROR": username + " is not verified on Twitter, unable to fetch data"}))

                    logger.info("Removing fetched Twitter data...")
                    (result_dir / (username + "-about-twitter.json")).unlink()
                    logger.info("Twitter data removed")

                    return

                else:
                    logger.info("Twitter user is verified")
                    # Sleep for 2 seconds to avoid getting banned
                    time.sleep(2)

                    logger.info("Fetching Twitter timeline data...")
                    try:
                        logger.info("Removing previous twint timeline results...")
                        if (result_dir / (username + "-timeline-twitter.json")).exists():
                            (result_dir / (username + "-timeline-twitter.json")).unlink()

                        subprocess.run([
                            os.path.join(scripts_path, "twint.exe") if platform.system() == "Windows" else os.path.join(scripts_path, "twint"),
                            "--username", username,
                            "--timeline",
                            "--limit", "5",
                            "--json",
                            "--output", os.path.join(str(result_dir), username + "-timeline-twitter.json")
                        ], shell=False, stdout=subprocess.DEVNULL, check=True)
                        logger.info("Fetched Twitter timeline data")
                    except Exception as err:
                        logger.exception("Exception occurred")
                        print(json.dumps({"ERROR": "Error occurred while fetching Twitter timeline data, see logs for more details."}))

                    # Fix the timeline formatting of JSON data
                    logger.info("Checking if Twitter timeline file exists")
                    if (result_dir / (username + "-timeline-twitter.json")).exists():
                        logger.info("Twitter timeline file exists")

                        fix_timeline_file(str(result_dir / (username + "-timeline-twitter.json")))

                print(json.dumps({"INFO": "Twitter data fetched"}))
                logger.info("Fetched Twitter data")

        # Read data from result files and store in twitter_user_info
        # twitter_user_info = []

        # with open(result_dir / (username + "-about-twitter.json"), "r", encoding='utf-8') as about:
        #     twitter_user_info.append('About User')
        #     for line in about:
        #         temp_dict = json.loads(line)
        #         twitter_user_info.append(temp_dict)
        #
        # with open(result_dir / (username + "-timeline-twitter.json"), 'r', encoding='utf-8') as timeline:
        #     twitter_user_info.append('Timeline')
        #     for line in timeline:
        #         temp_dict = json.loads(line)
        #         twitter_user_info.append(temp_dict)

    except Exception as err:
        logger.exception("Exception occurred")
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": "Error occurred while fetching Twitter data, see logs for more details."}))
