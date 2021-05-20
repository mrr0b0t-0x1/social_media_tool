#!/bin/env python3

import requests
import random
import json
import sys
import os
from local import *

username = None
resp_js = None
is_private = False
total_uploads = 10
out_dir = None

def proxy_session():
	session = requests.session()
	session.proxies = {
		'http':  'socks5://127.0.0.1:9050',
		'https': 'socks5://127.0.0.1:9050'
	}
	return session

def get_page(usrname):
	global resp_js, username
	username = usrname
	session = requests.session()
	session.headers = {'User-Agent': random.choice(useragent)}
	resp_js = session.get('https://www.instagram.com/'+usrname+'/?__a=1').text
	return resp_js

def exinfo():

	def xprint(xdict, text):
		if xdict != {}:
			print(f"{su} {re}most used %s :" % text)
			i = 0
			for key, val in xdict.items():
				if len(mail) == 1:
					if key in mail[0]:
						continue
				print(f"  {gr}%s : {wh}%s" % (key, val))
				i += 1
				if i > 4:
					break
			print()
		else:
			pass
	
	raw = find(resp_js)

	mail = raw['email']
	tags = sort_list(raw['tags'])
	ment = sort_list(raw['mention'])

	# if mail != []:
	# 	if len(mail) == 1:
	# 		print(f"{su} {re}email found : \n{gr}  %s" % mail[0])
	# 		print()
	# 	else:
	# 		print(f"{su} {re}email found : \n{gr}  ")
	# 		for x in range(len(mail)):
	# 			print(mail[x])
	# 		print()
	#
	# xprint(tags, "tags")
	# xprint(ment, "mentions")

	return [mail, tags, ment]
	
def user_info(usrname, out):

	global total_uploads, is_private, out_dir

	out_dir = out
	
	resp_js = get_page(usrname)
	js = json.loads(resp_js)
	js = js['graphql']['user']
	
	if js['is_private'] != False:
		is_private = True
	
	if js['edge_owner_to_timeline_media']['count'] > 10:
		pass
	else:
		total_uploads = js['edge_owner_to_timeline_media']['count']

	usrinfo = {
		'username': js['username'],
		'user id': js['id'],
		'name': js['full_name'],
		'followers': js['edge_followed_by']['count'],
		'following': js['edge_follow']['count'],
		'posts img': js['edge_owner_to_timeline_media']['count'],
		'posts vid': js['edge_felix_video_timeline']['count'],
		'reels': js['highlight_reel_count'],
		'bio': js['biography'].replace('\n', ', '),
		'external url': js['external_url'],
		'private': js['is_private'],
		'verified': js['is_verified'],
		'profile img': urlshortner(js['profile_pic_url_hd']),
		'business account': js['is_business_account'],
		#'connected to fb': js['connected_fb_page'],  -- requires login
		'joined recently': js['is_joined_recently'],
		'business category': js['business_category_name'],
		'category': js['category_enum'],
		'has guides': js['has_guides'],
	}

	exinf = exinfo()

	usrinfo['email'] = exinf[0]
	usrinfo['most used tags'] = exinf[1]
	usrinfo['most used mentions'] = exinf[2]

	# Write output to file
	with open(os.path.join(out_dir, username + "-about-insta.json"), "w", encoding="utf-8") as f:
		json.dump(usrinfo, f, indent=2)
		print("Saved user info")


def highlight_post_info(i):

	postinfo = {}
	total_child = 0
	child_img_list = []

	x = json.loads(resp_js)
	js = x['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']

	# this info will be same on evry post
	info = {
		'comments': js['edge_media_to_comment']['count'],
		'comment disable': js['comments_disabled'],
		'timestamp': js['taken_at_timestamp'],
		'likes': js['edge_liked_by']['count'],
		'location': js['location'],
	}

	# if image dosen't have caption this key dosen't exist instead of null
	try:
		info['caption'] = js['edge_media_to_caption']['edges'][0]['node']['text']
	except IndexError:
		pass

	# if uploder has multiple images / vid in single post get info how much edges are
	if 'edge_sidecar_to_children' in js:
		total_child = len(js['edge_sidecar_to_children']['edges'])

		for child in range(total_child):
			js = x['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_sidecar_to_children']['edges'][child]['node']
			img_info = {
				'typename': js['__typename'],
				'id': js['id'],
				'shortcode': js['shortcode'],
				'dimensions': str(js['dimensions']['height'] + js['dimensions']['width']),
				'image url' : js['display_url'],
				'fact check overall': js['fact_check_overall_rating'],
				'fact check': js['fact_check_information'],
				'gating info': js['gating_info'],
				'media overlay info': js['media_overlay_info'],
				'is_video': js['is_video'],
				'accessibility': js['accessibility_caption']
			}

			child_img_list.append(img_info)

		postinfo['imgs'] = child_img_list
		postinfo['info'] = info

	else:
		info = {
			'comments': js['edge_media_to_comment']['count'],
			'comment disable': js['comments_disabled'],
			'timestamp': js['taken_at_timestamp'],
			'likes': js['edge_liked_by']['count'],
			'location': js['location'],
		}

		try:
			info['caption'] = js['edge_media_to_caption']['edges'][0]['node']['text']
		except IndexError:
			pass

		img_info = {
				'typename': js['__typename'],
				'id': js['id'],
				'shortcode': js['shortcode'],
				'dimensions': str(js['dimensions']['height'] + js['dimensions']['width']),
				'image url' : js['display_url'],
				'fact check overall': js['fact_check_overall_rating'],
				'fact check': js['fact_check_information'],
				'gating info': js['gating_info'],
				'media overlay info': js['media_overlay_info'],
				'is_video': js['is_video'],
				'accessibility': js['accessibility_caption']
			}
		
		child_img_list.append(img_info)
		
		postinfo['imgs'] = child_img_list
		postinfo['info'] = info

	return postinfo


def post_info():
	
	if is_private != False:
		print(f"{fa} {gr}cannot use -p for private accounts !\n")
	
	else:
		posts_json = {}
		
		for x in range(total_uploads):
			posts_json[x] = highlight_post_info(x)

		# Write output to file
		with open(os.path.join(out_dir, username + "-posts-insta.json"), "w", encoding="utf-8") as f:
			json.dump(posts_json, f, indent=2)
			print("Saved posts info")
