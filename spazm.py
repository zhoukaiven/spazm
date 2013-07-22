#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
		
		self.streams = {}
	
	def get_streams_followed(self):
		stream_data = self.twitch.getstreamsfollowing()["streams"]
		live_urls = [channel_data['channel']['url'] for channel_data in stream_data]
		
		cached_live_urls  = set(live_urls) & set(self.streams.keys())
		dead_urls = set(self.streams.keys()) - set(cached_live_urls)
		new_urls = set(live_urls) - set(cached_live_urls)
		
		for dead_url in dead_urls:
			del self.streams[dead_url] 
			
		for channel_data in stream_data:
			url = channel_data['channel']['url']
			if url in new_urls:
				self.streams[url] = Stream(channel_data)
				new_urls.remove(url)
			else: #it is in cached_live_urls
				self.streams[url].update(channel_data)
		
	def display_streams_followed(self):

		self.get_streams_followed()
		
		while True:
			self.reset()
			#Display streams followed that are live
			self.add(["=== Streams Followed ===", "\n", "`) Refresh", "\n"] ) 

			#try:
			for i, stream in enumerate(self.streams.values()):
				stream_buffer = stream.load_stream_buffer()
				stream_buffer[0] = "%s) %s" % (hex(i + 1)[2:], stream_buffer[0]) #add index to the stream_buffer
				self.add(stream_buffer) #change add to take a list
				self.add()
			#except:
			#	pass
			self.display()
			#self.set_status(str(t1-t0))
			input = self.get_input()
			
			if input == '`':
				self.set_status("REFRESHING")
				streams = self.get_streams_followed()
			else:
				self.reset()
				self.add(["=== Qualities ===", "\n", "`) Back", "\n"])
				
				self.set_status("LOADING")
				
				try:

					stream = self.streams.values()[int(input, 16) - 1] #values() should always return the same list
					qualities = stream.load_qualities_buffer()
					if not qualities: #refresh list of streams, since this stream is now dead
						self.set_status("FAILED")
						streams = self.get_streams_followed()
					else:
						self.add(qualities)					
						self.display()
						
						input = self.get_input()
						if input != '`' and input.isdigit():
							self.set_status("STARTING")
							
							stream.watch(int(input) - 1)			
				except:
					pass
	
if __name__ == '__main__':
	s = Spazm()
	s.display_streams_followed()
