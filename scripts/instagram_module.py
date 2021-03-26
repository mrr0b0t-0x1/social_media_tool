import subprocess
from globals import ROOT_DIR
import json
from colorama import Fore

def fix_filename(username, result_dir):
    if (result_dir / (username + ".json")).exists():
        (result_dir / (username + ".json")).rename(
            result_dir / (username + "-about-instagram.json")
        )

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
        subprocess.run([
            "python", ROOT_DIR / "venv1/bin/instagram-scraper", "-q",
            username,
            "--profile-metadata",
            "--include-location",
            "-m", "10",
            "-d", result_dir
        ], shell=False, stdout=subprocess.DEVNULL, check=True)

        fix_filename(username, result_dir)

        # Read data from result file
        # with open(result_dir / (username + ".json"), "r") as about:
        #     data = json.load(about)

        # TODO: Remove this in final build
        # Print result data
        # print('\nInstagram Data:')
        # print(json.dumps(data, indent=2))

        # Remove instagram-scraper's log file
        if (ROOT_DIR / "ui" / "instagram-scraper").with_suffix(".log").exists():
            (ROOT_DIR / "ui" / "instagram-scraper").with_suffix(".log").unlink()
        elif (ROOT_DIR / "instagram-scraper").with_suffix(".log").exists():
            (ROOT_DIR / "instagram-scraper").with_suffix(".log").unlink()

        print(json.dumps({"INFO": "Instagram data fetched"}))

    except Exception as err:
        # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
        print(json.dumps({"ERROR": str(err)}))
