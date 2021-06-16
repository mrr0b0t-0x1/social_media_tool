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

import argparse

def get_parser():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Social Media Tool - A tool to gather information about a user from multiple social networks"
    )

    # First mutually exclusive group
    group1 = parser.add_mutually_exclusive_group()

    # Second mutually exclusive group
    group2 = parser.add_mutually_exclusive_group()

    # Add the arguments
    group1.add_argument(
        "--username",
        type=str,
        help="Username to be searched"
    )
    group2.add_argument(
        "--search",
        action="store_true",
        help="Search about the user online, use with --username"
    )
    group2.add_argument(
        "--update",
        action="store_true",
        help="Update locally stored user data, use with --username"
    )
    group2.add_argument(
        "--remove",
        action="store_true",
        help="Remove all locally stored user data, use with --username"
    )
    group1.add_argument(
        "--json_to_html",
        metavar="DATA",
        type=str,
        help="Convert JSON data to HTML table"
    )
    group1.add_argument(
        "--reindex_db",
        action="store_true",
        help="Re-index database to remove discrepancy"
    )

    return parser
