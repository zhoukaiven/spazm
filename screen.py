#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import curses
from textwrap import wrap

class Screen(object):
	HEIGHT = 24
	WIDTH = 78
	ACCEPTED_INPUT = "`123456789abcdef"
	
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
			return unicode(obj).encode('ascii','replace')#.encode('unicode_escape')
	
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
	
	def add(self, new_buffer = None):
		if new_buffer:
			for line in new_buffer:
				if line == "\n":
					self.buffer.append(" ")
				else:
					self.buffer.extend(wrap(self.to_str(line), self.WIDTH))
		else:
			self.buffer.append(" ") #Appending a new line breaks the border
	
	def set_status(self, status):
		self.screen.addstr(1, self.WIDTH - len(status), status, curses.A_REVERSE)
	
	def get_input(self):
		input = self.screen.getch()

		if input == curses.KEY_UP:
			self.scroll_up()
			return self.get_input()
		elif input == curses.KEY_DOWN:
			self.scroll_down()
			return self.get_input()
		elif unichr(input) not in self.ACCEPTED_INPUT:
			return self.get_input()
			
		self.offset = 0 #reset the offset so that the next buffer loaded is in the correct position
		return unichr(input)
		
	def scroll_up(self):
		self.offset -= 1
		if self.offset < 0:
			self.offset = 0
		else:
			self.display()
		
	def scroll_down(self):
		self.offset += 1
		max_offset = max(0, len(self.buffer) - self.HEIGHT)
		if self.offset > max_offset:
			self.offset = max_offset
		else:
			self.display()
		