#-------------------------------------------------------------------------------
# Name:        testcase - CupCake Test Case Class
# Purpose:     A module to contain a single test case, and, provides methods to
#              initiate test case, data, oracle, results etc
# Author:      Sreekanth Manda
#
# Created:     15/10/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#General Python modules import
import collections
import subprocess
import time
from collections import OrderedDict

#Imports from CUPCAKE Framework
from .testoracle import TestOracle
from .parser import TestData
from .testresults import TestResults



#Class to hold all details of a particular test
class TestCase:
    """
    A class to hold all details of a particular test, one should create a
    wrapper of this class and then build test case on it
    Data:
        _test_dict : A dictionary to hold information related to a test case
    Methods:
        __init__() : Initializes TestClass Object with defaults
        prepare()  : Prepares a TestClass Object
        execute_command() : Executes a command supplied
        set_time_to_execute() : Sets total time taken to run a test case
        __str__() : Displays certain test case properties
    Notes:
        one should create object of this class and then build test case
        accordingly,
        TestData() - TestData class from CupCake Framework which was imported
        from parser module
    """

    def __init__(self):
        self._test_dict = OrderedDict()
        self.initialize_dict()

    def initialize_dict(self):
        self._test_dict["NAME"] = None
        self._test_dict["ID"] =  None
        self._test_dict["SUMMARY"] =  None
        self._test_dict["TEST_DATA"] =  TestData()
        self._test_dict[ "TEST_ORACLE"] =  TestOracle()
        self._test_dict["TEST_RESULTS"] =  TestResults()
        self._test_dict["RETURN_CODE"] =  None
        self._test_dict["PLATFORM"] =  None
        self._test_dict["START_TIME"] =  None
        self._test_dict["END_TIME"] =  None
        self._test_dict["TIME_TO_EXECUTE"] =  None
        self._test_dict["FLAG"] =  None
        self._test_dict["STATUS"] =  False
        self._test_dict["REBOOT"] =  False
        self._test_dict["INTERNAL_ID"] =  None
        self._test_dict["THREADED"] =  False
        self._test_dict["EXECUTION_STATUS"] =  None
        self._test_dict["LAST_EXECUTED"] =  time.ctime()
        self._test_dict["PRIORITY"] = None

    def prepare(self):
        """
        Consumes: None
        Returns : None
        Purpose : None
        Example : None
        """
        #Implementation based on need
        pass

    def setup(self):
        """
        Consumes: None
        Returns : None
        Purpose : None
        Example : None
        """
        #Implementation based on need
        pass

    def cleanup(self):
        """
        Consumes: None
        Returns : None
        Purpose : None
        Example : None
        """
        #Implementation based on need
        pass

    def execute_command(self, what_to_execute):
        """
        Consumes: None
        Returns : None, sets RETURN_CODE
        Purpose : Executes a command supplied in "what_to_execute" and sets
                  RETURN_CODE returned from subprocess which indicates the
                  result of the command executed
        Example : execute_command("notepad.exe") -> _test_dict["RETURN_CODE"]
        """
        print "Executing TC " + self._test_dict["NAME"]
        proc = subprocess.Popen(what_to_execute, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)
        STDOUT, STDERR = proc.communicate()
        self._cmd_returncode = proc.returncode
        self._test_dict["RETURN_CODE"] = proc.returncode
        return STDOUT, STDERR

    def set_time_to_execute(self):
        """
        Consumes: None
        Returns : None, sets TIME_TO_EXECUTE
        Purpose : Gets the difference from START_TIME to END_TIME to calculate
                  TIME_TO_EXECUTE for a test cases.
        Example : set_time_to_execute() -> _test_dict["TIME_TO_EXECUTE"];
        """
        self._test_dict["TIME_TO_EXECUTE"] = self._test_dict["END_TIME"] - \
                                             self._test_dict["START_TIME"]

    def __str__(self):
        printStr = "-" * 50 + "\n"
        printStr += "Name     			: %s\n" % self._test_dict["NAME"]
        printStr += "Summary  			: %s\n" % self._test_dict["SUMMARY"]
        #printStr += "Result   			: %d\n" % self["RESULT_ID"]
        printStr += "Execution Status  	: %s\n" % self._test_dict["EXECUTION_STATUS"]
        printStr += "Execution Time		: %s seconds\n" % \
                                    str(self._test_dict["TIME_TO_EXECUTE"])
        printStr += "Status  			: %s\n" % self._test_dict["STATUS"]
        printStr += "Last Executed       : %s\n" % self._test_dict["LAST_EXECUTED"]
        printStr += "Platforms         : %s\n" % self._test_dict["PLATFORM"]
        printStr += "-" * 50 + "\n"
        return printStr
