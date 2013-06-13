from livestreamer import Livestreamer
import twitchingpython
import subprocess
from subprocess import check_call, Popen, PIPE
import os

class Spazm():
	ACCESS_TOKEN = None
	twitch = None
	BASE_URL = None
	def __init__(self,token=None):
		if not token:
			self.ACCESS_TOKEN = twitchingpython.gettoken()
		else:
			self.ACCESS_TOKEN = token
		self.twitch = twitchingpython.TwitchingWrapper(self.ACCESS_TOKEN)

	def to_str(self, obj):
		try:
			return str(obj)
		except UnicodeEncodeError: # obj is unicode
			return unicode(obj).encode('unicode_escape')
			
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
		livestreamer = Livestreamer()
		plugin = livestreamer.resolve_url(url)
		qualities = plugin.get_streams().keys()
		if not qualities: #IDK why, sometimes livestreamer API doesnt work, so I manually run livestreamer
			qualities, stderr = Popen("livestreamer %s" % url, stdout=PIPE, stderr=PIPE).communicate()
		return self.to_str(qualities)
	
	def start_video(self, url, quality = "worst"):
		vid_status = None
		vid = self.run("livestreamer %s %s" % (url, quality)) #does not wait to complete
		
	def watch_streams_followed(self):
		streams = self.get_streams_followed()
		while True:
			print "\n\n"
			
			#Display streams followed that are live
			print "=== Streams Followed ==="
			
			for i, stream in enumerate(streams):
				print "%s) %s [%s]" % (i, stream['streamer'], stream['game'])
				print stream['status']
				print
				
			print "Choose: ",
			input = raw_input()
			print
			
			#Display qualities for the stream chosen
			url = self.to_str(streams[int(input)]['url'])
			print "Qualities: %s" % self.get_stream_qualities(url)
			
			print "\nChoose: ",
			input = raw_input()
			
			#Start VLC and connect to stream
			self.start_video(url, input)
			
if __name__ == '__main__':
	s = Spazm()
	while True:
		print "=== Options ==="
		options = ["Streams Following"]
		
		for i, option in enumerate(options):
			print "%s) %s" % (i, option)
			
		print "Choose: ",
		input = raw_input()
		
		if input == '0':
			s.watch_streams_followed()
