#!/usr/bin/python
## Pattern.py


class PatternMatch:
    def __init__(self, pattern, match):
        self.pattern = pattern
        self.match = match

    def getCliCommand(self):
        if self.pattern.cliCommand:
            return PatternMatch.fillArgs(self.pattern.cliCommand, self.getArgs())
        else:
            return None

    def getDelegateFunction(self):
        return self.pattern.function

    def getArgs(self):
        return self.match.groupdict()

    def getArgTuples(self):
        return self.match.groupdict().iteritems()

    @staticmethod
    def fillArgs(cmd, args):
        for arg, argVal in args.iteritems():
            cmd = cmd.replace("<" + arg + ">", argVal)
        return cmd
