#
# Macgrab - A simple TinyGrab alternative
# Written by Steve Gattuso
# http://www.stevegattuso.me // @vestonian
# Distributed under the MIT license
#
import os, ConfigParser

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
	
	return config

# Run tests
if __name__ == "__main__":
	config = getConfig()
	print "Watch path is: %s" % config.get("general", "watch_path")
