#!/usr/bin/python
## Handle.py

import json
import re
from pprint import pprint
from Pattern import Pattern
from PatternMatch import PatternMatch
import dynamic

class Handle:

	# static
	# JSON file keys
	# file defining command handles in JSON format
	HANDLES_FILENAME = "handles.json"
	HANDLES_LIST_KEY = "handle_list"

	# Handle keys
	NAME_KEY = "name"
	DESCRIPTION_KEY = "description"
	DELEGATE_PATH_KEY = "delegatePath"
	MAN_PATH_KEY = "manPath"
	PATTERNS_LIST_KEY = "patterns"

	def __init__(self,info):
		self.name = info.get(Handle.NAME_KEY)
		self.description = info.get(Handle.DESCRIPTION_KEY)
		self.delegatePath = info.get(Handle.DELEGATE_PATH_KEY)
		self.manPath = info.get(Handle.MAN_PATH_KEY)
		self.patterns = Pattern.load(info.get(Handle.PATTERNS_LIST_KEY))

		# dynamically loaded HandleDelegate
		# TODO: error handling
		if self.delegatePath:
			self.delegate = dynamic.loadClass(self.delegatePath)()

	def executeDelegate(self,match):
		# TODO:
		#	Figure out how to give args so that args are passed in line as ussual
		method = match.getDelegateFunction()
		args = match.getArgs()
		print args
		return dynamic.callMethod(self.delegate,method,args)

	@staticmethod
	def processHandles(handleList,compare):
		handleResults = []
		for handle in handleList:
			matches = Pattern.getMatches(handle.patterns,compare)
			if len(matches) >0:
				handleResults.append( (handle,matches) )
		return handleResults

	@staticmethod
	def load(path):
		# Handle[]
		handles = []
		handlesJson = json.load(open(path))
		#pprint(handlesJson)
		for handleDef in handlesJson.get(Handle.HANDLES_LIST_KEY):
			handles.append(Handle(handleDef))
		return handles

if __name__ == "__main__":

	# test dynamic delegate loading
	delegateClass = dynamic.loadClass("crazyflie-clients-python.CrazyflieHandleDelegate.CrazyflieHandleDelegate")
	delegate = delegateClass()
	delegate.handle()