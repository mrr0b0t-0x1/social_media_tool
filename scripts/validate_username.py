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

import re

# Validate username based on whitelist
def validate(username):
    # Invalidate empty input
    if len(username) < 1:
        return 'Username cannot be empty'

    # Invalidate input greater than 50 characters
    elif len(username) > 50:
        return 'Username too long'

    # Invalidate single-digit input that doesn't contain
    # alpha-numeric characters and underscores
    elif len(username) == 1:
        regex = re.compile("^[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else 'Invalid username'

    # Invalidate any input that doesn't contain alpha-numeric characters,
    # underscores, hyphens or periods. Also invalidate any input containing
    # two consecutive hyphens or periods
    else:
        regex = re.compile("^[\w](?!.*[-.]{2})[_.\w-]*[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else 'Invalid username'
