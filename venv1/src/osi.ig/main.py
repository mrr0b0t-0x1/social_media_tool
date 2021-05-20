#!/bin/env python3

import os
import sys
import platform
sys.path.append(os.getcwd()+"/.lib/")
import argparse
from api import *
import time

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", required=True, help="username of account to scan")
ap.add_argument("-p", "--post", action="store_true", help="image info of user uploads")
ap.add_argument("-o", "--output", required=True, help="output results to file")
args = vars(ap.parse_args())
	
try:
	if args['user']:
		user_info(usrname=args["user"], out=args["output"])
		time.sleep(2)

	if args['post']:
		post_info()

except Exception as err:
	print(err)
