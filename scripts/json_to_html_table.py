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
