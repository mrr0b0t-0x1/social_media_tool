from globals import CWD
from scripts.timer_module import Timer
from scripts import reddit_module, sherlock_module, instagram_module, twitter_module, facebook_module, validate_username
import multiprocessing
from colorama import Fore


def make_dirs(sites):
    if sites:
        for site in sites:
            # Create required directory
            result_dir = CWD / "scripts" / "results" / username / site.lower().replace(' ', '_')
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
    # elif site == 'Facebook':
    #     facebook_module.gather_info(username)


# Main
if __name__ == '__main__':
    # Get username as input
    username = ''
    while True:
        try:
            username = str(input("Enter a username: "))
            # Validate the username
            if validate_username.validate(username):
                break
        except Exception as err:
            print(err)
    # username = "billgates"    # debug

    # Timer
    t = Timer()
    # Start timer
    t.start()

    # Get the list of sites on which user exists
    sites_found = sherlock_module.check_username(username)
    # sites_found = ['Twitter', 'Instagram', 'Reddit']    # debug

    # Make respective module directories
    make_dirs(sites_found)

    # If sites found, execute respective modules concurrently
    if sites_found:
        with multiprocessing.Pool() as pool:
            pool.map(execute_module, sites_found)
    else:
        print('\nUsername not found on any of the social media websites\n')

    # Stop timer
    t.stop()
