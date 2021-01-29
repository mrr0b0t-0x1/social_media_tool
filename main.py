import subprocess
from globals import CWD
from pathlib import Path
from timer_module import Timer
import sherlock_module
import twitter_module
import instagram_module
import reddit_module
import facebook_module

# Main
if __name__ == '__main__':
    # Get username as input
    username = input("Enter a username : ")

    # Timer
    t = Timer()
    # Start timer
    t.start()

    # Get the list of sites on which user exists
    sites_found = sherlock_module.check_username(username)
    # sites_found = ['Twitter', 'Instagram', 'Reddit']      # For debug

    if sites_found:

        for site in sites_found:
            # Create required directory
            result_dir = CWD / "results" / username / site.lower().replace(' ', '_')
            try:
                result_dir.mkdir(parents=True)
            except OSError as err:
                print(err)

            # Execute respective module
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

    else:
        print('\nUsername not found on any of the social media websites\n')

    # Stop timer
    t.stop()
