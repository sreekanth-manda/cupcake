#-------------------------------------------------------------------------------
# Name:        ck_parser - A CupCake Parser Class
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
    """A class to read data from a JSON file and stores in a python data
    strcutre DICT, and, makes it available across all the tests
    """

    #Class data memebers
    def __init__(self):
        """Constructor to initialize _json_file_path, _json_object and
        _json_object, Pass json file path while initializing an object of this
        class
        """
        try:
            print "Initializing Parser Class"
            self._json_file_path = None
            self._json_object = dict()
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

    def get_json_object(self):
        """A function to get all test details, set to run in JSON file and
        stores them in a dict format in _json_object
        Consumes: self._json_object
        Returns : none, test data would be stored in self._json_object
        Purpose : A function to get all test details, set to run in JSON file
                  and stores them in a dict format in _json_object
        Example : get_json_object() -> dict _json_object;
        """
        try:
            if self._json_object:
                for dict_key, child_dict in self._json_object.items():
                    if child_dict['status'] == 'ON':
                        self._json_object[dict_key] = child_dict
        except Exception as exp_obj:
            print "Error occured in get_json_object() :",
            print exp_obj
            exit()

    def print_json_object(self):
        """A function to print test data which is set to run in JSON file
        Consumes: self._json_object
        Returns : none
        Purpose : A function to print test data which is set to run in JSON file
        Example : print_json_object() -> prints _json_object;
        """
        try:
            if self._json_object:
                for p_key, p_val in self._json_object.items():
                    print "Key : " + str(p_key) + "\n"
                    for c_key, c_val in p_val.items():
                        print "\t"+ c_key + " -- " + str(c_val)
            else:
                print "No JSON object found to print, please verify JSON file \
                for correctness"
        except Exception as exp_obj:
            print "Error occured in print_json_object() : ",
            print exp_obj