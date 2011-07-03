
#!/usr/bin/env python

#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, time, re, logging
import macgrab
from ConfigParser import NoOptionError
from AppKit import NSPasteboard
from datetime import datetime
from PyObjCTools import AppHelper
from FSEvents import *

# Globals vars
# Load the configuration
CONFIG = macgrab.getConfig()

# watch folder path - desktop by default
WATCH_PATH = CONFIG.get("general", "watch_path")
	
# Compile the regex used to identify screenshots
MAC_SCREENSHOT_REGEX = re.compile("Screen shot ([0-9]{4})-([0-9]{2})-([0-9]{2}) at (1?[0-9]).([0-9]{2}).([0-9]{2}) ([A|PM]{2}).png")	

# timer fires every x of these intervals to check for keyboard interrupt (ie control-c)
INTERVAL_TO_CHECK_FOR_PROGRAM_EXIT = 5.0

# main function
def main():
	
	# Pre-populate skip set with all existing screen shots
	firstLoadFileList = os.listdir(WATCH_PATH)
	for filename in firstLoadFileList:
		if MAC_SCREENSHOT_REGEX.match(filename):
			macgrab.addUploaded(filename)
			
	# Listen for filesystem events at the watch_path
	addFSEventListener()
	
	# Keep alive
	CFRunLoopAddTimer(NSRunLoop.currentRunLoop().getCFRunLoop(), 
					CFRunLoopTimerCreate(None, CFAbsoluteTimeGetCurrent(), INTERVAL_TO_CHECK_FOR_PROGRAM_EXIT, 0, 0, onTimerCallback, None), 
					kCFRunLoopCommonModes)

	# respond to control-c to terminate
	try:
		AppHelper.runConsoleEventLoop(installInterrupt=True)
	except KeyboardInterrupt:
		print "exiting"

# action to take if the filesystem is updated at the WATCH_PATH 
# will be called multiple times per new screen shot
def uploadNewScreenshots():
	# Get a list of filenames in the watch directory
	files = os.listdir(WATCH_PATH)
	
	lastUploadedFile = None
	screenshots = []
	
	# See if there are any screenshots to upload
	# Make sure we haven't already uploaded it
	for filename in files:
		if MAC_SCREENSHOT_REGEX.match(filename) and not macgrab.isUploaded(filename):
			screenshots.append(filename)
		
		# Proceed if there was a new screen shot
		if len(screenshots) > 0:
			logging.info("Found screenshots to upload: %s" % screenshots)
			
			for screenshot in screenshots:
			
				# Attempt to upload the image
				status, resp = macgrab.upload(os.path.join(WATCH_PATH, screenshot))
	
				# If it worked, tell us the URL, else tell us what went wrong.
				if status != True:
					print "There was an error while trying to upload the screenshot: %s" % resp
					continue
	
				# print to std out for simple copy/paste
				print "Screenshot uploaded successfully! URL is %s" % resp['original_image']
	
				# returns url
				lastUploadedFile = [resp['original_image']]
	
				# Add the screenshot to the list of already uploaded shots
				macgrab.addUploaded(screenshot)
	
				# If we're told to, delete the screenshot afterwards
				try:
					delshot = CONFIG.getboolean('general', 'post_delete')
				except NoOptionError:
					delshot = False
				
				if delshot:
					os.remove(os.path.join(WATCH_PATH, screenshot))
	
			# Steps to take after a file has been uploaded
			if lastUploadedFile != None:
				
				# verbose notification
				macgrab.say("uploaded screen shot")
			
				# Now copy the URL to the clipboard
				pb = NSPasteboard.generalPasteboard()
				pb.clearContents()
				pb.writeObjects_(lastUploadedFile)
				
				# clear last uploaded file var
				lastUploadedFile = None;


def addFSEventListener():

	# Executing lifecycle defined in FSEvents.h
	# 1. FSEventStreamCreate
	stream = FSEventStreamCreate(kCFAllocatorDefault, onFSEvent, None, [WATCH_PATH], kFSEventStreamEventIdSinceNow, 1.0, 0)

	if not stream:
		raise RuntimeError("FSEventStreamCreate failed")

	# 2. FSEventStreamScheduleWithRunLoop
	FSEventStreamScheduleWithRunLoop(stream, NSRunLoop.currentRunLoop().getCFRunLoop(), kCFRunLoopDefaultMode)

	# 3. FSEventStreamStart
	if not FSEventStreamStart(stream):
		raise RuntimeError("FSEventStreamStart failed")

	# FSEventStreamRelease 
	print "FSEventStream started for path: %s" % WATCH_PATH


def onFSEvent(stream, full_path, event_count, paths, masks, ids):
	if(len(paths) > 0):
		logging.info("onFSEvent at %s" % paths[0]);
		uploadNewScreenshots()
		
		
def onTimerCallback(timer, stream):
	pass # noop
	
if __name__ == "__main__":
	main()
