#-------------------------------------------------------------------------------
# Name:        constructer.py
# Purpose:     This module stores all the test cases that are selected by user
#              to execute later in the process of automation
# Author:      Sreekanth Manda
#
# Created:     17/10/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Python generic modules import
from collections import OrderedDict
import sys

#Add root folder path to sys.path; read the path from constructor jason file in
#later stage
sys.path.append(r"D:\Tools_Automation")

#Imports from framework
from constructor_parser import Parser
from Framework.CUPCAKE.lib.utils.logger import Logging

#Initializing logger
logger_object = Logging(r"Framework\CUPCAKE\logs\CUPCAKE.log")

class Constructor:

    """
    Constructor class definition goes here
    """

    def __init__(self, testcases_json_file, product_json_file, os_json_file):
        """
        Initialize _test_cases list object and _jason_file_path
        """
        self._test_cases = OrderedDict()
        self._product_info = OrderedDict()
        self._os_info = OrderedDict()
        self._testcases_json_file = testcases_json_file
        self._product_json_file = product_json_file
        self._os_json_file = os_json_file

    def get_class(self, class_name):
        try:
            """
            Imports class by importing inidividuals modules to make the class
            available for initializing object in later stage
            """
            parts = class_name.split('.')
            module = ".".join(parts[:-1])
            top_module = __import__ ( module )
            for comp in parts[1:]:
                top_module = getattr(top_module, comp)
            return top_module
        except Exception as exp:
            print str(exp)

    def get_testcases(self):
        """
        Gets all classes set to run and stores in _test_cases
        """
        test_data_obj = Parser()
        test_data_obj.read_json_file(self._testcases_json_file)
        test_data_obj.get_targeted_test()
        for os_name, test_cases in test_data_obj._targeted_test.items():
            for test_case in test_cases:
                index = test_cases.index(test_case)
                test_cases[index] = (self.get_class(test_case))
            self._test_cases[os_name] = test_cases

    def get_product_data(self):
        """
        Retrieves information about product under test
        """
        product_data_obj = Parser()
        product_data_obj.read_json_file(self._product_json_file)
        for keys, values in product_data_obj._json_object.items():
            self._product_info[keys] = values

    def get_os_data(self):
        """
        get_os_data information goes here
        """
        os_data_obj = Parser()
        os_data_obj.read_json_file(self._os_json_file)
        for keys, values in os_data_obj._json_object.items():
            self._os_info[keys] = values