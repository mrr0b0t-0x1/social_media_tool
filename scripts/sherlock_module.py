import subprocess
import re
from globals import CWD

# Check username in Sherlock
def check_username(username):
    """
    Passes username to the Sherlock tool to check whether the user exists on any social media platforms
    :param username:
    :return:
    """

    # Run sherlock as a subprocess
    # res = subprocess.run("python3 /home/mrr0b0t/Downloads/Git_Repos/sherlock/sherlock/sherlock.py " + username + " --site Twitter --site Reddit --site Instagram --site Facebook --print-found --local --no-color", shell=True, stdout=subprocess.PIPE)
    res = subprocess.run([
        "python", CWD / "venv/src/sherlock/sherlock",
        username,
        "--site", "Twitter",
        "--site", "Reddit",
        "--site", "Instagram",
        "--site", "Facebook",
        "--print-found",
        "--local",
        "--no-color"
    ], shell=False, stdout=subprocess.PIPE)
    # res = subprocess.run("python3 /home/mrr0b0t/Downloads/Git_Repos/sherlock/sherlock/sherlock.py " + username + " --site Facebook --print-found --no-color", shell=True, stdout=subprocess.PIPE)

    print(res.stdout.decode('utf-8'))

    # Remove the text file made by Sherlock
    try:
        (CWD / username).with_suffix('.txt').unlink()
    except FileNotFoundError as err:
        print(err)

    # Pattern to get site names on which username is found
    pattern = "\[\+\]\s([A-Z][a-z]+)\:"

    # Returns list of sites on which username was found
    return re.findall(pattern, str(res.stdout))
