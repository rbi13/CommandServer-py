#!/usr/bin/python
## Handle.py

import json
from Pattern import Pattern
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

	def __init__(self, info):
		self.name = info.get(Handle.NAME_KEY)
		self.description = info.get(Handle.DESCRIPTION_KEY)
		self.delegatePath = info.get(Handle.DELEGATE_PATH_KEY)
		self.manPath = info.get(Handle.MAN_PATH_KEY)
		self.patterns = Pattern.load(info.get(Handle.PATTERNS_LIST_KEY))

		# dynamically loaded HandleDelegate
		# TODO: error handling
		if self.delegatePath:
			self.delegate = dynamic.load_class(self.delegatePath)()

	def executeDelegate(self, match):
		# TODO:
		#	Figure out how to give args so that args are passed in line as usual
		method = match.getDelegateFunction()
		args = match.getArgs()

		return dynamic.call_method(self.delegate, method, args)

	@staticmethod
	def processHandles(handle_list, compare):
		handle_results = []
		for handle in handle_list:
			matches = Pattern.getMatches(handle.patterns, compare)
			if len(matches) > 0:
				handle_results.append((handle, matches))
		return handle_results

	@staticmethod
	def load(path):
		# Handle[]
		handles = []
		handles_json = json.load(open(path))
		# pprint(handlesJson)
		for handleDef in handles_json.get(Handle.HANDLES_LIST_KEY):
			try:
				handles.append(Handle(handleDef))
			except ImportError:
				print("Warning: " + handleDef.get(Handle.NAME_KEY) + " project not found")
		return handles


if __name__ == "__main__":
	# test dynamic delegate loading
	delegateClass = dynamic.load_class("crazyflie-clients-python.CrazyflieHandleDelegate.CrazyflieHandleDelegate")
	delegate = delegateClass()
	delegate.handle()
