import subprocess
import re
import json
from globals import ROOT_DIR
import logging

# Start a logger
logger = logging.getLogger('sherlock module')

# Check username in Sherlock
def check_username(username):
    """
    Passes username to the Sherlock tool to check whether the user exists on any social media platforms
    :param username:
    :return:
    """

    # Run sherlock as a subprocess
    try:
        logger.info("Running sherlock...")
        res = subprocess.run([
            "python", ROOT_DIR / "venv1" / "src" / "sherlock" / "sherlock",
            username,
            "--site", "Twitter",
            "--site", "Reddit",
            "--site", "Instagram",
            "--site", "Facebook",
            "--print-found",
            "--local",
            "--no-color"
        ], shell=False, stdout=subprocess.PIPE)
        logger.info("Executed sherlock successfully")

        print(json.dumps({"INFO": res.stdout.decode('utf-8')}))

        logger.info("Removing sherlock log file...")
        # Remove the text file made by Sherlock
        if (ROOT_DIR / "ui" / username).with_suffix('.txt').exists():
            (ROOT_DIR / "ui" / username).with_suffix('.txt').unlink()
        elif (ROOT_DIR / username).with_suffix('.txt').exists():
            (ROOT_DIR / username).with_suffix('.txt').unlink()
        logger.info("Removed sherlock log file")

        # Pattern to get site names on which username is found
        pattern = "\[\+\]\s([A-Z][a-z]+)\:"

        logger.info("Returning sites found...")
        # Returns list of sites on which username was found
        return re.findall(pattern, str(res.stdout))

    except Exception as err:
        logger.exception("Exception occurred")
        print(json.dumps({"ERROR": "Error occurred while searching username, see logs for more details."}))


