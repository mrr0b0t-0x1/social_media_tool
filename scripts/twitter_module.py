import subprocess
import json
from colorama import Fore
from globals import ROOT_DIR
import time
# import tweepy

def fix_timeline_file(file):
    """
    Fixes the format of JSON data stored in the Twitter timeline file
    :param file:
    :return:
    """
    timeline_data = {}

    i = 0
    try:
        with open(file, 'r') as handle:
            lines = handle.readlines()
            for line in lines:
                # Keep only latest 10 tweets
                if i < 10:
                    timeline_data[i] = json.loads(line)
                    i += 1
                else:
                    break

        with open(file, 'w') as handle:
            handle.write(json.dumps(timeline_data, indent=2))

    except Exception:
        print(json.dumps({"ERROR": "Error reading file at " + str(file)}))


def gather_info(username):
    """
    Gathers information about a user from his Twitter profile
    :param username:
    :return:
    """

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
    try:
        subprocess.run([
            "python", ROOT_DIR / "venv1/bin/twint",
            "--username", username,
            "--user-full",
            "--json",
            "--output", result_dir / (username + "-about-twitter.json")
        ], shell=False, stdout=subprocess.DEVNULL, check=True)
    except Exception:
        print(json.dumps({"ERROR": "Some error occurred while fetching Twitter about data"}))

    try:
        # Check if user is verified
        if (result_dir / (username + "-about-twitter.json")).exists():
            with open(result_dir / (username + "-about-twitter.json"), "r") as handle:
                about = json.load(handle)

                # If not verified, remove the fetched file and exit
                if not about['verified']:
                    print(json.dumps({"ERROR": username + " is not verified on Twitter, unable to fetch data"}))

                    (result_dir / (username + "-about-twitter.json")).unlink()
                    return

                else:
                    # Sleep for 2 seconds to avoid getting banned
                    time.sleep(2)

                    try:
                        subprocess.run([
                            "python", ROOT_DIR / "venv1/bin/twint",
                            "--username", username,
                            "--timeline",
                            "--limit", "5",
                            "--json",
                            "--output", result_dir / (username + "-timeline-twitter.json")
                        ], shell=False, stdout=subprocess.DEVNULL, check=True)
                    except Exception:
                        print(json.dumps({"ERROR": "Some error occurred while fetching Twitter timeline data"}))

                    # Fix the timeline formatting of JSON data
                    if (result_dir / (username + "-timeline-twitter.json")).exists():
                        fix_timeline_file(str(result_dir / (username + "-timeline-twitter.json")))

                print(json.dumps({"INFO": "Twitter data fetched"}))

        # Read data from result files and store in twitter_user_info
        # twitter_user_info = []

        # with open(result_dir / (username + "-about-twitter.json"), "r") as about:
        #     twitter_user_info.append('About User')
        #     for line in about:
        #         temp_dict = json.loads(line)
        #         twitter_user_info.append(temp_dict)
        #
        # with open(result_dir / (username + "-timeline-twitter.json"), 'r') as timeline:
        #     twitter_user_info.append('Timeline')
        #     for line in timeline:
        #         temp_dict = json.loads(line)
        #         twitter_user_info.append(temp_dict)

    except Exception as err:
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": str(err)}))

    # TODO: Remove this in final build
    # Print result data
    # print('\nTwitter Data:')
    # print(json.dumps(twitter_user_info, indent=2))
