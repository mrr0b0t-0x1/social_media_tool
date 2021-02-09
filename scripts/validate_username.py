import re

# Validate username based on whitelist
def validate(username):
    # Invalidate empty input
    if len(username) < 1:
        print('Username cannot be empty\n')

    # Invalidate input greater than 50 characters
    elif len(username) > 50:
        print('Username too long\n')

    # Invalidate single-digit input that doesn't contain
    # alpha-numeric characters and underscores
    elif len(username) == 1:
        regex = re.compile("^[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else print('Invalid username\n')

    # Invalidate any input that doesn't contain alpha-numeric characters,
    # underscores, hyphens or periods. Also invalidate any input containing
    # two consecutive hyphens or periods
    else:
        regex = re.compile("^[\w](?!.*[-.]{2})[_.\w-]*[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else print('Invalid username\n')
