import subprocess
from globals import CWD
import json
from colorama import Fore

def gather_info(username):
    """
    Gathers information about a user from his Instagram profile
    :param username:
    :return:
    """

    print('Fetching Instagram Data...\n')

    # Target directory
    result_dir = CWD / "scripts" / "results" / username / "instagram"

    # Run instagram-scraper as a subprocess
    subprocess.run([
        "python",
        "./venv/bin/instagram-scraper", "-q",
        "-u", "pyvma_1990",
        "-p", "i652HD9dkbUFWLMGn647",
        username,
        "--profile-metadata",
        "-m", "10",
        "-d", result_dir
    ], shell=False, stdout=subprocess.DEVNULL, check=True)
    # subprocess.run([
    #     "python", CWD / "venv/bin/instagram-scraper",
    #     username,
    #     "--profile-metadata",
    #     "-m", "10",
    #     "-d", result_dir
    # ], shell=False)

    # Read data from result file
    try:
        with open(result_dir / (username + ".json"), "r") as about:
            data = json.load(about)

        # TODO: Remove this in final build
        # Print result data
        # print('\nInstagram Data:')
        # print(json.dumps(data, indent=2))
        print('Instagram data fetched\n')
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))

    # Remove instagram-scraper's log file
    try:
        (CWD / "instagram-scraper.log").unlink()
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
