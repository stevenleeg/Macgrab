# Welcome to Macgrab
Macgrab is a simple alternative to screenshot uploading software such as GrabUp (now dead) and [TinyGrab](http://tinygrab.com). Although it'spurpose is more for education rather than improving on it's competitors, it is still a perfectly suitable alternative.

## Why make something that's already been done?
Well why not? I love programming and especially in Python! Most of my inspiration for making this project in particular was my dissaproval ofTinyGrab's latest release: 2.0. For some reason, they decided it would be best to use links to a webpage rather than the original image, which was a minor inconvenience to me as I like to embed screenshots directly into emails. Since I had some free time, I figured it'd be fun to write a small alternative to TinyGrab in python and learn a thing or two about pyobjc and the imgur API.

## Using macgrab
Before starting, make sure you're on a mac and have installed the pycurl library. In most cases, this is as easy as running `easy_install pycurl`.

Now that we have that out of the way, go ahead and download the latest revision of Macgrab from the github repository. You can do this by running the following command in the directory you'd like to store the application:

    git clone git://github.com/stevenleeg/Macgrab.git

Once you have the files, just run `python watcher.py` and you're good to go, To test it out, just take a screenshot and you should then hear a audible notification once it's done uploading. Open up your browser and paste your clipboard into the address bar and you should see your screenshot!

If you want to run Macgrab without having to leave a terminal window open, just run `python watcher.py &`. This will spawn a new process in the background, allowing you to exit out of the terminal while still being able to have your screenshots uploaded.

## Configuring macgrab
After running macgrab for the first time, a new directory in your home folder called .macgrab is created. In this directory is the defaul configuration file, macgrab.conf, which you can edit to your liking. Here are the options:

* `watch_path`: The directory macgrab will watch for new screenshots. Defaults to ~/Desktop
* `sound`: The path to a sound file which is played after every upload. Defaults to /System/Library/Sounds/Purr.aiff
* `post_delete`: If set to true, macgrab will delete screenshots after a successful upload. Defaults to false.

## Licensing
Because this project was created for the purpose of education, I encourage anybody to take my work and learn from it by doing whatever you'd like with it! For this reason, this project is licensed under the [MIT License](http://www.opensource.org/licenses/mit-license.php)
