#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from threading import Thread, Condition
import os
import subprocess
from subprocess import check_call, Popen, PIPE
import re
from livestreamer import Livestreamer

class Stream(object):
	def __init__(self, channel_data):
		self.update(channel_data)
		
		self.qualities = None
		
		self.thread_condition = Condition()
		self.thread = Thread(target = self.get_stream_qualities)
		self.thread.daemon = True
		self.thread.start()
		
	def update(self, channel_data):
		channel = channel_data['channel']
		
		self.streamer = channel['display_name']
		self.status = channel['status']
		self.game = channel['game']
		self.url = channel['url'] #primary key
	
	def run(self, cmd):
		startupinfo = None
		if os.name == 'nt': #might be redundant due to threading
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=PIPE, stderr=PIPE)
		return process
	
	def load_stream_buffer(self):
		buffer = ["%s [%s]" % (self.streamer, self.game), self.status]
		return buffer

	def get_stream_qualities(self):
		self.thread_condition.acquire()
		
		'''	 #can't use this until livestreamer python api supports flash streams
		livestreamer = Livestreamer()
		plugin = livestreamer.resolve_url(self.url)

		self.qualities = plugin.get_streams().keys()
		'''
		qualities_data, stderr = self.run("livestreamer %s" % self.url).communicate()
		found_qualities = re.search("Found streams: (.*)", qualities_data)
		no_streams = re.search("No streams found", qualities_data)
		
		if found_qualities:
			self.qualities = found_qualities.group(1).replace("\n", '').replace("(worst)","").replace("(best)",'').replace("(worst, best)", '')
			self.qualities = [x.strip() for x in self.qualities.split(',')]
		elif no_streams:
			self.qualities = -1
		
		self.thread_condition.notify()
		self.thread_condition.release()
			
	def load_qualities_buffer(self):
		self.thread_condition.acquire()
		while not self.qualities:
			self.thread_condition.wait()
		
		if self.qualities == -1:
			return None
		else:
			buffer = list(self.qualities) #create a copy
			for i, quality in enumerate(buffer):
				buffer[i] = "%s) %s"%( (i+1), quality )
			return buffer
		'''
		if self.qualities:
			buffer = list(self.qualities) #create a copy
			for i, quality in enumerate(buffer):
				buffer[i] = "%s) %s"%( (i+1), quality )
			return buffer
		elif self.qualities == -1:
			return None
		else:
			self.get_stream_qualities()
			return self.load_qualities_buffer()
		'''
		
	def watch(self, quality):
		self.run("livestreamer %s %s" % (self.url, self.qualities[quality])) #does not wait to complete
