from json2html import *

def convert(data):
    return json2html.convert(
        json=data,
        table_attributes="class = \"table table-condensed table-sm table-bordered table-hover fs-smaller\""
    )
