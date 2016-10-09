#-------------------------------------------------------------------------------
# Name:        testoracle - CupCake Test Oracle Class
# Purpose:     A module to contain a single test case, and, provides couple of
#              class methods to initiate test case, data, oracle, results etc
# Author:      Sreekanth Manda
#
# Created:     15/10/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Python imports
from collections import OrderedDict

class TestOracle:

    def __init__(self):
		self._test = None
		self.result_boolean = {
			"PASS"	: 1,
			"FAIL"  : 0
		}

    def register(self, test):
		self._test = test

    def updateTestResults(self, oracle, actual, result):
        self._test["TEST_RESULTS"].addResult(oracle, str(actual), result)

    def assertTrue(self, actual, oracle):
		result = None
		if actual:
			result = "PASS"
		else:
			result = "FAIL"
		self.updateTestResults(oracle, "%s" % str(actual), result)

    def assertEqual(self, actual, expected, oracle):
		result = None
		if actual == expected:
			result = "PASS"
		else:
			result = "FAIL"
		self.updateTestResults(oracle + ". Expected: %s" % str(expected),
                                    "%s" % str(actual), result)
		return self.result_boolean[result]

    def hasString(self, base, looking_for, oracle):
		result = None
		if type(base) is types.StringType:
			if base.find(str(looking_for)) != -1:
				result = "PASS"
				self.updateTestResults(oracle + \
                    ". Expected: Finding %s" % str(looking_for),
                    "String found.", result)
			else:
				result = "FAIL"
				self.updateTestResults(oracle + \
                    ". Expected: Finding %s" % str(looking_for),
                    "String not found.",result)
		return self.result_boolean[result]
