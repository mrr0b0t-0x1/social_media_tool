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
