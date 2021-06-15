import sys
sys.path.append("..")

from globals import ROOT_DIR
from scripts.timer_module import Timer
from scripts import sherlock_module, reddit_module, instagram_module, \
    twitter_module, facebook_module, validate_username, json_to_html_table
from scripts import database
import multiprocessing
import logging
# from colorama import Fore
import json
import scripts.arg_parser as ap

# Get an argument parser
parser = ap.get_parser()

# Start a logger
logger = logging.getLogger('main')

# Make directories
def make_dirs(username, sites):
    if sites:
        logger.info(f"Creating directory for {username}...")
        for site in sites:
            # Create required directory
            result_dir = ROOT_DIR / "scripts" / "results" / username / site.lower().replace(' ', '_')
            try:
                logger.info(f"Creating sub-directory for {str(site)}")
                result_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created sub-directory for {str(site)}")
            except Exception as e:
                logger.exception("Exception occurred")
                # print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))
                print(json.dumps({"ERROR": "Error occurred while creating directories, see logs for more details."}))


# Execute respective site modules
def execute_module(username, site):
    logger.info(f"Executing {site} module...")
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

    logger.info(f"Executed {str(site).capitalize()} module")


# Run the search operation
def run_search(username, dbs):
    # Get the list of sites on which user exists
    logger.info("Starting sherlock search...")
    sites_found = sherlock_module.check_username(username)
    logger.info("Sherlock search finished")
    # sites_found = ['Twitter', 'Instagram', 'Reddit']    # debug

    # Make respective module directories
    logger.info("Creating respective directories...")
    make_dirs(username, sites_found)
    logger.info("Directories created")

    # If sites found, execute respective modules concurrently
    if sites_found:
        logger.info("Sites are found")
        try:
            logger.info("Starting multiprocessing module...")
            with multiprocessing.Pool() as pool:
                logger.info("Executing respective site modules...")
                pool.starmap(execute_module, [(username, site) for site in sites_found])
                logger.info("Site modules executed")

            # Update user data in DB
            logger.info("Updating database with gathered data")
            dbs.update_user()
            logger.info("Database updated")

            # Get data from DB
            logger.info("Fetching data...")
            print(json.dumps({"DATA": dbs.get_data()}))
            logger.info("Data fetched")

        except Exception as err:
            logger.exception("Exception occurred")
            # print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
            print(json.dumps({"ERROR": "Error occurred while gathering data, see logs for more details."}))

    else:
        logger.error("Username not found on any of the social media websites")
        print(json.dumps({"ERROR": "Username not found on any of the social media websites."}))


# Main
if __name__ == '__main__':
    # Parse args
    args = parser.parse_args()

    # If no args are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    # Check if --search, --update or --remove is used without --username
    if not args.username and (args.search or args.update or args.remove):
        parser.error("Specify username with --username flag to perform this operation")
    # Check if --search, --update or --remove is not used with --username
    if args.username and not (args.search or args.update or args.remove):
        parser.error("Specify operation with --username: --search, --update or --remove")

    logger.info("Starting main module")

    # Timer
    t = Timer()
    # Start timer
    t.start()
    logger.info("Timer started")

    # Search or update data
    if args.username and (args.search or args.update):
        logger.info("Operation: Search or Update user data")

        # Get username as input
        username = str(args.username)
        logger.info(f"Username = {username}")

        logger.info("Validating username...")
        result = validate_username.validate(username)
        logger.info("Username validated")

        if result == True:
            logger.info("Username is valid")

            try:
                logger.info("Establishing database connection...")
                # Initialize database connection
                with database.DatabaseConnection(username) as db:
                    logger.info("Database connection established")

                    logger.info("Checking search type...")
                    if args.search:
                        logger.info("Operation type: 'search'")

                        logger.info("Checking user in database...")
                        if not db.check_user():
                            logger.info("User does not exists in database")

                            # print(json.dumps(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " not in DB"))
                            print(json.dumps({"INFO": f"{username} does not exist in local database!"}))

                            logger.info("Starting search...")
                            run_search(username, db)
                            logger.info("Search finished")

                        else:
                            logger.info("User exists in database")
                            # print(json.dumps(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " in DB"))
                            print(json.dumps({"INFO": f"{username} exists in local database!"}))

                            # Get data from DB
                            logger.info("Fetching user data...")
                            print(json.dumps({"DATA": db.get_data()}))
                            logger.info("User data fetched")

                    elif args.update:
                        logger.info("Operation type: 'update'")

                        logger.info("Updating user data...")
                        db.remove_user()
                        run_search(username, db)
                        logger.info("User data updated")

                    logger.info("Database connection terminated")

            except Exception as err:
                logger.exception("Exception occurred")
                print(json.dumps({"ERROR": "Error occurred while fetching data, see logs for more details."}))

        else:
            logger.error("Username is invalid")
            # print(json.dumps(Fore.RED + "ERROR" + Fore.RESET + ": " + result))
            print(json.dumps({"ERROR": str(result)}))

    # Convert JSON data to HTML Table format
    elif args.json_to_html:
        logger.info("Operation: Convert JSON to HTML Table")

        logger.info("Loading JSON data...")
        data = json.loads(args.json_to_html)
        logger.info("JSON data loaded")

        try:
            logger.info("Converting data...")
            print(json.dumps({"DATA": json_to_html_table.convert(data)}))
            # print(json_to_html_table.convert(data))
            logger.info("Data converted")
        except Exception as err:
            logger.exception("Exception occurred")
            print(json.dumps({"ERROR": "Error occurred while converting data, see logs for more details."}))
            # print(str(err))

    # Remove Data
    elif args.username and args.remove:
        logger.info("Operation: Remove user data")

        username = str(args.username)
        logger.info(f"Username = {username}")

        try:
            logger.info("Establishing database connection...")
            with database.DatabaseConnection(username) as db:
                logger.info("Database connection established")

                logger.info("Removing user data...")
                db.remove_user("rd")
                logger.info("User data removed")

            logger.info("Database connection terminated")
        except Exception as e:
            logger.exception("Exception occurred")
            print(json.dumps({"ERROR": "Error occurred while removing data, see logs for more details."}))

    # Re-index DB
    elif args.reindex_db:
        logger.info("Operation: Re-index database")
        try:
            logger.info("Establishing database connection...")
            with database.DatabaseConnection('') as db:
                logger.info("Database connection established")

                logger.info("Re-indexing database...")
                db.reindex_db()
                logger.info("Database re-indexed")

            logger.info("Database connection terminated")
        except Exception as e:
            logger.exception("Exception occurred")
            print(json.dumps({"ERROR": "Error occurred while re-indexing database, see logs for more details."}))

    # Stop timer
    logger.info("Timer stopped")
    print(json.dumps({"ELAPSED_TIME": t.stop()}))
