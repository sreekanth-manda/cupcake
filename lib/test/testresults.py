#-------------------------------------------------------------------------------
# Name:        testcase - CupCake Test Results Class
# Purpose:     A module to contain a single test case, and, provides couple of
#              class methods to initiate test case, data, oracle, results etc
# Author:      Sreekanth Manda
#
# Created:     15/10/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Python imports
import time, os

class TestResults:
	'''
    TestResults maintains the results structure for muliple checks done as a
    part of a single test.
	'''
	def __init__(self):
		self._ParentTest = None
		self._results = []

	def addResult(self,oracle, actual, result):
		self._results.append([self.timestamp(),oracle,actual,result])

	def timestamp(self):
		return int(time.time())

##	def __str__(self):
##		counter = None
##		printStr = ""
##
##		for result in self._results:
##			printStr += "\n"
##			printStr += "Time    : %s\n" % str(result[0])
##			printStr += "Oracle  : %s\n" % result[1]
##			printStr += "Actual  : %s\n" % result[2]
##			printStr += "Result  : %s\n" % result[3]
##			printStr += "\n"
##		return printStr

	def setTest(self, test):
		self._ParentTest = test
