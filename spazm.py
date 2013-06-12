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

	def safe_print(self, phrase):
		try:
			print str(phrase)
		except UnicodeEncodeError: # obj is unicode
			print unicode(phrase).encode('unicode_escape')
	
	def to_str(self, obj):
		try:
			return str(phrase)
		except UnicodeEncodeError: # obj is unicode
			return unicode(phrase).encode('unicode_escape')
			
	def run(self, cmd):
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		stdout = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=PIPE, stderr=PIPE)
		return stdout
	
	def watch_streams_followed(self):
		livestreamer = Livestreamer()
		
		streams = []
		streams_followed = self.twitch.getstreamsfollowing()["streams"]
		for i in range(0, len(streams_followed)):
				channel = streams_followed[i]['channel']
				
				stream = {}
				stream['streamer'] = channel['display_name']
				stream['status'] = channel['status']
				stream['game'] = channel['game']
				stream['url'] = channel['url']

				streams.append(stream)
			
		while True:
			print "\n\n"
			
			#Display streams followed that are live
			print "=== Streams Followed ==="
			for i in range(0, len(streams)):
				stream = streams[i]
				self.safe_print("%s) %s [%s]" % (i, stream['streamer'], stream['game']))
				self.safe_print(stream['status'])
				print
				
			print "\nChoose: ",
			input = raw_input()
			print
			
			#Display qualities for the stream chosen
			url = streams[int(input)]['url']
			
			plugin = livestreamer.resolve_url(url)
			qualities = plugin.get_streams().keys()
			if not qualities: #IDK why, sometimes livestreamer API doesnt work, so I manually run livestreamer
				qualities, stderr = Popen("livestreamer %s" % url, stdout=PIPE, stderr=PIPE) #possibly opens new cmd prompt
			self.safe_print("Qualities: %s" %qualities)
			
			print "\nChoose: ",
			input = raw_input()
			
			#Start VLC and connect to stream
			self.run("livestreamer %s %s" % (url, input)) #does not wait to complete
			
			'''
			#Allow quality change
			'''
			
if __name__ == '__main__':
	ACCESS_TOKEN = "2abycrsbnonndh31nkxfuq96yh8flqg"
	s = Spazm(ACCESS_TOKEN)
	while True:
		print "=== Options ==="
		print "1) Following streams"
		print "Choose: ",
		input = raw_input()
		
		if input == '1':
			s.watch_streams_followed()
