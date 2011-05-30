#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, time, re, logging
import macgrab

# Get the config file
config = macgrab.getConfig()
watch_path = config.get("general","watch_path")

# Compile the regex used to identify screenshots
screenshot_regex = re.compile("Screen shot ([0-9]{4})-([0-9]{2})-([0-9]{2}) at (1?[0-9]).([0-9]{2}).([0-9]{2}) ([A|PM]{2}).png")	

while 1:
	# Get a list of filenames in the watch directory
	files = os.listdir(watch_path)

	screenshots = []
	# See if there are any screenshots to upload
	for filename in files:
		if screenshot_regex.match(filename):
			screenshots.append(filename)
			
	if len(screenshots) > 0:
		logging.info("Found screenshots to upload: %s" % screenshots)
	
	# Sleep for a bit, since we don't need to be doing this all the time.
	time.sleep(1)
