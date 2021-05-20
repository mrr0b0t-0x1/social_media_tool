import os
import subprocess
from globals import ROOT_DIR, scripts_path
import json
import re
import logging
# from colorama import Fore

# Start a logger
logger = logging.getLogger('instagram module')

# Fix filename for consistency
# def fix_filename(username, result_dir):
#     if (result_dir / (username + ".json")).exists():
#         (result_dir / (username + ".json")).rename(
#             result_dir / (username + "-about-instagram.json")
#         )

# Strip ANSI colors from output for osi.ig scraper
def strip_color(username, result_dir):
    logger.info("Stripping colors from Instagram results...")
    try:
        with open((result_dir / username).with_suffix(".txt"), "r", encoding='utf-8') as handle:
            lines = handle.readlines()
        with open((result_dir / username).with_suffix(".txt"), "w", encoding='utf-8') as handle:
            for line in lines:
                handle.writelines(re.sub("\033\\[([0-9]+)(;[0-9]+)*m", "", line))
        logger.info("Stripped colors from Instagram results")
    except FileNotFoundError as err:
        logger.exception("Exception occurred")
        print(json.dumps({"ERROR": "Error occurred while simplifying Instagram results, see logs for more details."}))

# Convert data to JSON for osi.ig scraper
def convert_to_json(username, result_dir):
    data = {}
    private = False

    logger.info("Converting Instagram text file to JSON file...")
    try:
        # Open the txt fiel and convert data to dictionary
        with open((result_dir / username).with_suffix(".txt"), "r", encoding='utf-8') as handle:
            temp = {}
            flag = ''
            for line in handle:

                if "[+]" in line:
                    if temp:
                        data[flag] = temp

                    if not line.startswith(tuple(["[+] contains", "[+] info"])):
                        flag = line.split("[+]")[1].split(":")[0].strip().replace(" ", "_")
                        temp = {}

                elif line == "\n":
                    pass

                elif flag.startswith(tuple(["user_info", "most_used", "post"])):
                    val = line.split(":", 1)

                    if len(val) == 1:
                        temp[key] += val[0].strip()
                    else:
                        key, val = val[0].strip(), val[1].strip()
                        # print(key + ": " + val)
                        if key == "verified" and val == "False":
                            logger.error(f"{username} is not verified on Instagram, unable to fetch data")
                            print(json.dumps({"ERROR": f"{username} is not verified on Instagram, unable to fetch data"}))
                            return

                        elif key == "private" and val == "True":
                            logger.error(f"{username}'s profile is private on Instagram, unable to fetch posts")
                            private = True
                            print(json.dumps({"ERROR": f"{username}'s profile is private on Instagram, unable to fetch posts"}))

                        else:
                            temp[key] = val

        logger.info("Storing Instagram about data to JSON file...")
        # Store about data in JSON
        with open((result_dir / (username + "-about-insta")).with_suffix(".json"), "w", encoding='utf-8') as handle:

            about_keys = [key for key in data.keys() if key.startswith(tuple(['user_info', 'most_used']))]
            about = {}
            for key in about_keys:
                if key == "user_info":
                    about = data['user_info']
                else:
                    about[key] = data[key]

            json.dump(about, handle, indent=2)
        logger.info("Stored Instagram about data to JSON file")

        # Store posts data in JSON if not private
        if not private:
            logger.info("Storing Instagram posts data to JSON file...")
            with open((result_dir / (username + "-posts-insta")).with_suffix(".json"), "w", encoding='utf-8') as handle:

                posts_keys = [key for key in data.keys() if key.startswith('post')]
                posts = {}
                for key in posts_keys:
                    posts[key] = data[key]

                json.dump(posts, handle, indent=2)
            logger.info("Stored Instagram posts data to JSON file")

    except Exception as err:
        logger.exception("Exception occurred")
        print(json.dumps({"ERROR": "Error occurred while converting Instagram data, see logs for more details."}))


def gather_info(username):
    """
    Gathers information about a user from his Instagram profile
    :param username:
    :return:
    """

    print(json.dumps({"INFO": "Fetching Instagram Data..."}))
    logger.info("Fetching Instagram data...")

    # Target directory
    result_dir = ROOT_DIR / "scripts" / "results" / username / "instagram"

    # Run instagram-scraper as a subprocess
    # subprocess.run([
    #     "python", CWD / "venv/bin/instagram-scraper", "-q",
    #     "-u", "pyvma_1990",
    #     "-p", "i652HD9dkbUFWLMGn647",
    #     username,
    #     "--profile-metadata",
    #     "-m", "10",
    #     "-d", result_dir
    # ], shell=False, stdout=subprocess.DEVNULL, check=True)
    try:
        # instagram-scraper
        # subprocess.run([
        #     "python", ROOT_DIR / "venv1/bin/instagram-scraper", "-q",
        #     username,
        #     "--profile-metadata",
        #     "-m", "10",
        #     "-d", result_dir
        # ], shell=False, stdout=subprocess.DEVNULL, check=True)
        #
        # fix_filename(username, result_dir)
        #
        # # Read data from result file
        # # with open(result_dir / (username + ".json"), "r", encoding='utf-8') as about:
        # #     data = json.load(about)
        #
        # # TODO: Remove this in final build
        # # Print result data
        # # print('\nInstagram Data:')
        # # print(json.dumps(data, indent=2))
        #
        # # Remove instagram-scraper's log file
        # if (ROOT_DIR / "ui" / "instagram-scraper").with_suffix(".log").exists():
        #     (ROOT_DIR / "ui" / "instagram-scraper").with_suffix(".log").unlink()
        # elif (ROOT_DIR / "instagram-scraper").with_suffix(".log").exists():
        #     (ROOT_DIR / "instagram-scraper").with_suffix(".log").unlink()

        # osi.ig scraper
        # with open((result_dir / username).with_suffix(".txt"), "w", encoding='utf-8') as handle:
        try:
            logger.info("Running osi.ig...")

            subprocess.run([
                os.path.join(scripts_path, "python"),
                os.path.join(str(ROOT_DIR), "venv1", "src", "osi.ig", "main.py"),
                "-u", username, "-p",
                "-o", os.path.join(str(result_dir))
            ], shell=False, stdout=subprocess.DEVNULL, check=True)

            logger.info("Executed osi.ig successfully")
        except Exception as err:
            logger.exception("Exception occurred")
            print(json.dumps({"ERROR": "Error occurred while fetching Instagram data, see logs for more details."}))

        # # Strip colors from output
        # strip_color(username, result_dir)
        #
        # # Convert output to JSON
        # convert_to_json(username, result_dir)
        #
        # # Remove the txt file
        # logger.info("Removing Instagram text file...")
        # (result_dir / username).with_suffix(".txt").unlink()
        # logger.info("Removed Instagram text file")

        print(json.dumps({"INFO": "Instagram data fetched"}))
        logger.info("Fetched Instagram data")

    except Exception as err:
        logger.exception("Exception occurred")
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": "Error occurred while fetching Instagram data, see logs for more details."}))
