#-------------------------------------------------------------------------------
# Name:        messenger.py
# Purpose:     Messenger unit part of CUPCAKE framework acts as a channel
#              between UI and the framework, it retrieves information provided
#              by user prepares and serializes the data and then passes on to
#              framework
#
# Author:      Sreekanth Manda
#
# Created:     17/10/2013
# Copyright:   (c) Sreekanth Manda 2013
# Licence:     GPL
#-------------------------------------------------------------------------------

#Python imports
from collections import OrderedDict
import collections
import json
import sys
import os
import cPickle as pickle
import time
import types
import datetime

#Add root folder path to sys.path; read the path from constructor jason file in
#later stage
sys.path.append(r"D:\Tools_Automation")

#CUPCAKE framework imports
from Framework.CUPCAKE.constructor.constructor import Constructor
from Framework.CUPCAKE.lib.vmmanager.vmmanager import VMManager
from Framework.CUPCAKE.lib.utils.logger import Logging
from Framework.CUPCAKE.lib.utils.sendmail import SendMail

#Initializing logger from
logger_object = Logging(r"Framework\CUPCAKE\logs\CUPCAKE.log")

#mail config
hostName="mail.na.nai.com"

sendMailToList=["Sreekanth_Manda@gmail.com"]
sendMailFromID="Framework.CUPCAKE@company.com"
subject = "Test Results"

class Messenger():
    try:
        """
        Messenger class information goes here
        """
        def __init__(self, constructor_json_file,
                            vm_json_file,
                            product_json_file,
                            os_json_file):
            """
            __init__() information goes here
            """
            logger_object.create_log("info",  ":MESSENGER:" + \
                                        "Initializing Messenger unit")

            #Messengers data structure
            self._messenger_data = OrderedDict()
            self._constructor_json_file = constructor_json_file
            self._vm_json_file = vm_json_file
            self._product_json_file = product_json_file
            self._os_json_file = os_json_file
            self._vm_json_object = OrderedDict()
            self._results_dict = OrderedDict()
            self._master_result_dict = OrderedDict()
            self._master_test_oracle = OrderedDict()
            self._max_col_size = None
            self._html_output = str()
            self.run_messenger()


        def read_json_file(self):
            """A function to read all data from a JSON file and stores in a python
            read_json_file information goes here
            """
            try:
                #print "Loading VM json file - " + self._vm_json_file
                logger_object.create_log("info",":MESSENGER: Loading VM json file -"
                + self._vm_json_file)
                self._vm_json_object = json.load(open(self._vm_json_file))
            except Exception as exception:
                logger_object.create_log("info",":MESSENGER:Encountered erro in "
                                    "messenger.read_json_file() when loading " + \
                " VM json file" + self._vm_json_file)
                print "Error occured in read_json_file() :",
                print str(exception)
    #            exit()

        def run_messenger(self):
            try:
                logger_object.create_log("info",":MESSENGER:Running messenger unit")
                self.call_constructor()
                self.prepare_os()
                #self.call_vmmanager()
            except Exception as exception:
                logger_object.create_log("info",  ":MESSENGER:" +\
                 "Encountered erro in messenger.run_messenger()")
                print "Error occured in messenger.run_messenger() :",
                print str(exception)
    #            exit()

        def call_constructor(self):
            print "Messenger unit working with constructor unit"
            logger_object.create_log("info",
                                ":MESSENGER:Working with constructor unit")
            logger_object.create_log("info",
                                ":MESSENGER:Initializing Constructor unit")
            constructor_object = Constructor(self._constructor_json_file,
                                                self._product_json_file,
                                                self._os_json_file)
            logger_object.create_log("info",  ":MESSENGER: Constructor unit "
            "retrieving targeted tests and OS information from JSON files")
            print "Constructor unit retrieving targeted tests, OS information"
            constructor_object.get_testcases()
            print "Constructor unit retrieving product under test information"
            constructor_object.get_product_data()
            print "Constructor unit retrieving os information"
            constructor_object.get_os_data()
            self._messenger_data["test_cases"] = constructor_object._test_cases
            self._messenger_data["product_info"] = constructor_object._product_info
            self._messenger_data["os_info"] = constructor_object._os_info

        def prepare_os(self):
            self.read_json_file()
            vm_settings = OrderedDict()
            for key in self._messenger_data["test_cases"].iterkeys():
                if self._vm_json_object.has_key(key):
                    vm_settings[key] = self._vm_json_object[key]
            self._messenger_data["vm_info"] = vm_settings

        def parse_result_files(self):
            for os_name in self._messenger_data['test_cases'].iterkeys():
                for pkl_file in os.listdir(os.path.abspath
                                (r"Framework\CUPCAKE\data\results\\" + os_name)):
                    fHandle = open (os.path.abspath
                    (r"Framework\CUPCAKE\data\results\\" + os_name + "\\" + \
                            pkl_file), 'r')
                    results_obj = pickle.load(fHandle)
                    fHandle.close()

                    if self._results_dict.has_key(pkl_file):
                        self._results_dict[pkl_file].append(results_obj)
                    else:
                        self._results_dict[pkl_file] = []
                        self._results_dict[pkl_file].append(results_obj)

        def prepare_master_results(self):
            print "Preparing results..."
            #Collection of Dicts from self._results_dict
            for dict_key, dict_items in self._results_dict.iteritems():
                super_dict = collections.defaultdict(set)
                #Item from collection, which is a dict from collection of dicts
                for current_dict in dict_items:
                    #Key, Values from the above dict (item)
                    for key, value in current_dict.iteritems():
                        super_dict[key].add(value)
                self._master_result_dict[dict_key] = super_dict

        def print_master_results(self):
            for master_keys, master_items in \
                                self._master_result_dict.items():
                print "\n\n\t@@@@@@@@@@ " + master_keys + " @@@@@@@@@@"
                for key, value in master_items.iteritems():
                    print key + " : ",
                    #print value
                    for item in value:
                        if isinstance(item, types.InstanceType):
                            if item.__class__.__name__ == 'TestResults':
                                print item._results
                        else:
                            print str(item) + "\n"

        def prepare_oracle(self):
            for master_keys, master_items in self._master_result_dict.items():
                current_test_oracle = OrderedDict()
                #print master_keys, master_items
                platforms = master_items["PLATFORM"].copy()
                platform_results = master_items["TEST_RESULTS"].copy()
                for count in range(0, len(platforms)):
                    current_test_oracle[platforms.pop()] = \
                                            (platform_results.pop())._results
                self._master_test_oracle[master_keys] = current_test_oracle
            print self._master_test_oracle

        def add_css(self):
            print "Adding style sheet to HTML.."
            css_code = str()
            css_code = css_code + "\n" + \
            "<style type=\"text/css\">" + "\n" + \
            "table.maintable, th, td" + "\n" + \
            "{" + "\n" + \
           	"font-family: verdana,arial,sans-serif;" + "\n" + \
            "font-size:11px;" + "\n" + \
            "border-collapse:collapse;" + "\n" + \
            "table-layout:fixed;" + "\n" + \
            "border: 1px solid black;" + "\n" + \
            "empty-cells:show;" + "\n" + \
            "border-width: 1px;" + "\n" + \
            "}" + "\n" + \
            "table.secondtable, th, td" + "\n" + \
            "{" + "\n" + \
           	"font-family: verdana,arial,sans-serif;" + "\n" + \
            "font-size:11px;" + "\n" + \
            "border-collapse:collapse;" + "\n" + \
            "table-layout:fixed;" + "\n" + \
            "empty-cells:show;" + "\n" + \
            "border-width: 1px;" + "\n" + \
            "}" + "\n" + \
            "table.thirdtable" + "\n" + \
            "{" + "\n" + \
           	"font-family: verdana,arial,sans-serif;" + "\n" + \
            "font-size:11px;" + "\n" + \
            "border-collapse:collapse;" + "\n" + \
            "table-layout:auto;" + "\n" + \
            "empty-cells:show;" + "\n" + \
            "border-width: 1px;" + "\n" + \
            "}" + "\n" + \
            "td, th" + "\n" + \
            "{" + "\n" + \
            "border-collapse:collapse;" + "\n" + \
            "overflow:hidden;" + "\n" + \
            "text-align:center;" + "\n" + \
            "vertical-align:middle;" + "\n" + \
            "width:250px;" + "\n" + \
            "white-space: nowrap;" + "\n" + \
            "}" + "\n" + \
            r"</style>"

            return css_code

        def prepare_oracle_html_report(self):

            now = datetime.datetime.now()
            html_file_name = now.strftime("%Y-%m-%d-%H-%M-%S")
            fHandle = open(r"Framework\CUPCAKE\data\master_report\\" + \
                                html_file_name + ".htm", 'w')

            self._html_output = r"<html><head>"
            self._html_output = self._html_output + self.add_css()
            self._html_output = self._html_output + "</head><body>" + \
                                                "<table class=\"maintable\">"

            self._html_output = self._html_output + \
                r"<tr>" + \
                r"<th >Test Case</td>" +\
                r"<th >Test Results</td>" +\
                r"</tr>"

            for keys, items in self._master_test_oracle.iteritems():

                #Row 2 with data - tc_name, os, test_oracle
                self._html_output = self._html_output + \
                r"<tr>"

                #Cell 1 with tc_name
                self._html_output = self._html_output + \
                r"<td>" + \
                keys + r"</td>"

                #Cell 2 with os and oracle
                self._html_output = self._html_output + \
                r"<td >"

                self._html_output = self._html_output + \
                                        "<table class=\"secondtable\">" + \
                                        r"<th >OS Name</td>" +\
                                        r"<th >Test Oracle</td>"

                for child_keys, child_items in items.iteritems():

                    self._html_output = self._html_output + r"<tr>"

                    #Cell 2 with os_name
                    self._html_output = self._html_output + \
                    r"<td >" + \
                    child_keys + r"</td>"

                    #Cell 3 with test_oracle
                    self._html_output = self._html_output + \
                    r"<td >"

                    for sub_item in child_items:
                        self._html_output = self._html_output + \
                        r"<table class=\"thirdtable\">" + \
                        r"<tr>"

                        for item in sub_item:
                            self._html_output = self._html_output + \
                            r"<td>" + str(item) + r"</td>"

                        self._html_output = self._html_output + r"</tr>"
                        self._html_output = self._html_output + r"</table>"

                self._html_output = self._html_output + r"</td>"
                self._html_output = self._html_output + r"</tr>"
                self._html_output = self._html_output + r"</table>"

                self._html_output = self._html_output + r"</td>"
                self._html_output = self._html_output + r"</tr>"
            self._html_output = self._html_output + r"</table>"

            self._html_output = self._html_output + r"</body></html>"

            fHandle.write(self._html_output)

            fHandle.close()

##        def prepare_master_report(self):
##            now = datetime.datetime.now()
##            html_file_name = now.strftime("%Y-%m-%d-%H-%M-%S")
##            fHandle = open(r"Framework\CUPCAKE\data\master_report\\" + \
##                                html_file_name + ".htm", 'w')
##
##            self._html_output = r"<html><body><table cellspacing='0' " + \
##            " border='1' style='empty-cells:show;' " + \
##            " >"
##
##            self._html_output = self._html_output + \
##                    r"<tr>" + \
##                    r"<td  nowrap font-size='1'  >Test Case</td>"
##
##            #List to hold HTML table row 1 values (Column headings)
##            col_headings = []
##
##            master_items = self._master_result_dict.values()
##
##            for child_keys in master_items[0].iterkeys():
##                    col_headings.append(child_keys)
##
##            for heading in col_headings:
##                self._html_output = self._html_output + \
##                                r"<td  width=25%font-size='1'  >" + \
##                                heading + r"</td>"
##
##            self._html_output = self._html_output + \
##                    r"</tr>"
##
##            #Table Data
##            self._html_output = self._html_output + \
##                    r"<tr>"
##
##            for master_keys, master_items in \
##                        self._master_result_dict.items():
##
##                self._html_output = self._html_output + \
##                r"<td  width=25%font-size='1'  >" + master_keys + \
##                r"</td>"
##
##                for child_keys, child_values in master_items.iteritems():
##
##                    platforms = master_items["PLATFORM"].copy()
##
##                    cell_value = str()
##                    print child_values
##                    for item in child_values:
##                        #if len(child_values) > 1 and not isinstance(item, types.InstanceType):
##                            print type(item)
##                            counter = 0
##                            if item.__class__.__name__ == "TestResults":
##                                print platforms.pop[counter]
##                                print platforms.pop()
##
##                                test_oracle[master_keys] = item._results
##                                counter = counter + 1
##                            cell_value = cell_value + str(item) + "; "
####                        else:
####                            cell_value = item
##                    self._html_output = self._html_output + \
##                        r"<td  width=25%font-size='1'  >" + \
##                            str(cell_value) + r"</td>"
##
##                self._html_output = self._html_output + \
##                        r"</tr>"
##
####
####                self._html_output = self._html_output + \
####
####                    r"<td  width=25%>" + master_keys + r"</td>"
####
####
####            self._html_output = self._html_output + \
####                    r"</tr>"
##
##            fHandle.write(self._html_output)
##
##            self._html_output = self._html_output + r"</table>"
##            self._html_output = self._html_output + \
##                        r"<a href=\"#results\">Test Results</a>"
##
##
##            self._html_output = self._html_output + r"</body></html>"
##            fHandle.close()

    except Exception, errormsg:
        print "Script errored!"
        print "Error message: %s" % errormsg
        print "Traceback:"
        import traceback
        traceback.print_exc()
        traceback.print_exception()
        traceback.print_stack()

if __name__ == '__main__':
    try:
        os.chdir(r"D:\Tools_Automation")
        sendmail_object = SendMail()
        messenger_object = Messenger(
            os.path.abspath(
                        r"Framework\CUPCAKE\data\json\constructor_data.json"),
            os.path.abspath(
                        r"Framework\CUPCAKE\data\json\vms_data.json"),
            os.path.abspath(
                        r"Framework\CUPCAKE\data\json\product_data.json"),
            os.path.abspath(
                        r"Framework\CUPCAKE\data\json\os_data.json"))

        fHandle = open(os.path.abspath(
                    r"Framework\CUPCAKE\data\pickle\messenger_pickle_file.pkl"),
                    'wb')
        pickle.dump(messenger_object._messenger_data, fHandle)
        fHandle.close()

##        vm_object = VMManager(
##            os.path.abspath(
##                    r"Framework\CUPCAKE\data\pickle\messenger_pickle_file.pkl"),
##            os.path.abspath(
##                    r"Framework\CUPCAKE\logs\vmmanager\vmmanager.log"))

        print "\nFinished performing tests on targeted OS"

        print "\nParsing results from all platforms"
        messenger_object.parse_result_files()
        messenger_object.prepare_master_results()
        #messenger_object.print_master_results()
        messenger_object.prepare_oracle()
        #messenger_object.get_max_col_size()
        messenger_object.prepare_oracle_html_report()
        #print messenger_object._master_result_dict

        print "Sending email with results and attachments... ",
        sendmail_object.sendEmail(hostName, sendMailToList, sendMailFromID,
                                subject, messenger_object._html_output)

    except Exception, errormsg:
        print "Script errored!"
        print "Error message: %s" % errormsg
        print "Traceback:"
        import traceback
        traceback.print_exc()