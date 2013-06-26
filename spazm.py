#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from livestreamer import Livestreamer
import twitchingpython
import subprocess
from subprocess import check_call, Popen, PIPE
import os
import re
from screen import *

class Spazm(Screen):
	ACCESS_TOKEN = None
	twitch = None
	
	def __init__(self, token = None):
		super(Spazm, self).__init__()
		
		if not token:
			self.ACCESS_TOKEN = twitchingpython.gettoken()
		else:
			self.ACCESS_TOKEN = token
		self.twitch = twitchingpython.TwitchingWrapper(self.ACCESS_TOKEN)

	
	def run(self, cmd):
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=PIPE, stderr=PIPE)
		return process
		
	def get_streams_followed(self):
		streams = []
		streams_followed = self.twitch.getstreamsfollowing()["streams"]
		for i, channel_data in enumerate(streams_followed):
			channel = channel_data['channel']
			
			stream = {}
			stream['streamer'] = self.to_str(channel['display_name'])
			stream['status'] = self.to_str(channel['status'])
			stream['game'] = self.to_str(channel['game'])
			stream['url'] = self.to_str(channel['url'])

			streams.append(stream)

		return streams
		
	def get_stream_qualities(self, url):
		'''
		#doesn't return all qualities
		livestreamer = Livestreamer()
		plugin = livestreamer.resolve_url(url)

		qualities = plugin.get_streams().keys()
		'''
		#qualities, stderr = Popen("livestreamer %s" % url, stdout=PIPE, stderr=PIPE).communicate()
		qualities_data, stderr = self.run("livestreamer %s" % url).communicate()
		found_qualities = re.search("Found streams: (.*)", qualities_data)
		if found_qualities:
			qualities = found_qualities.group(1).replace("\n", '').replace("(worst)","").replace("(best)",'').replace("(worst, best)", '')
			qualities = [x.strip() for x in qualities.split(',')]
		return qualities

	def start_video(self, url, quality = "worst"):
		vid_status = None
		vid = self.run("livestreamer %s %s" % (url, quality)) #does not wait to complete
		
	def display_streams_followed(self):
	
		streams = self.get_streams_followed()
		while True:
			self.reset()
			#Display streams followed that are live
			self.add("=== Streams Followed ===") 
			self.add()
			self.add("`) Refresh")
			self.add()
			
			for i, stream in enumerate(streams):
				self.add("%s) %s [%s]" % (i + 1, stream['streamer'], stream['game']))
				self.add(stream['status'])
				self.add()
				
			self.display()
			input = self.get_input()
			
			if input == '`':
				self.screen.addstr(1, 66, "[REFRESHING]")
				self.screen.refresh()
				streams = self.get_streams_followed()
			elif input.isdigit():
				self.reset()
				self.add("=== Qualities ===")
				self.add()
				self.add("`) Back")
				self.add()
				
				self.screen.addstr(1, 69, "[LOADING]")
				self.screen.refresh()
				
				url = streams[int(input) - 1]['url'] #Display qualities for the stream chosen
				qualities = self.get_stream_qualities(url)
				for i, quality in enumerate(qualities):
					self.add("%s) %s" % (i, quality))
				
				self.display()
				input = self.get_input()
				if input != '`' and input.isdigit():
					self.screen.addstr(1, 68, "[STARTING]")	
					self.screen.refresh()
					self.start_video(url, qualities[int(input)]) #Start VLC and connect to stream
	
if __name__ == '__main__':
	s = Spazm()

	while True:
		'''
		screen.clear()
		screen.border(0)
		
		print "=== Options ==="
		options = ["Streams Following"]
		
		for i, option in enumerate(options):
			print "%s) %s" % (i, option)
			
		print "Choose: ",
		input = raw_input()
		'''
		input = '0'
		if input == '0':
			s.display_streams_followed()
