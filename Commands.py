#!/usr/bin/python
## Commands.py

# temp... move to utility project
import subprocess
from pprint import pprint
from Handle import Handle
from Pattern import Pattern
from PatternMatch import PatternMatch
from HandleResult import HandleResult

class Commands:

	def __init__(self):
		# JSON stored command handles
		self.handles = Handle.load(Handle.HANDLES_FILENAME)

	def process(self,command):
		# TODO: 
		#	- check/feedback behaviour for multi handles or matches
		#	- database support for remembering/tracking/learning choices
		handleResults = Handle.processHandles(self.handles,command)
		return self.executeCommand(handleResults)

	def executeCommand(self,handleResults):
		# TODO:
		#	- handle errors 
		# 	- implement command collision handling (solution involving user defaults)
		# 		for now, simply take first match of first handle
		# print handleResults
		if len(handleResults) >0:
			execHandle,matches = handleResults[0]
			matched = matches[0]
			cliCommand = matched.getCliCommand()
			print cliCommand
			if cliCommand:
				stdout = self.executeCLI(cliCommand,splitCmd=True)
				return HandleResult(execHandle,handled=True,extras={"stdout":stdout})
			else:
				extras = execHandle.executeDelegate(matched)
				return HandleResult(execHandle,handled=True,extras=extras)
				# return HandleResult(execHandle,extras={"TODO":"implement handleDelegate"})
		else:
			return HandleResult(None,extras={"error":"No handle matches found"})

	def executeCLI(self,command,splitCmd=False):
		cmd = command.split() if splitCmd else command
		return subprocess.check_output(cmd)


if __name__ == "__main__":
	
	# test command regex
	testCommand = "echo hello world"
	commands = Commands()
	result = commands.process(testCommand)
	pprint (vars(result))
