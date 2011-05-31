#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, time, re, logging
import macgrab
from AppKit import NSPasteboard, NSSound

# Get the config file
config = macgrab.getConfig()
watch_path = config.get("general","watch_path")

# Compile the regex used to identify screenshots
screenshot_regex = re.compile("Screen shot ([0-9]{4})-([0-9]{2})-([0-9]{2}) at (1?[0-9]).([0-9]{2}).([0-9]{2}) ([A|PM]{2}).png")	

# Setup the NSSound object for the "Success" notification
#TODO: Add a config option for the sound
notif = NSSound.alloc()
notif.initWithContentsOfFile_byReference_('/System/Library/Sounds/Purr.aiff', True)

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
		
		for screenshot in screenshots:
			# Make sure we haven't already uploaded it
			if macgrab.uploaded(screenshot):
				continue
			# Attempt to upload the image
			status, resp = macgrab.upload(os.path.join(watch_path, screenshot))

			# If it worked, tell us the URL, else tell us what went wrong.
			if status != True:
				print "There was an error while trying to upload the screenshot: %s" % resp
				continue
			
			print "Screenshot uploaded successfully! URL is %s" % resp['original_image']
			# Now copy the URL to the clipboard
			pb = NSPasteboard.generalPasteboard()
			pb.clearContents()
			pb.writeObjects_([resp['original_image']])

			# Add the screenshot to the list of already uploaded shots
			macgrab.write(screenshot)

			# Play a sound for confirmation
			# TODO: If growl's python APIs weren't terrible there would be a visual notification here
			notif.stop()
			notif.play()
	
	# Sleep for a bit, since we don't need to be doing this all the time.
	time.sleep(1)
