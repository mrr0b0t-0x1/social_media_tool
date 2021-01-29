import subprocess
from globals import CWD
import json

def gather_info(username):
    """
    Gathers information about a user from his Instagram profile
    :param username:
    :return:
    """

    # Target directory
    result_dir = CWD / "results" / username / "instagram"

    # Run instagram-scraper as a subprocess
    # subprocess.run([
    #     "python",
    #     "./venv/bin/instagram-scraper",
    #     "-u", "pyvma_1990",
    #     "-p", "i652HD9dkbUFWLMGn647",
    #     username,
    #     "--profile-metadata",
    #     "-m", "10"
    # ], shell=False)
    subprocess.run([
        "python", "./venv/bin/instagram-scraper",
        username,
        "--profile-metadata",
        "-m", "10",
        "-d", result_dir
    ], shell=False)

    # Read data from result file
    try:
        with open(result_dir / (username + ".json"), "r") as about:
            data = json.load(about)

        # TODO: Remove this in final build
        # Print result data
        print('\nInstagram Data:')
        print(json.dumps(data, indent=2))
    except OSError as err:
        print(err)

    # Remove instagram-scraper's log file
    try:
        (CWD / "instagram-scraper.log").unlink()
    except FileNotFoundError as err:
        print(err)