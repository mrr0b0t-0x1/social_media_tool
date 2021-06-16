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

from json2html import *
import logging

# Start a logger
logger = logging.getLogger('json to html module')

def convert(data):
    logger.info("Converting JSON data to HTML Table")
    return json2html.convert(
        json=data,
        table_attributes="class = \"table table-condensed table-sm table-bordered table-hover fs-smaller\""
    )
