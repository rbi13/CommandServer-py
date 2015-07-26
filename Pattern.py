#!/usr/bin/python
## Pattern.py

import re
from PatternMatch import PatternMatch


class Pattern:
    # Pattern keys
    PATTERN_KEY = "pattern"
    CLI_COMMAND_KEY = "cliCommand"
    FUNCTION_KEY = "function"

    def __init__(self, info):
        self.pattern = info.get(Pattern.PATTERN_KEY)
        self.cliCommand = info.get(Pattern.CLI_COMMAND_KEY)
        self.function = info.get(Pattern.FUNCTION_KEY)

    def match(self, compare):
        match = re.search(self.pattern, compare)
        if match:
            return PatternMatch(self, match)
        else:
            return None

    @staticmethod
    def getMatches(pattern_list, compare):
        matches = []
        for pattern in pattern_list:
            match = pattern.match(compare)
            if match:
                matches.append(match)
        return matches

    @staticmethod
    def load(json_list):
        # Pattern[]
        patterns = []
        # pprint(json_list)
        for patternDef in json_list:
            patterns.append(Pattern(patternDef))
        return patterns
