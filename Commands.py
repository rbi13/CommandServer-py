#!/usr/bin/python
## Commands.py

# temp... move to utility project
import subprocess
from pprint import pprint
from Handle import Handle
from HandleResult import HandleResult

class Commands:

	def __init__(self):
		# JSON stored command handles
		self.handles = Handle.load(Handle.HANDLES_FILENAME)

	def process(self, command):
		# TODO:
		#	- check/feedback behaviour for multi handles or matches
		#	- database support for remembering/tracking/learning choices
		handle_results = Handle.processHandles(self.handles, command)
		return self.executeCommand(handle_results)

	@staticmethod
	def execute_command(handle_results):
		# TODO:
		#	- handle errors
		# 	- implement command collision handling (solution involving user defaults)
		# 		for now, simply take first match of first handle
		# print handle_results
		if len(handle_results) > 0:
			exec_handle, matches = handle_results[0]
			matched = matches[0]
			cli_command = matched.getCliCommand()
			print(cli_command)
			if cli_command:
				stdout = handle_results.execute_cli(cli_command, split_cmd=True)
				return HandleResult(exec_handle, handled=True, extras={"stdout": stdout})
			else:
				extras = exec_handle.executeDelegate(matched)
				return HandleResult(exec_handle, handled=True, extras=extras)
			# return HandleResult(execHandle,extras={"TODO":"implement handleDelegate"})
		else:
			return HandleResult(None, extras={"error": "No handle matches found"})

	@staticmethod
	def execute_cli(command, split_cmd=False):
		cmd = command.split() if split_cmd else command
		return subprocess.check_output(cmd)

if __name__ == "__main__":
	# test command regex
	testCommand = "echo hello world"
	commands = Commands()
	result = commands.process(testCommand)
	pprint(vars(result))
