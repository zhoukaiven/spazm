#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import subprocess
from subprocess import check_call, Popen, PIPE
import re

class Stream(object):
	def __init__(self, channel_data):
		channel = channel_data['channel']
		
		self.streamer = channel['display_name']
		self.status = channel['status']
		self.game = channel['game']
		self.url = channel['url'] #primary key
		
		self.qualities = None
		
	def run(self, cmd):
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=PIPE, stderr=PIPE)
		return process
	
	def load_stream_buffer(self):
		'''
		self.add("%s) %s [%s]" % (hex(i + 1)[2:], stream['streamer'], stream['game']))
		self.add(stream['status'])
		self.add()
		'''
		buffer = ["%s [%s]" % (self.streamer, self.game), self.status]
		return buffer

	def get_stream_qualities(self):
		'''
		#doesn't return all qualities
		livestreamer = Livestreamer()
		plugin = livestreamer.resolve_url(self.url)

		qualities = plugin.get_streams().keys()
		'''
		#qualities, stderr = Popen("livestreamer %s" % self.url, stdout=PIPE, stderr=PIPE).communicate()
		qualities_data, stderr = self.run("livestreamer %s" % self.url).communicate()
		found_qualities = re.search("Found streams: (.*)", qualities_data)
		if found_qualities:
			self.qualities = found_qualities.group(1).replace("\n", '').replace("(worst)","").replace("(best)",'').replace("(worst, best)", '')
			self.qualities = [x.strip() for x in self.qualities.split(',')]
				
	def load_qualities_buffer(self):
		if self.qualities:
			buffer = list(self.qualities) #create a copy
			for i, quality in enumerate(buffer):
				buffer[i] = "%s) %s"%( (i+1), quality )
			return buffer
		else:
			self.get_stream_qualities()
			return self.load_qualities_buffer()
		
	#def start_video(self, url, quality = "worst"):
	def watch(self, quality = "worst"):
		self.run("livestreamer %s %s" % (self.url, self.qualities[quality])) #does not wait to complete
		
	def get_url(self):
		return self.url