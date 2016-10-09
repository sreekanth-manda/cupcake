#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Sreek
#
# Created:     19/11/2013
# Copyright:   (c) Sreek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import cPickle as pickle
import os
import sys
import time

sys.path.append(r"C:\Tools_Automation")

#Imports from framework

#Initializing logger
logger_object = Logging(r"Framework\CUPCAKE\logs\CUPCAKE.log")

class Serialize:
    """
    """

    def __init__(self, messenger_pickle_file, vm_name):
        self._messenger_pickle_file = messenger_pickle_file
        self._vm_name = vm_name
        self._test_cases = {}
        self._messenger_dict = {}

    def get_data_from_pickle(self):
        try:
            fHandle = open(self._messenger_pickle_file, 'rb')
            self._messenger_dict = pickle.load(fHandle)
            fHandle.close()
        except Exception as exp:
            print str(exp)

    def retrieve_test_cases(self):
        try:
            #print self._messenger_dict
            if self._messenger_dict['test_cases'].has_key(self._vm_name):
                self._test_cases = self._messenger_dict['test_cases'][self._vm_name]
        except Exception as exp:
            print str(exp)


if __name__ == '__main__':
    try:
        serialize_object = Serialize(
        r"C:\Tools_Automation\Framework\CUPCAKE\data\pickle\messenger_pickle_file.pkl",
        sys.argv[1])
        serialize_object.get_data_from_pickle()
        serialize_object.retrieve_test_cases()
        if serialize_object._test_cases:
            for test_case in serialize_object._test_cases:
                try:
                    print test_case
                    test_case(
                    os.path.abspath(
                    "Framework\CUPCAKE\data\pickle\messenger_pickle_file.pkl"),
                    sys.argv[1])
                except Exception as exp:
                    print str(exp)
        fHandle = open(os.path.abspath(r"Framework\CUPCAKE\data\Done.txt"), 'w')
        fHandle.write("Done")
        fHandle.close()
    except Exception, errormsg:
        print "Script errored!"
        print "Error message: %s" % errormsg
        print "Traceback:"
        import traceback
        traceback.print_exc()
        fHandle = open(os.path.abspath(r"Framework\CUPCAKE\data\Done.txt"), 'w')
        fHandle.write("Done")
        fHandle.close()

