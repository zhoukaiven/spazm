#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from livestreamer import Livestreamer
import twitchingpython
import subprocess
from subprocess import check_call, Popen, PIPE
import os
import curses
import re
from textwrap import wrap

class Spazm():
	ACCESS_TOKEN = None
	twitch = None
	BASE_URL = None
	output = []
	
	def __init__(self,token=None):
		if not token:
			self.ACCESS_TOKEN = twitchingpython.gettoken()
		else:
			self.ACCESS_TOKEN = token
		self.twitch = twitchingpython.TwitchingWrapper(self.ACCESS_TOKEN)
	
	def to_str(self, obj):
		try:
			return str(obj)
		except UnicodeEncodeError:
			return unicode(obj).encode('unicode_escape')
	
	def run(self, cmd):
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=PIPE, stderr=PIPE)
		return process
	
	def display(self, screen, all_text):
		screen.clear()
		screen.border(0)
		line = 1
		for text_block in all_text:	
			if text_block == "\n":
				line +=1
			else:
				for text in wrap(text_block,78):
					try:
						screen.addstr(line, 1, text)
					except: pass
					line += 1
		screen.refresh()
		
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
		
	def watch_streams_followed(self, screen):
		screen.clear()
		screen.border(0)
		
		streams = self.get_streams_followed()
		while True:
			output = []
			#Display streams followed that are live
			output.append("=== Streams Followed ===") 
			output.append("\n")
			output.append("`) Refresh")
			output.append("\n")
			
			for i, stream in enumerate(streams):
				output.append("%s) %s [%s]" % (i + 1, stream['streamer'], stream['game']))
				output.append(stream['status'])
				output.append("\n")
				
			self.display(screen, output)
			input = unichr(screen.getch())
			
			if input == '`':
				screen.addstr(1, 66, "[REFRESHING]")
				screen.refresh()
				streams = self.get_streams_followed()
			else:
				output = ["=== Qualities ===", "\n", "`) Back", "\n"]
				
				screen.addstr(1, 69, "[LOADING]")
				screen.refresh()
				
				url = streams[int(input) - 1]['url'] #Display qualities for the stream chosen
				qualities = self.get_stream_qualities(url)
				for i, quality in enumerate(qualities):
					output.append("%s) %s" % (i, quality))
				
				self.display(screen, output)
				input = unichr(screen.getch())
				if input != '`':
					screen.addstr(1, 68, "[STARTING]")	
					screen.refresh()
					self.start_video(url, qualities[int(input)]) #Start VLC and connect to stream
				
if __name__ == '__main__':
	s = Spazm()
	screen = curses.initscr()
	curses.noecho()
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
			s.watch_streams_followed(screen)
