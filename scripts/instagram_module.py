import subprocess
from globals import ROOT_DIR
import json
import re
from colorama import Fore


# Fix filename for consistency
def fix_filename(username, result_dir):
    if (result_dir / (username + ".json")).exists():
        (result_dir / (username + ".json")).rename(
            result_dir / (username + "-about-instagram.json")
        )

# Strip ANSI colors from output for osi.ig scraper
def strip_color(username, result_dir):
    try:
        with open((result_dir / username).with_suffix(".txt"), "r") as handle:
            lines = handle.readlines()
        with open((result_dir / username).with_suffix(".txt"), "w") as handle:
            for line in lines:
                handle.writelines(re.sub("\033\\[([0-9]+)(;[0-9]+)*m", "", line))
    except FileNotFoundError as err:
        print(json.dumps({"ERROR": str(err)}))

# Convert data to JSON for osi.ig scraper
def convert_to_json(username, result_dir):
    data = {}
    private = False
    try:
        # Open the txt fiel and convert data to dictionary
        with open((result_dir / username).with_suffix(".txt"), "r") as handle:
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
                            print(json.dumps({"ERROR": username + " is not verified on Instagram, unable to fetch data"}))
                            return

                        elif key == "private" and val == "True":
                            private = True
                            print(json.dumps({"ERROR": username + "'s profile is private on Instagram, unable to fetch posts"}))

                        else:
                            temp[key] = val

        # Store about data in JSON
        with open((result_dir / (username + "-about-insta")).with_suffix(".json"), "w") as handle:

            about_keys = [key for key in data.keys() if key.startswith(tuple(['user_info', 'most_used']))]
            about = {}
            for key in about_keys:
                if key == "user_info":
                    about = data['user_info']
                else:
                    about[key] = data[key]

            json.dump(about, handle, indent=2)

        # Store posts data in JSON if not private
        if not private:
            with open((result_dir / (username + "-posts-insta")).with_suffix(".json"), "w") as handle:

                posts_keys = [key for key in data.keys() if key.startswith('post')]
                posts = {}
                for key in posts_keys:
                    posts[key] = data[key]

                json.dump(posts, handle, indent=2)

    except Exception as err:
        print(json.dumps({"ERROR": str(err)}))


def gather_info(username):
    """
    Gathers information about a user from his Instagram profile
    :param username:
    :return:
    """

    print(json.dumps({"INFO": "Fetching Instagram Data..."}))

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
        # # with open(result_dir / (username + ".json"), "r") as about:
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
        with open((result_dir / username).with_suffix(".txt"), "w") as handle:
            try:
                subprocess.run([
                    "python", ROOT_DIR / "venv1" / "src" / "osi.ig" / "main.py",
                    "-u", username, "-p"
                ], shell=False, stdout=handle, check=True)
            except Exception as err:
                print(json.dumps({"ERROR": "Some error occurred while fetching Instagram data"}))

        # Strip colors from output
        strip_color(username, result_dir)

        # Convert output to JSON
        convert_to_json(username, result_dir)

        # Remove the txt file
        (result_dir / username).with_suffix(".txt").unlink()

        print(json.dumps({"INFO": "Instagram data fetched"}))

    except Exception as err:
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": str(err)}))
