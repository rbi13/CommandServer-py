#!/usr/bin/python
## HandleResult.py

class HandleResult:

	def __init__(self,handle,handled=False,engaged=False,extras={}):
		self.handle = handle
		self.handled = handled
		self.engaged = engaged
		self.extras = extras