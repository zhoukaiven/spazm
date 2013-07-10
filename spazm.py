#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from livestreamer import Livestreamer
import twitchingpython

from screen import *
from stream import *

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
		
		self.streams = []
	
	def get_streams_followed(self):
		streams_followed = self.twitch.getstreamsfollowing()["streams"]
		for channel_data in streams_followed:
			url = channel_data['channel']['url']
			if not any(stream.get_url() == url for stream in self.streams):
				self.streams.append(Stream(channel_data))
		
	def display_streams_followed(self):
	
		self.get_streams_followed()
		while True:
			self.reset()
			#Display streams followed that are live
			self.add(["=== Streams Followed ===", "\n", "`) Refresh", "\n"] ) 

			#try:
			for i, stream in enumerate(self.streams):
				stream_buffer = stream.load_stream_buffer()
				stream_buffer[0] = "%s) %s" % (hex(i + 1)[2:], stream_buffer[0]) #add index to the stream_buffer
				self.add(stream_buffer) #change add to take a list
				self.add()
			#except:
			#	pass
			self.display()
			input = self.get_input()
			
			if input == '`':
				self.screen.addstr(1, 66, "[REFRESHING]")
				self.screen.refresh()
				streams = self.get_streams_followed()
			else:
				self.reset()
				self.add(["=== Qualities ===", "\n", "`) Back", "\n"])
				
				self.screen.addstr(1, 69, "[LOADING]")
				self.screen.refresh()
				
				#try:
				'''#print out the qualities
				url = self.streams[int(input, 16) - 1]['url'] #Display qualities for the stream chosen
				
				qualities = self.get_stream_qualities(url)
				for i, quality in enumerate(qualities):
					self.add("%s) %s" % (i + 1, quality))
				'''
				stream = self.streams[int(input, 16) - 1]
				self.add(stream.load_qualities_buffer())					
				self.display()
				
				input = self.get_input()
				if input != '`' and input.isdigit():
					self.screen.addstr(1, 68, "[STARTING]")	
					self.screen.refresh()
					
					#self.start_video(url, qualities[int(input) - 1]) #Start VLC and connect to stream
					stream.watch(int(input) - 1)
							
				#except:
				#	pass
	
if __name__ == '__main__':
	s = Spazm()

	while True:
		input = '0'
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
		if input == '0':
			s.display_streams_followed()
