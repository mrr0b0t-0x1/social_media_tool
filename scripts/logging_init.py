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

import sys
sys.path.append("..")

from globals import ROOT_DIR
import logging

FORMAT = '\n---------------------------------------------------------------------------------------\n%(asctime)s - %(message)s\n---------------------------------------------------------------------------------------\n'

logger_init = logging.getLogger(__name__)
fh = logging.FileHandler(filename=ROOT_DIR / 'logs' / 'app.log')
formatter = logging.Formatter(fmt=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(fmt=formatter)
fh.setLevel(logging.INFO)
logger_init.addHandler(fh)
logger_init.propagate = False


if __name__ == '__main__':
    if sys.argv[1] == '--start':
        logger_init.info("Started")
    elif sys.argv[1] == '--stop':
        logger_init.info("Stopped")
        logging.shutdown()
