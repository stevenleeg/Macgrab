#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, ConfigParser, json, base64, urllib, urllib2, logging
screenshotsOnDesktop = set()
from AppKit import NSSpeechSynthesizer

# keep track of existing screen shots
screenshotsOnDesktop = set()

# for debugging
noUpload = False

def getConfig():
	# Find the config directory and create it if it doesn't already exist
	config_path = os.path.join(os.path.expanduser("~"), ".macgrab")

	if os.path.exists(config_path) is False:
		os.mkdir(config_path)
	
	# Next, the config file
	config = ConfigParser.RawConfigParser()
	
	if os.path.exists(os.path.join(config_path, "macgrab.conf")):
		config.read(os.path.join(config_path, "macgrab.conf"))

	# No config file? No problem!
	else:
		config.add_section("general")
		config.set("general", "watch_path", os.path.join(os.path.expanduser("~"), "Desktop"))
		config.set("general", "sound", '/System/Library/Sounds/Purr.aiff')
		config.set("general", "post_delete", 'false')
		
		# Write the newly generated config file
		with open(os.path.join(config_path, "macgrab.conf"), 'wb') as file:
			config.write(file)
	
	return config

#TODO: Use imgur's authentication UI instead of anonymous
def upload(path):
	if(noUpload):
		return (True, {'original_image': 'http://test'})
	
	data = {
        'key': 'bbc8f922180d480cdf32bce06e47eefa',
        'image': base64.b64encode(open(path).read()),
    }

	data = urllib.urlencode(data)
	req = urllib2.urlopen("http://imgur.com/api/upload.json", data=data)
	response = json.loads(req.read())

	if req.code == 200:
		return (True, response["rsp"]["image"])
	return (False, response["rsp"]["error_msg"])

def addUploaded(filename):
	""" Writes the filename to the database so we know not to upload it again"""
	screenshotsOnDesktop.add(filename)

def isUploaded(filename):
	""" Reads the database file and tells us if filename has already been uploaded or not """
	return filename in screenshotsOnDesktop

def say(txt):
	voice = NSSpeechSynthesizer.defaultVoice()
	speech = NSSpeechSynthesizer.alloc().initWithVoice_(voice)
	speech.startSpeakingString_(txt)

# Run tests
if __name__ == "__main__":
	config = getConfig()
	print "Watch path is: %s" % config.get("general", "watch_path")
