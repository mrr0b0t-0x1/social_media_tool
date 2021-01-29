import requests
import json
import bs4
from globals import CWD

def gather_info(username):
    """
    Gathers information about a user from his Facebook profile or page
    :param username:
    :return:
    """

    # Target directory
    result_dir = CWD / "results" / username / "facebook"

    # Dictionary to store result data
    facebook_user_info = {
        "about_user": {
            "about": '',
            "contact": {},
            "city_home": {},
            "education": {},
            "work": {},
            "fav_quotes": ''
        },
        "favourites": {
            "music": {},
            "books": {},
            "films": {},
            "television": {},
            "games": {},
            "athletes": {},
            "sports_teams": {},
            "inspirational_people": {},
            "other": {}
        },
        "photos": {}
    }

    # Fetch the Facebook page of user
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.7.12) Gecko/20100101 Firefox/80.0',
        'Accept-Language': 'en-GB,en;q=0.5'
    }
    res = requests.get('https://en-gb.facebook.com/' + username, headers=headers)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Get about user
    about_user = soup.select('div.clearfix._h71')
    for section in about_user:
        sec_name = section.span.getText().lower()

        sec_con = section.next_sibling

        if sec_name == 'work':
            get_work(facebook_user_info, sec_con)

        elif sec_name == 'education':
            get_edu(facebook_user_info, sec_con)

        elif sec_name == 'current city and home town':
            get_city_home(facebook_user_info, sec_con)

        elif 'about' in sec_name:
            get_about(facebook_user_info, sec_con)

        elif sec_name == 'favourite quotes':
            get_fav_quotes(facebook_user_info, sec_con)

        elif sec_name == 'contact information':
            get_contact(facebook_user_info, sec_con)

        else:
            continue

    # Get favourites
    favourites = soup.select('div._5h60.allFavorites th.label')
    for section in favourites:
        sec_name = section.get_text().lower().replace(' ', '_')

        sec_con = section.next_sibling

        get_favourites(facebook_user_info, sec_name, sec_con)

    # Get photos
    get_photos(facebook_user_info, soup.select('div._xcx img'))

    # Store result data to file
    try:
        with open(result_dir / (username + "-fb-user.json"), "w+") as handle:
            json.dump(facebook_user_info, handle, indent=2)
    except OSError as err:
        print(err)

    # TODO: Remove this in final build
    # Print result data
    print(json.dumps(facebook_user_info, indent=2))


def get_work(facebook_user_info, sec_con):
    """
    Gathers information from Work section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    all_items = sec_con.find_all('li')
    i = 0

    for item in all_items:
        facebook_user_info['about_user']['work'][i] = {}

        if item.find('div', class_='_2lzr _50f5 _50f7') is not None:
            facebook_user_info['about_user']['work'][i]['company_name'] = item.select('div._2lzr._50f5._50f7 a')[
                0].get_text()
            facebook_user_info['about_user']['work'][i]['company_link'] = \
                item.select('div._2lzr._50f5._50f7 a')[0].attrs['href']

        if item.find('div', class_='fsm fwn fcg') is not None:
            facebook_user_info['about_user']['work'][i]['work_details'] = item.select('div.fsm.fwn.fcg')[
                0].get_text().split(' · ')

        if item.find('div', class_='_3-8w _50f8') is not None:
            facebook_user_info['about_user']['work'][i]['description'] = item.select('div._3-8w._50f8')[
                0].get_text()

        if item.find('img', class_='img') is not None:
            facebook_user_info['about_user']['work'][i]['image'] = item.select('div._2tdc img')[0].attrs[
                'src'].replace('amp;', '')

        i += 1

    return


def get_edu(facebook_user_info, sec_con):
    """
    Gathers information from Education section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    all_items = sec_con.find_all('li')
    i = 0

    for item in all_items:
        facebook_user_info['about_user']['education'][i] = {}

        if item.find('div', class_='_2lzr _50f5 _50f7') is not None:
            facebook_user_info['about_user']['education'][i]['institute_name'] = \
                item.select('div._2lzr._50f5._50f7 a')[0].get_text()
            facebook_user_info['about_user']['education'][i]['institute_link'] = \
                item.select('div._2lzr._50f5._50f7 a')[0].attrs['href']

        if item.find('div', class_='fsm fwn fcg') is not None:
            facebook_user_info['about_user']['education'][i]['graduation_details'] = item.select('div.fsm.fwn.fcg')[
                0].get_text().split(' · ')

        if item.find('div', class_='_3-8w _50f8') is not None:
            facebook_user_info['about_user']['education'][i]['description'] = item.select('div._3-8w._50f8')[
                0].get_text()

        if item.find('img', class_='img') is not None:
            facebook_user_info['about_user']['education'][i]['image'] = item.select('div._2tdc img')[0].attrs[
                'src'].replace('amp;', '')

        i += 1

    return


def get_city_home(facebook_user_info, sec_con):
    """
    Gathers information from Current City and Home section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    all_items = sec_con.find_all('li')
    i = 0

    for item in all_items:
        facebook_user_info['about_user']['city_home'][i] = {}

        if item.find('div', class_='_6a _6b') is not None:
            facebook_user_info['about_user']['city_home'][i]['city'] = item.select('div._6a._6b span')[0].get_text()

        if item.find('img', class_='img') is not None:
            facebook_user_info['about_user']['city_home'][i]['image'] = item.select('div img')[0].attrs[
                'src'].replace(
                'amp;', '')

        i += 1

    return


def get_about(facebook_user_info, sec_con):
    """
    Gathers information from About section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    item = sec_con.find('li')

    if item.find('div', class_='_4bl9') is not None:
        facebook_user_info['about_user']['about'] = item.select('div._4bl9 span')[0].get_text()

    elif sec_con.find('li', class_='_3pw9 _2pi4') is not None:
        facebook_user_info['about_user']['about'] = sec_con.select('li._3pw9._2pi4')[0].get_text()

    return


def get_fav_quotes(facebook_user_info, sec_con):
    """
    Gathers information from Favourite Quotes section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    item = sec_con.find('li')

    if item.find('div', class_='_4bl9') is not None:
        facebook_user_info['about_user']['fav_quotes'] = item.select('div._4bl9 span')[0].get_text()

    return


def get_contact(facebook_user_info, sec_con):
    """
    Gathers information from Contact section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_con:
    :return:
    """

    all_items = sec_con.find_all('li', class_='_3pw9 _2pi4 _2ge8')
    i = 0

    for item in all_items:
        facebook_user_info['about_user']['contact'][i] = {}

        if item.find('div', class_='_4bl7 _3xdi _52ju') is not None:
            facebook_user_info['about_user']['contact'][i][
                item.select('div._4bl7._3xdi._52ju span')[0].get_text()] = \
                item.select('span._50f7')[0].get_text()

        i += 1

    return


def get_favourites(facebook_user_info, sec_name, sec_con):
    """
    Gathers information from Favourites section of the user's Facebook profile or page
    :param facebook_user_info:
    :param sec_name:
    :param sec_con:
    :return:
    """

    if sec_name != 'other':
        item = sec_con.find('li')

        facebook_user_info['favourites'][sec_name]['name'] = item.select('div.mediaPageName')[0].get_text()
        facebook_user_info['favourites'][sec_name]['link'] = item.select('a.mediaRowItem')[0].attrs['href']
        facebook_user_info['favourites'][sec_name]['image'] = item.select('img')[0].attrs['src'].replace('amp;', '')

    else:
        items = sec_con.select('div#u_0_e a')
        for i in range(0, len(items)):
            facebook_user_info['favourites'][sec_name][i] = items[i].get_text()

    return


def get_photos(facebook_user_info, items):
    """
    Gathers photos from Photos section of the user's Facebook profile or page
    :param facebook_user_info:
    :param items:
    :return:
    """

    for i in range(0, len(items)):
        facebook_user_info['photos'].update(
            {i: {'src': items[i].attrs['src'].replace('amp;', ''),
                 'src_set': items[i].attrs['data-src'].replace('amp;', ''),
                 'height': items[i].attrs['height'],
                 'width': items[i].attrs['width'],
                 'caption': items[i].attrs['caption']
                 }
             }
        )

    return
