import requests
from requests_html import HTMLSession
import bs4
import json
import re
import time
from random import randint, uniform
from globals import *
from colorama import Fore
from facebook_scraper import get_posts

# Generate new headers each time the program is run
headers = {
    'Host': 'www.facebook.com',
    'User-Agent': USER_AGENTS[randint(0, len(USER_AGENTS) - 1)],
    'Accept': 'text/html,application/xhtml+xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Referer': REFERERS[randint(0, len(REFERERS) - 1)],
    'Connection': 'keep-alive',
    'DNT': '1',
    "Upgrade-Insecure-Requests": "1",
}

# Initialize session for "requests" and "requests_html"
req_session = requests.session()
req_html_session = HTMLSession()


# Gather Facebook User info
def gather_user_info(username, home_soup, result_dir):
    """
    Gathers information about a user from his Facebook profile
    :param username:
    :param home_soup:
    :param result_dir:
    """

    # Dictionary to store result data
    facebook_user_info = {
        "about_user": {},
        "favourites": {},
        "photos": {}
    }

    # Definition of all user functions start here

    # Get Work info
    def get_user_work(work_contents):
        """
        Gathers information from Work section of the user's Facebook profile
        :param work_contents:
        """

        # Find all items in the Work section
        all_items = work_contents.find_all('li')

        if all_items:
            facebook_user_info['about_user']['work'] = {}

            for i, item in enumerate(all_items):
                facebook_user_info['about_user']['work'][i] = {}

                if item.find('div', class_='_2lzr _50f5 _50f7') is not None:
                    # Get the company name
                    facebook_user_info['about_user']['work'][i]['company_name'] = item.select(
                        'div._2lzr._50f5._50f7 a')[0].get_text()
                    # Get the company URL
                    facebook_user_info['about_user']['work'][i]['company_link'] = item.select(
                        'div._2lzr._50f5._50f7 a')[0].attrs['href']

                if item.find('div', class_='fsm fwn fcg') is not None:
                    # Get work details
                    facebook_user_info['about_user']['work'][i]['work_details'] = item.select(
                        'div.fsm.fwn.fcg')[0].get_text().split(' · ')

                if item.find('div', class_='_3-8w _50f8') is not None:
                    # Get work description
                    facebook_user_info['about_user']['work'][i]['description'] = item.select(
                        'div._3-8w._50f8')[0].get_text()

                if item.find('img', class_='img') is not None:
                    # Get company image
                    facebook_user_info['about_user']['work'][i]['image'] = item.select(
                        'div._2tdc img')[0].attrs['src'].replace('amp;', '')

        # If no items are present in Work section
        else:
            facebook_user_info['about_user']['work'] = "No work details to show"

    # Get Education info
    def get_user_edu(education_contents):
        """
        Gathers information from Education section of the user's Facebook profile
        :param education_contents:
        """

        # Find all items in the Education section
        all_items = education_contents.find_all('li')

        if all_items:
            facebook_user_info['about_user']['education'] = {}

            for i, item in enumerate(all_items):
                facebook_user_info['about_user']['education'][i] = {}

                if item.find('div', class_='_2lzr _50f5 _50f7') is not None:
                    # Get institute name
                    facebook_user_info['about_user']['education'][i]['institute_name'] = item.select(
                        'div._2lzr._50f5._50f7 a')[0].get_text()
                    # Get institute URL
                    facebook_user_info['about_user']['education'][i]['institute_link'] = item.select(
                        'div._2lzr._50f5._50f7 a')[0].attrs['href']

                if item.find('div', class_='fsm fwn fcg') is not None:
                    # Get graduation details
                    facebook_user_info['about_user']['education'][i]['graduation_details'] = item.select(
                        'div.fsm.fwn.fcg')[0].get_text().split(' · ')

                if item.find('div', class_='_3-8w _50f8') is not None:
                    # Get education description
                    facebook_user_info['about_user']['education'][i]['description'] = item.select(
                        'div._3-8w._50f8')[0].get_text()

                if item.find('img', class_='img') is not None:
                    # Get institute image
                    facebook_user_info['about_user']['education'][i]['image'] = item.select(
                        'div._2tdc img')[0].attrs['src'].replace('amp;', '')

        # If no items are present in Education section
        else:
            facebook_user_info['about_user']['education'] = "No education details to show"

    # Get City and Home details
    def get_user_city_home(city_home_contents):
        """
        Gathers information from Current City and Home section of the user's Facebook profile
        :param city_home_contents:
        """

        # Get all items in the City and Home section
        all_items = city_home_contents.find_all('li')

        if all_items:
            facebook_user_info['about_user']['city_home'] = {}

            for i, item in enumerate(all_items):
                facebook_user_info['about_user']['city_home'][i] = {}

                # Get city name
                if item.find('div', class_='_6a _6b') is not None:
                    facebook_user_info['about_user']['city_home'][i]['city'] = item.select(
                        'div._6a._6b span')[0].get_text()

                # Get city image
                if item.find('img', class_='img') is not None:
                    facebook_user_info['about_user']['city_home'][i]['image'] = item.select('div img')[0].attrs[
                        'src'].replace('amp;', '')

        # If no items are present in City and Home section
        else:
            facebook_user_info['about_user']['city_home'] = "No city or home details to show"

    # Get About info
    def get_user_about(about_contents):
        """
        Gathers information from About section of the user's Facebook profile
        :param about_contents:
        """

        # Get the About section contents
        item = about_contents.find('li')

        if item.find('div', class_='_4bl9') is not None:
            facebook_user_info['about_user']['about'] = item.select('div._4bl9 span')[0].get_text()

        elif about_contents.find('li', class_='_3pw9 _2pi4') is not None:
            facebook_user_info['about_user']['about'] = about_contents.select('li._3pw9._2pi4')[0].get_text()

        # If no items are present in About section
        else:
            facebook_user_info['about_user']['about'] = "No about details to show"

    # Get Favourite quotes
    def get_user_fav_quotes(fav_quotes_contents):
        """
        Gathers information from Favourite Quotes section of the user's Facebook profile
        :param fav_quotes_contents:
        """

        # Get the favourite quotes
        item = fav_quotes_contents.find('li')

        if item.find('div', class_='_4bl9') is not None:
            facebook_user_info['about_user']['fav_quotes'] = item.select('div._4bl9 span')[0].get_text()

        # If no items are present in Favourite quotes section
        else:
            facebook_user_info['about_user']['fav_quotes'] = "No favourite quotes to show"

    # Get Contact info
    def get_user_contact(contact_contents):
        """
        Gathers information from Contact section of the user's Facebook profile
        :param contact_contents:
        """

        # Get all items in Contact section
        all_items = contact_contents.find_all('li', class_='_3pw9 _2pi4 _2ge8')

        if all_items:
            facebook_user_info['about_user']['contact'] = {}

            for i, item in enumerate(all_items):
                facebook_user_info['about_user']['contact'][i] = {}

                if item.find('div', class_='_4bl7 _3xdi _52ju') is not None:
                    # Get the contact info details
                    facebook_user_info['about_user']['contact'][i][
                        item.select('div._4bl7._3xdi._52ju span')[0].get_text()] = \
                        item.select('span._50f7')[0].get_text()
        else:
            facebook_user_info['about_user']['contact'] = contact_contents.find('li', class_='_3pw9 _2pi4').text

    # Get Favourites info
    def get_user_favourites(fav_section, fav_contents):
        """
        Gathers information from Favourites section of the user's Facebook profile
        :param fav_section:
        :param fav_contents:
        """

        facebook_user_info['favourites'][fav_section] = {}

        # If section name is not "Other", get section item
        if fav_section != 'other':
            item = fav_contents.find('li')

            # Get item name
            facebook_user_info['favourites'][fav_section]['name'] = item.select('div.mediaPageName')[0].get_text()
            # Get item URL
            facebook_user_info['favourites'][fav_section]['link'] = item.select('a.mediaRowItem')[0].attrs['href']
            # Get item image
            facebook_user_info['favourites'][fav_section]['image'] = item.select('img')[0].attrs['src'].replace(
                'amp;', '')

        # If section name is "Other", get all items
        else:
            items = fav_contents.select('div#u_0_e a')
            for i, item in enumerate(items):
                facebook_user_info['favourites'][fav_section][i] = {}
                # Get the item name
                facebook_user_info['favourites'][fav_section][i]['name'] = item.get_text()
                # Get item link
                facebook_user_info['favourites'][fav_section][i]['link'] = item.attrs['href']

    # Get Photos
    def get_user_photos():
        """
        Gathers photos from Photos section of the user's Facebook profile
        """

        # Get the element containing photos
        items = home_soup.select('div._xcx img')
        if items:
            for i, item in enumerate(items):
                # Get the photo URL
                photo_url = item.attrs['src'].replace('amp;', '')

                # Update photo info
                facebook_user_info['photos'].update(
                    {i: {'src': photo_url,
                         'src_set': item.attrs['data-src'].replace('amp;', ''),
                         'height': item.attrs['height'],
                         'width': item.attrs['width'],
                         'caption': item.attrs['caption']
                         }
                     }
                )

                # Save the image files to a directory
                try:
                    filename = photo_url.split('/')[-1].split('?')[0]
                    photo = requests.get(photo_url, stream=True)

                    with open(result_dir / filename, 'wb') as user_photo:
                        user_photo.write(photo.content)

                except Exception as e:
                    print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))

                # Sleep for 1 second to avoid getting banned
                time.sleep(round(uniform(1, 3), 1))

        # If no photos are found
        else:
            facebook_user_info['photos'] = "No photos to show"

        # Get the profile photo
        if home_soup.find('div', class_='_1nv3 _11kg _1nv5 profilePicThumb').find('img') is not None:
            facebook_user_info['about_user']['profile_photo'] = {}
            facebook_user_info['about_user']['profile_photo']['src'] = home_soup.find(
                'div', class_='_1nv3 _11kg _1nv5 profilePicThumb').find('img').attrs['src']
            facebook_user_info['about_user']['profile_photo']['alt_text'] = home_soup.find(
                'div', class_='_1nv3 _11kg _1nv5 profilePicThumb').find('img').attrs['alt']

        # Get the Cover image
        if home_soup.find('span', id='fbCoverImageContainer').find('img', class_='coverPhotoImg photo img') is not None:
            facebook_user_info['about_user']['cover_photo'] = {}
            facebook_user_info['about_user']['cover_photo']['src'] = home_soup.find(
                'span', id='fbCoverImageContainer').find('img', class_='coverPhotoImg photo img').attrs['src']
            facebook_user_info['about_user']['cover_photo']['alt_text'] = home_soup.find(
                'span', id='fbCoverImageContainer').find('img', class_='coverPhotoImg photo img').attrs['alt']

    # Get data sections
    sections = home_soup.select('div.clearfix._h71')
    for section in sections:
        # Get the section name
        sec_name = section.span.getText().lower()

        # Get the section content
        sec_con = section.next_sibling

        # Execute all functions
        if sec_name == 'work':
            get_user_work(sec_con)

        elif sec_name == 'education':
            get_user_edu(sec_con)

        elif sec_name == 'current city and home town':
            get_user_city_home(sec_con)

        elif 'about' in sec_name:
            get_user_about(sec_con)

        elif sec_name == 'favourite quotes':
            get_user_fav_quotes(sec_con)

        elif sec_name == 'contact information':
            get_user_contact(sec_con)

        else:
            continue

    # Get favourites
    favourites = home_soup.select('div._5h60.allFavorites th.label')
    for section in favourites:
        # Get section name
        sec_name = section.get_text().lower().replace(' ', '_')
        # Get section content
        sec_con = section.next_sibling

        get_user_favourites(sec_name, sec_con)

    # Get photos
    get_user_photos()

    # Store result data to file
    try:
        with open(result_dir / (username + "-fb-user.json"), "w+") as handle:
            json.dump(facebook_user_info, handle, indent=2)
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))

    # TODO: Remove this in final build
    # Print result data
    # print(json.dumps(facebook_user_info, indent=2))


# Gather Facebook Page info
def gather_page_info(username, home_soup, result_dir):
    # Dictionary to store result data
    facebook_page_info = {
        "about": {},
        "posts": {},
        "photos": {},
        "videos": {},
        "events": {},
        "community": {}
    }

    # Definition of all page functions start here

    # Get About info
    def get_page_about():
        # Fetch the About page
        about_page = req_session.get('https://en-gb.facebook.com/' + username + '/about',
                                     headers=headers,
                                     allow_redirects=False)
        # Create the BeautifulSoup object
        about_soup = bs4.BeautifulSoup(about_page.text, 'html.parser')

        # Check if About section is present
        if about_soup.select('._4-u2._3xaf._3-95._4-u8'):
            sections = about_soup.select('._4-u2._3xaf._3-95._4-u8')

            for section in sections:
                # Get the section name
                if section.find('div', class_='_50f7'):
                    sec = section.find('div', class_='_50f7').text
                elif section.find('div', class_='_50f4'):
                    sec = section.find('div', class_='_50f4').text
                else:
                    continue

                # Remove any spaces and lowercase everything
                sec = sec.lower().replace(' ', '_')
                facebook_page_info['about'][sec] = {}

                # Find all sub-sections
                subsec = section.find_all('div', class_='_5aj7 _3-8j')

                for i, item in enumerate(subsec):
                    facebook_page_info['about'][sec][i] = {}

                    # Get the link, if any
                    if item.findChildren('a'):
                        if len(item.findChildren('a')) == 1:
                            facebook_page_info['about'][sec][i]['link'] = item.findChild('a')['href']
                        elif len(item.findChildren('a')) > 1:
                            enum = enumerate([child['href'] for child in item.findChildren('a')])
                            facebook_page_info['about'][sec][i]['links'] = dict((x, y) for x, y in enum)

                    # Get the text/title of the sub-section
                    if item.select('._5aj7._3-8j ._4bl9 ._50f4'):
                        facebook_page_info['about'][sec][i]['text'] = item.select('._5aj7._3-8j ._4bl9 ._50f4')[0].text

                    # Get the description, if any
                    if item.findChild('div', class_='_3-8w') is not None:
                        facebook_page_info['about'][sec][i]['description'] = item.findChild('div', class_='_3-8w').text

        # If about section is not present
        else:
            facebook_page_info['about']['about'] = "Nothing in about section"

        # Check if page categories is present
        if about_soup.select('._4bl9._5m_o a'):
            # Get the page categories
            cat_section = about_soup.select('._4bl9._5m_o a')
            facebook_page_info['about']['categories'] = " . ".join(list(map(lambda cat: cat.text, cat_section)))
        # If no page categories are found
        else:
            facebook_page_info['about']['categories'] = "No categories to show"

        # Check if Story card section is present
        if about_soup.select('._4wye.rfloat._ohf'):
            sections = about_soup.select('._4wye.rfloat._ohf')

            for section in sections:
                if section.find('div', class_='_50f7') is not None:
                    # Get the section name
                    sec = section.find('div', class_='_50f7').text.lower().replace(' ', '_')

                    facebook_page_info['about'][sec] = {}

                    # Find all sub-sections
                    subsec = section.find_all('div', class_='_2pit _2pij')

                    for i, item in enumerate(subsec):
                        facebook_page_info['about'][sec][i] = {}

                        # Get the link, if any
                        if item.findChild('a') is not None:
                            facebook_page_info['about'][sec][i]['link'] = item.findChild('a')['href']

                        # Get the story title
                        if item.findChild('div', class_='_hil _50f5') is not None:
                            facebook_page_info['about'][sec][i]['title'] = item.findChild('div',
                                                                                          class_='_hil _50f5').text

                        # Get the story description
                        if item.select('._hik._2iem ._2vxa._3-95'):
                            spans = item.select('._hik._2iem ._2vxa._3-95')
                            span_content = " ".join([span.text for span in spans if span.text != " "])
                            facebook_page_info['about'][sec][i]['description'] = span_content

        # If story card section is not present
        else:
            facebook_page_info['about']['story'] = "N/A"

        # Check if Milestones section is present
        if about_soup.select('._4wye.rfloat._ohf ._1xnd'):
            sections = about_soup.select('._4wye.rfloat._ohf ._1xnd')

            for section in sections:
                if section.find('div', class_='_4bl9') is not None:
                    # Get the section name
                    sec = section.find('div', class_='_4bl9').text.lower().replace(' ', '_')

                    facebook_page_info['about'][sec] = {}

                    # Find all sub-sections
                    subsec = section.find_all('div', class_='clearfix _ikh _3-95')

                    for item in subsec:
                        if item.find('div', class_='_4bl7 _5zd') is not None:
                            # Get the year of milestone
                            year = item.find('div', class_='_4bl7 _5zd').text
                            facebook_page_info['about'][sec][year] = {}

                            # Get all the milestones in that year
                            year_subsec = item.find_all('li', class_='_2lch')

                            for i, y_item in enumerate(year_subsec):
                                if y_item.findChild('a') is not None:
                                    # Get the milestone text
                                    facebook_page_info['about'][sec][year][i] = y_item.find('a').text

        # If milestones section is not present
        else:
            facebook_page_info['about']['milestones'] = "N/A"

    # Get Posts
    def get_page_posts():
        json_posts = {}

        # Run facebook-scraper
        posts = get_posts(username, pages=3)

        for i, post in enumerate(posts):
            json_posts[i] = post
            # Convert date time object to string
            if json_posts[i]['time']:
                json_posts[i]['time'] = str(json_posts[i]['time'])

        # Store the posts data to JSON file
        try:
            with open(result_dir / (username + "-fb-page-posts.json"), 'w+', encoding='utf-8') as jsonf:
                jsonf.write(json.dumps(json_posts, indent=2, ))
        except Exception as e:
            print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))

    # Get Photos
    def get_page_photos():
        # Fetch the Photos page
        photos_page = req_html_session.get('https://en-gb.facebook.com/' + username + '/photos',
                                           headers=headers,
                                           allow_redirects=False)

        # Render the Javascript
        photos_page.html.render(sleep=2, timeout=30)

        # Create the BeautifulSoup object
        photos_soup = bs4.BeautifulSoup(photos_page.html.html, 'html.parser')

        # Get the Profile photo
        if photos_soup.find(id='u_0_d') is not None:
            if photos_soup.find(id='u_0_d').find('img') is not None:
                # Get profile photo URL
                facebook_page_info['about']['profile_photo'] = photos_soup.find(id='u_0_d').find('img').attrs['src']

        # Get the Cover photo
        if photos_soup.find(id='u_0_o') is not None:
            if photos_soup.find(id='u_0_o').find('img') is not None:
                # Get the cover photo URL
                facebook_page_info['about']['cover_photo'] = photos_soup.find(id='u_0_o').find('img').attrs['src']

        # Check if All Photos section is present
        if photos_soup.select('._2pie ._2pie ._2y_h._4-u2._4-u8'):
            all_photos = photos_soup.select('._2pie ._2pie ._2y_h._4-u2._4-u8')[0]

            # Check if there are any photos in All Photos section
            if all_photos.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['_2eea']) is not None:
                # Get each photo's section
                sections = all_photos.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['_2eea'])

                f10_photo_paths = []

                for section in sections:
                    # Get the webpage URLs for latest 10 photos
                    if len(f10_photo_paths) < 10:
                        if section.select_one('a') is not None:
                            # Get the webpage URL
                            photo_path = section.select_one('a')
                            f10_photo_paths.append(photo_path['href'])
                    else:
                        break

                for i, url in enumerate(f10_photo_paths):
                    # Fetch the webpage for each photo
                    photo_page = req_session.get(url, headers=headers, allow_redirects=False)
                    photo_soup = bs4.BeautifulSoup(photo_page.text, 'html.parser')

                    # Get the photo URL
                    link_tags = photo_soup.find_all('link', attrs={"as": "image"})
                    links = [link['href'] for link in link_tags]
                    image_url = max(set(links), key=links.count)

                    # Update photo info
                    facebook_page_info['photos'][i] = image_url

                    # Sleep for 1 second to avoid getting banned
                    time.sleep(round(uniform(1, 3), 1))

                    # Save the image files to a directory
                    try:
                        filename = image_url.split('/')[-1].split('?')[0]
                        photo = requests.get(image_url, stream=True)

                        with open(result_dir / filename, 'wb') as user_photo:
                            user_photo.write(photo.content)

                    except Exception as e:
                        print(Fore.RED + type(e).__name__ + Fore.RESET + ": " + str(e))

                    # Sleep for 1 second to avoid getting banned
                    time.sleep(round(uniform(1, 3), 1))

        # If no photos are found
        else:
            facebook_page_info['photos'] = "No photos to show"

    # Get Videos
    def get_page_videos():
        # Fetch the Videos page
        videos_page = req_html_session.get('https://en-gb.facebook.com/' + username + '/videos',
                                           headers=headers,
                                           allow_redirects=False)

        # Render the javascript
        videos_page.html.render(sleep=2, scrolldown=9, timeout=30)

        # Create the BeautifulSoup object
        videos_soup = bs4.BeautifulSoup(videos_page.html.html, 'html.parser')

        # Check if All Videos section is present
        if videos_soup.select('.tw6a2znq.gl4o1x5y.i1fnvgqd.lhclo0ds.j83agx80.ll8tlv6m'):
            all_videos = videos_soup.select('.tw6a2znq.gl4o1x5y.i1fnvgqd.lhclo0ds.j83agx80.ll8tlv6m')[0]

            # Check if there are any videos in All Videos section
            if all_videos.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['kfpcsd3p']):
                # Get each video's section
                sections = all_videos.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['kfpcsd3p'])

                f10_video_paths = []

                for section in sections:
                    # Get the webpage URLs for latest 10 videos
                    if len(f10_video_paths) < 10:
                        if section.select_one('span._3vwb._400z._2-40') is not None:
                            # Get the webpage URL
                            video_path = section.select_one('span._3vwb._400z._2-40')
                            f10_video_paths.append(video_path['href'])
                    else:
                        break

                for i, url in enumerate(f10_video_paths):
                    # Fetch the webpage for each video
                    video_page = req_session.get(url, headers=headers, allow_redirects=False)
                    video_soup = bs4.BeautifulSoup(video_page.text, 'html.parser')

                    # Get the video URL
                    video_tag = video_soup.find('meta', attrs={"property": "og:video:url"})
                    video_url = video_tag['content']

                    # Update video info
                    facebook_page_info['videos'][i] = video_url

                    # Sleep for 1 second to avoid getting banned
                    time.sleep(round(uniform(1, 3), 1))

        # If no videos are found
        else:
            facebook_page_info['videos'] = "No videos to show"

    # Get Events info
    def get_page_events():
        # Fetch the Events page
        events_page = req_html_session.get('https://en-gb.facebook.com/' + username + '/events',
                                           headers=headers,
                                           allow_redirects=False)

        # Render the javascript
        events_page.html.render(sleep=2, scrolldown=10, timeout=30)

        # Create the BeautifulSoup object
        events_soup = bs4.BeautifulSoup(events_page.html.html, 'html.parser')

        # Categories of events
        event_status = ['upcoming', 'past']

        if events_soup.select('._2pie ._4bl7._2u97._2q5c'):
            # Get all events
            all_events = events_soup.select('._2pie ._4bl7._2u97._2q5c')[0]

            for status in event_status:
                # Set the element IDs for respective category of events
                if status == 'upcoming':
                    n_tag_id = '#no_upcoming_events_card'
                    y_tag_id = '#upcoming_events_card'
                else:
                    n_tag_id = '#no_past_events_card'
                    y_tag_id = '#past_events_card'

                # Check for no upcoming or past events
                if all_events.select(f'{n_tag_id} ._2pi1._52jv'):
                    facebook_page_info['events'][status] = "No " + status + " events"

                # Check for upcoming or past events
                elif all_events.select(f'{y_tag_id} ._24er'):
                    # Get all events of a particular category
                    events = all_events.select(f'{y_tag_id} ._24er')

                    facebook_page_info['events'][status] = {}

                    for i, event in enumerate(events):
                        # Get the latest 10 events in respective category
                        if len(facebook_page_info['events'][status]) < 10:
                            facebook_page_info['events'][status][i] = {}

                            # Get the event date
                            if event.select('span._5x8v._5a5j._5a5i span'):
                                date_tag = event.select('span._5x8v._5a5j._5a5i span')
                                facebook_page_info['events'][status][i]['date'] = " ".join(
                                    [x.text.strip() for x in date_tag])

                            # Get the event title
                            if event.select('td._4dmi._51m- span._50f7'):
                                facebook_page_info['events'][status][i]['title'] = event.select(
                                    'td._4dmi._51m- span._50f7')[0].text.strip()

                            # Get the event day, time and no. of guests
                            if event.select('td._4dmi._51m- div._4dml.fsm.fwn.fcg'):
                                day_time_guests = event.select('td._4dmi._51m- div._4dml.fsm.fwn.fcg')[0].get_text()
                                if " · " in day_time_guests:
                                    facebook_page_info['events'][status][i]['day_time'] = day_time_guests.split(
                                        " · ")[0].strip()
                                    facebook_page_info['events'][status][i]['guests'] = day_time_guests.split(
                                        " · ")[1].strip()
                                else:
                                    facebook_page_info['events'][status][i]['day_time_guests'] = day_time_guests

                            # Check if event has any place or location
                            if event.select('td._5pxd._51m- div._4dmn'):
                                place_loc = event.select('td._5pxd._51m- div._4dmn')[0]

                                # Get the event place
                                if place_loc.find('a') is not None:
                                    facebook_page_info['events'][status][i]['place'] = place_loc.find('a').text

                                elif place_loc.find(class_='_30n-') is not None:
                                    facebook_page_info['events'][status][i]['place'] = place_loc.find(
                                        class_='_30n-').text

                                # Get the event location
                                if place_loc.find(class_='_30n_') is not None:
                                    facebook_page_info['events'][status][i]['location'] = place_loc.find(
                                        class_='_30n_').text

                        else:
                            break

        # If no events are found
        else:
            facebook_page_info['events'] = "No events to show"

    # Get Home and Community info
    def get_page_home_community():
        # Check if Community section is present
        if home_soup.find(class_='_4-u2 _6590 _3xaf _4-u8') is not None:
            community_div = home_soup.find(class_='_4-u2 _6590 _3xaf _4-u8')
            items = community_div.select('._2pi9._2pi2')

            # Get the likes, followers and check-ins
            for item in items:
                if 'like' in item.text:
                    facebook_page_info['community']['like'] = item.text
                elif 'follow' in item.text:
                    facebook_page_info['community']['follow'] = item.text
                elif 'check-in' in item.text:
                    facebook_page_info['community']['check-ins'] = item.text

        # If community section is not found
        else:
            facebook_page_info['community']['no_info'] = "No info about likes, followers or check-ins"

        # Check if "Pages liked by page" section is present
        if home_soup.find('div', id=re.compile('^PagePagesLikedByPageSecondaryPagelet')).find(
                class_='_5ay5') is not None:
            pages_liked = home_soup.find('div', id=re.compile('^PagePagesLikedByPageSecondaryPagelet')).find(
                class_='_5ay5')
            # Get the top 10 pages from the list
            items = pages_liked.find_all(class_='_4-lt', limit=10)

            facebook_page_info['community']['pages_liked'] = {}

            for i, item in enumerate(items):
                facebook_page_info['community']['pages_liked'][i] = {}
                # Get the page name and link
                if item.find('a', class_='_4-lu ellipsis') is not None:
                    facebook_page_info['community']['pages_liked'][i]['link'] = item.find(
                        'a', class_='_4-lu ellipsis').attrs['href']
                    facebook_page_info['community']['pages_liked'][i]['name'] = item.find(
                        'a', class_='_4-lu ellipsis').text

        # If "Pages liked by page" section is not present
        else:
            facebook_page_info['community']['pages_liked'] = "No info about liked pages"

    # Execute all functions
    get_page_about()

    # Sleep for 5 seconds to avoid getting banned
    time.sleep(round(uniform(5, 7), 1))

    get_page_posts()

    time.sleep(round(uniform(5, 7), 1))

    get_page_photos()

    time.sleep(round(uniform(5, 7), 1))

    get_page_videos()

    time.sleep(round(uniform(5, 7), 1))

    get_page_events()

    time.sleep(round(uniform(5, 7), 1))

    get_page_home_community()

    # pprint(facebook_page_info)

    # Store result data to file
    try:
        with open(result_dir / (username + '-fb-page.json'), 'w+') as handle:
            json.dump(facebook_page_info, handle, indent=2)
    except Exception as err:
        print(Fore.RED + type(err).__name__ + Fore.RESET + ": " + str(err))


# Gather info about username
def gather_info(username):

    print('Fetching Facebook Data...\n')

    # Fetch the home page
    home_page = req_session.get('https://www.facebook.com/' + username, headers=headers)
    # Create the BeautifulSoup object
    home_soup = bs4.BeautifulSoup(home_page.text, 'html.parser')

    # Check if it is a FB profile or FB page
    if home_soup.find('meta', property='al:android:url') is not None:
        # Target directory
        result_dir = CWD / "scripts" / "results" / username / "facebook"

        # If its a FB profile
        if 'fb://profile/' in home_soup.find('meta', property='al:android:url')['content']:
            gather_user_info(username, home_soup, result_dir)

        # If its a FB page
        elif 'fb://page/' in home_soup.find('meta', property='al:android:url')['content']:
            gather_page_info(username, home_soup, result_dir)

        # If its not a FB profile or page
        else:
            print("\nThis doesn't seem to be a facebook profile or page. Please try again.\n")

    else:
        print('\nThere is no facebook profile or page by this name. Please try again.\n')

    print('Facebook data fetched\n')
