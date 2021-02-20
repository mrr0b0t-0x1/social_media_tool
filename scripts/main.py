import sys
sys.path.append("..")

from globals import ROOT_DIR
from scripts.timer_module import Timer
from scripts import sherlock_module, reddit_module, instagram_module, twitter_module, facebook_module, validate_username
from scripts import database
import multiprocessing
from colorama import Fore


def make_dirs(sites):
    if sites:
        for site in sites:
            # Create required directory
            result_dir = ROOT_DIR / "scripts" / "results" / username / site.lower().replace(' ', '_')
            try:
                result_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))


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


# Main
if __name__ == '__main__':
    # Get username as input
    username = str(sys.argv[1])

    # Validate the username
    result = validate_username.validate(username)

    if result == True:

        # Timer
        t = Timer()
        # Start timer
        t.start()

        # Initialize database connection
        with database.DatabaseConnection(username) as db:

            if not db.check_user():
                print(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " not in DB")

                # Get the list of sites on which user exists
                # sites_found = sherlock_module.check_username(username)
                # # sites_found = ['Twitter', 'Instagram', 'Reddit']    # debug
                #
                # # Make respective module directories
                # make_dirs(sites_found)
                #
                # # If sites found, execute respective modules concurrently
                # if sites_found:
                #     try:
                #         with multiprocessing.Pool() as pool:
                #             pool.map(execute_module, sites_found)
                #
                #         db.update_user()
                #     except Exception as err:
                #         print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))
                # else:
                #     print('\nUsername not found on any of the social media websites\n')

            else:
                print(Fore.RED + "ERROR" + ": " + Fore.RESET + username + " in DB")

                db.get_data()

        # with database.DatabaseConnection('') as db:
        #     db.reindex_db()

        # Stop timer
        t.stop()

    else:
        print(Fore.RED + "ERROR" + Fore.RESET + ": " + result)
