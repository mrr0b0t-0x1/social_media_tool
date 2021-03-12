import subprocess
import re
import json
from globals import ROOT_DIR

# Check username in Sherlock
def check_username(username):
    """
    Passes username to the Sherlock tool to check whether the user exists on any social media platforms
    :param username:
    :return:
    """

    # Run sherlock as a subprocess
    try:
        res = subprocess.run([
            "python", ROOT_DIR / "venv1/src/sherlock/sherlock",
            username,
            "--site", "Twitter",
            "--site", "Reddit",
            "--site", "Instagram",
            "--site", "Facebook",
            "--print-found",
            "--local",
            "--no-color"
        ], shell=False, stdout=subprocess.PIPE)

        print(json.dumps({"INFO": res.stdout.decode('utf-8')}))

        # Remove the text file made by Sherlock
        if (ROOT_DIR / "ui" / username).with_suffix('.txt').exists():
            (ROOT_DIR / "ui" / username).with_suffix('.txt').unlink()
        elif (ROOT_DIR / username).with_suffix('.txt').exists():
            (ROOT_DIR / username).with_suffix('.txt').unlink()

        # Pattern to get site names on which username is found
        pattern = "\[\+\]\s([A-Z][a-z]+)\:"

        # Returns list of sites on which username was found
        return re.findall(pattern, str(res.stdout))

    except Exception as err:
        print(json.dumps({"ERROR": str(err)}))


