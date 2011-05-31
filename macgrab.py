#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, ConfigParser, pycurl, json

class ResponseHandler:
	""" Used to handle responses from the imgur api"""
	def __init__(self):
		self.contents = ''
	
	def write(self, buff):
		self.contents += buff
	
	def parse(self):
		#TODO: Be ready for a non-json response and react appropriately
		return json.loads(self.contents)

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
		
		# Write the newly generated config file
		with open(os.path.join(config_path, "macgrab.conf"), 'wb') as file:
			config.write(file)

		# Make an uploaded.db file
		with open(os.path.join(config_path, "uploaded.db"), 'w') as file:
			file.write('# This file stores the filenames of screenshots already uploaded\n')
			file.close()
	
	return config

#TODO: Use imgur's authentication UI instead of anonymous
def upload(path):
	send = pycurl.Curl()

	# Setup the post values to send to imgur
	values = [
		('key', 'bbc8f922180d480cdf32bce06e47eefa'),
		('image', (send.FORM_FILE, path))
	]
	
	# Initiate a ResponseHandler object to capture imgur's response
	handler = ResponseHandler()

	# Set the options and send imgur a picture
	send.setopt(send.URL, "http://imgur.com/api/upload.json")
	send.setopt(send.HTTPPOST, values)
	send.setopt(send.WRITEFUNCTION, handler.write)
	send.perform()
	
	# React to the response
	resp = handler.parse()['rsp']
	if resp['stat'] == 'ok':
		return (True, resp['image'])
	else:
		return (False, resp['error_msg'])

def write(filename):
	""" Writes the filename to the database so we know not to upload it again"""
	f = open(os.path.join(os.path.expanduser('~'), '.macgrab/uploaded.db'), 'a')
	f.write(filename + "\n")
	f.close()

def uploaded(filename):
	""" Reads the database file and tells us if filename has already been uploaded or not """
	f = open(os.path.join(os.path.expanduser('~'), '.macgrab/uploaded.db'), 'r')
	for line in f.readlines():
		if filename == line.replace('\n', ''):
			return True
	f.close()
	# We never detected it, so return false
	return False

# Run tests
if __name__ == "__main__":
	config = getConfig()
	print "Watch path is: %s" % config.get("general", "watch_path")
