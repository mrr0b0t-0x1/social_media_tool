import sys
sys.path.append("..")

from globals import ROOT_DIR
from scripts.timer_module import Timer
from scripts import sherlock_module, reddit_module, instagram_module, \
    twitter_module, facebook_module, validate_username, json_to_html_table
from scripts import database
import multiprocessing
from colorama import Fore
import json
import time


def make_dirs(sites):
    if sites:
        for site in sites:
            # Create required directory
            result_dir = ROOT_DIR / "scripts" / "results" / username / site.lower().replace(' ', '_')
            try:
                result_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                # print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))
                print(json.dumps({"ERROR": str(e)}))


# Execute respective site modules
def execute_module(site):
    # Twitter
    if site == 'Twitter':
        twitter_module.gather_info(username)

    # Reddit
    elif site == 'Reddit':
        reddit_module.gather_info(username)

    # Instagram
    elif site == 'Instagram':
        instagram_module.gather_info(username)

    # Facebook
    elif site == 'Facebook':
        facebook_module.gather_info(username)


# Run the search operation
def run_search(uname, dbs):
    # Get the list of sites on which user exists
    sites_found = sherlock_module.check_username(uname)
    # sites_found = ['Twitter', 'Instagram', 'Reddit']    # debug

    # Make respective module directories
    make_dirs(sites_found)

    # If sites found, execute respective modules concurrently
    if sites_found:
        try:
            with multiprocessing.Pool() as pool:
                pool.map(execute_module, sites_found)

            # Update user data in DB
            dbs.update_user()

            # Get data from DB
            print(json.dumps({"DATA": dbs.get_data()}))

        except Exception as err:
            # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
            print(json.dumps({"ERROR": str(err)}))

    else:
        print(json.dumps({"ERROR": "Username not found on any of the social media websites."}))


# Main
if __name__ == '__main__':

    # Search or update data
    if sys.argv[1] == '--username':
        # Get username as input
        username = str(sys.argv[2])

        result = validate_username.validate(username)

        if result == True:

            # Timer
            t = Timer()
            # Start timer
            t.start()

            # Initialize database connection
            with database.DatabaseConnection(username) as db:

                if sys.argv[3] == '--search':
                    if not db.check_user():
                        # print(json.dumps(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " not in DB"))
                        print(json.dumps({"INFO": username + " does not exist in local database!"}))

                        run_search(username, db)

                    else:
                        # print(json.dumps(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " in DB"))
                        print(json.dumps({"INFO": username + " exists in local database!"}))

                        # Get data from DB
                        print(json.dumps({"DATA": db.get_data()}))

                elif sys.argv[3] == '--update':
                    run_search(username, db)

            # Stop timer
            print(json.dumps({"ELAPSED_TIME": t.stop()}))

        else:
            # print(json.dumps(Fore.RED + "ERROR" + Fore.RESET + ": " + result))
            print(json.dumps({"ERROR": str(result)}))

    # Convert JSON data to HTML Table format
    elif sys.argv[1] == '--json-to-html':
        data = json.loads(sys.argv[2])
        try:
            print(json.dumps({"DATA": json_to_html_table.convert(data)}))
            # print(json_to_html_table.convert(data))
        except Exception as err:
            print(json.dumps({"ERROR": str(err)}))
            # print(str(err))

    # Remove Data
    elif sys.argv[1] == '--remove-data':
        username = str(sys.argv[2])
        print(json.dumps({"INFO": str(username) + ' remove-db elif block'}))

    # Re-index DB
    elif sys.argv[1] == '--reindex-db':
        try:
            with database.DatabaseConnection('') as db:
                db.reindex_db()
        except Exception as e:
            print(json.dumps({"ERROR": str(e)}))
