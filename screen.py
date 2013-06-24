#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import curses
from textwrap import wrap

class Screen(object):
	HEIGHT = 25
	WIDTH = 80
	
	screen = None
	title = None
	buffer = None
	offset = None #vertical scrolling offset

	def __init__(self):
		self.screen = curses.initscr()
		self.title = []
		self.buffer = []
		self.offset = 0
	
	def reset(self):
		self.buffer = []
	
	def display(self):
		self.screen.clear()
		self.load_buffer()
		self.screen.refresh()
	
	def to_str(self, obj):
		try:
			return str(obj)
		except UnicodeEncodeError:
			return unicode(obj).encode('unicode_escape')
	
	def load_buffer(self):
		line = 0
		
		#display title
		for text in self.title:
			self.screen.addstr(line, 0, self.to_str(text))
			line += 1
			if line == self.HEIGHT:
				return
		
		#display all lines of buffer
		for text in self.buffer[self.offset:]:
			self.screen.addstr(line, 0, self.to_str(text))
			line += 1
			if line == self.HEIGHT:
				return
	
	def add(self, str = "\n"):
		if str == "\n":
			self.buffer.append(str)
		else:
			self.buffer.extend(wrap(str, self.WIDTH))
			
	def get_input(self):
		return unichr(self.screen.getch())
		
	def scroll_up(self):
		self.offset -= 1
		if self.offset < 0:
			self.offset = 0
		
	def scroll_down(self):
		self.offset += 1
		if self.offset > len(self.buffer):
			self.offset = len(self.buffer)
		