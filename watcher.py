#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, time, re

while 1:
	# Get the path to their desktop and list it
	path = os.path.join(os.path.expanduser("~"), "Desktop")
	watch_dir = os.listdir(path)

	# See if there are any screenshots to upload
	for filename in watch_dir:
		regex = re.compile("Screen shot ([0-9]{4})-([0-9]{2})-([0-9]{2}) at (1?[0-9]).([0-9]{2}).([0-9]{2}) ([A|PM]{2}).png")	
