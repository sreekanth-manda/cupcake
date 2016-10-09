#-------------------------------------------------------------------------------
# Name:        parser.py - A constructor's parser class
# Purpose:     A module to read data from a JSON file and stores in a python
#              data strcutre DICT, and, makes it available across all the tests
# Author:      Sreekanth Manda
#
# Created:     27/09/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Imports
import json

#Class to hold data that is read from JSON file
class Parser:
    """A class to parse targeted test cases from a JSON file and stores in a
    python data strcutre DICT, and, makes it availableto use later in a class
    variable
    """

    #Class data memebers
    def __init__(self):
        """Constructor to initialize _json_file_path, _json_object and
        _targeted_test, Pass json file path while initializing an object of this
        class
        """
        try:
            self._json_file_path = None
            self._json_object = None
            self._targeted_test = dict()
        except WindowsError as exp:
            print "Error occured in __init__():",
            print exp
            exit()
        except Exception as exp_obj:
            print "Error occured in __init__() :",
            print exp_obj
            exit()

    def read_json_file(self, _json_file_path):
        """A function to read all data from a JSON file and stores in a python
        data strcutre DICT.
        Consumes: self._json_file_path
        Returns : none, test data would be stored in self._json_object
        Purpose : A function to read all data from a JSON file and stores in a
                  python data strcutre DICT.
        Example : read_json_file() -> dict _json_object;
        """
        try:
            self._json_file_path = _json_file_path
            self._json_object = json.load(open(self._json_file_path))
        except IOError as exp_obj:
            print "Error occured in read_json_file():",
            print exp_obj
            exit()
        except Exception as exp_obj:
            print "Error occured in read_json_file() :",
            print exp_obj
            exit()

    def get_targeted_test(self):
        """A function to get all test details, set to run in JSON file and
        stores them in a dict format in _targeted_test
        Consumes: self._json_object
        Returns : none, test data would be stored in self._targeted_test
        Purpose : A function to get all test details, set to run in JSON file
                  and stores them in a dict format in _targeted_test
        Example : get_targeted_test() -> dict _targeted_test;
        """
        try:
            if self._json_object:
                for dict_key, child_dict in self._json_object.items():
                    test_cases_list = []
                    for child_dict_key, child_dict_value in child_dict.items():
                        if child_dict_value == 'ON':
                            test_cases_list.append(child_dict_key)
                    if test_cases_list:
                        self._targeted_test[dict_key] = test_cases_list
        except Exception as exp_obj:
            print "Error occured in get_targeted_test() :",
            print exp_obj
            exit()


    def print_test_data(self):
        """A function to print test data which is set to run in JSON file
        Consumes: self._targeted_test
        Returns : none
        Purpose : A function to print test data which is set to run in JSON file
        Example : print_test_data() -> prints _targeted_test;
        """
        try:
            if self._targeted_test:
                for p_key, p_val in self._targeted_test.items():
                    print "Test Name : " + str(p_key)
                    print "Test Properties..."
                    for c_key, c_val in p_val.items():
                        print "\t"+ c_key + " -- " + str(c_val)
            else:
                print "No test is targeted to run, please set test status to ON"
        except Exception as exp_obj:
            print "Error occured in print_test_data() : ",
            print exp_obj