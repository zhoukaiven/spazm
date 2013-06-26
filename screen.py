#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import curses
from textwrap import wrap

class Screen(object):
	HEIGHT = 23
	WIDTH = 78
	
	screen = None
	title = None
	buffer = None
	offset = None #vertical scrolling offset

	def __init__(self):
		self.screen = curses.initscr()
		self.screen.keypad(1)
		self.screen.leaveok(1)
		curses.noecho()
		
		self.title = []
		self.buffer = []
		self.offset = 0
	
	def reset(self):
		self.buffer = []
	
	def display(self):
		self.screen.clear()
		self.screen.border(0)
		self.load_buffer()
		self.screen.refresh()
	
	def to_str(self, obj):
		try:
			return str(obj)
		except UnicodeEncodeError:
			return unicode(obj).encode('unicode_escape')
	
	def load_buffer(self):
		line = 1 #offset for the border
		
		#display title
		for text in self.title:
			self.screen.addstr(line, 1, self.to_str(text))
			line += 1
			if line == self.HEIGHT:
				return
		
		#display all lines of buffer
		for text in self.buffer[self.offset:]:
			self.screen.addstr(line, 1, self.to_str(text))
			line += 1
			if line == self.HEIGHT:
				return
	
	def add(self, str = "\n"):
		if str == "\n":
			self.buffer.append(" ") #Appending a new line breaks the border
		else:
			self.buffer.extend(wrap(str, self.WIDTH))
			
	def get_input(self):
		input = self.screen.getch()

		if input == curses.KEY_UP:
			self.scroll_up()
			return self.get_input()
		elif input == curses.KEY_DOWN:
			self.scroll_down()
			return self.get_input()
			
		return unichr(input)
		
	def scroll_up(self):
		self.offset -= 1
		if self.offset < 0:
			self.offset = 0
		else:
			self.display()
		
	def scroll_down(self):
		self.offset += 1
		if self.offset > len(self.buffer):
			self.offset = len(self.buffer)
		else:
			self.display()
		