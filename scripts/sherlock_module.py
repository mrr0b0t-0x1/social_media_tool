"""
Social Media Tool - A tool to gather information about a user from multiple social networks
Copyright (C) 2021  Arpan Adlakhiya, Aditya Mahakalkar, Nihal Nakade and Renuka Lakhe

This file is part of Social Media Tool.

Social Media Tool is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Social Media Tool is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Social Media Tool.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import subprocess
import re
import json
from globals import ROOT_DIR, scripts_path
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
            os.path.join(scripts_path, "python"),
            os.path.join(str(ROOT_DIR), "venv1", "src", "sherlock", "sherlock"),
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


