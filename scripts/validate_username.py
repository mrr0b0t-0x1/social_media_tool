import re

# Validate username based on whitelist
def validate(username):
    # Invalidate empty input
    if len(username) < 1:
        return 'Username cannot be empty'

    # Invalidate input greater than 50 characters
    elif len(username) > 50:
        return 'Username too long'

    # Invalidate single-digit input that doesn't contain
    # alpha-numeric characters and underscores
    elif len(username) == 1:
        regex = re.compile("^[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else 'Invalid username'

    # Invalidate any input that doesn't contain alpha-numeric characters,
    # underscores, hyphens or periods. Also invalidate any input containing
    # two consecutive hyphens or periods
    else:
        regex = re.compile("^[\w](?!.*[-.]{2})[_.\w-]*[\w]$", re.ASCII)
        match = regex.search(username)
        return bool(match) if bool(match) else 'Invalid username'
