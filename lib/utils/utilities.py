#-------------------------------------------------------------------------------
# Name:        CupCake Utilities
# Purpose:     General Utilities used in developing tools automation
#
# Author:      Sreekanth Manda
# Version:     1.0
# Created:     20/08/2013
# Copyright:   (c) Sreek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""This module contains all utility functions"""

import os
import sys
import shutil
from logger import *
import glob
import wmi
import psutil
#import pychecker.checker

__version__ = "$Revision: $"
__author__ = "Sreekanth Manda"

class Utilities():

    """Contains all the required utility functions for performing automation
    tasks"""

    #Class member functions
    #Function to initialize class variables
    def __init__(self, exit_code, actual_result, sample_running):
        Utilities._exit_code = exit_code
        Utilities._actual_result = actual_result
        Utilities._sample_running = sample_running

    #function to copy files from source to destination
    @classmethod
    def copy_files(cls, source_path, dest_path):

        """This function is used to copy files from source to dest with
        logging"""
        try:
            Logging.create_log("info","Checking if " + dest_path + \
                        " destination directory exists")
            if os.path.exists(dest_path):
                Logging.create_log("error", dest_path + " destination path " +\
                                    "exists")
                Logging.create_log("info","Deleting " + dest_path + \
                            " destination directory")
                shutil.rmtree(dest_path)
                Logging.create_log("info", "Copying files from source " + \
                                    source_path + " to destination " + \
                                    dest_path)
            if os.path.exists(source_path):
                shutil.copytree(source_path, dest_path)
                Logging.create_log("info","Copy completed")
            else:
                Logging.create_log("error", source_path + " source directory is\
                                     not available")
                Logging.create_log("info","Exiting from script with code 1")
                sys.exit(1)

        except WindowsError as windows_error:
            Logging.create_log("error", "Exception in copy_files method : " + \
                        str(windows_error))
            sys.exit(1)

    #Function to parse scan report for passed string
    @classmethod
    def parse_scan_report(cls, report_file, string_to_parse):

        """This function is used to parse the file to search of string and
        return pass or fail based on the search result"""
        try:
            file_handle = open(report_file, 'r')
            file_lines = file_handle.read()
            matching_string = file_lines.find(string_to_parse)
            if(matching_string != -1):
                cls._actual_result = "PASS"
            else:
                cls._actual_result = "FAIL"
        except WindowsError as windows_error:
            Logging.create_log("error", "The following exception was caught in \
                        method 'parse_scan_report': " + str(windows_error))

    #Function delete files from the specified directory
    @classmethod
    def delete_files(cls, files_path):

        """This function is used to delete files from specified dir with
        logging"""
        try:
            if os.path.exists(files_path):
                files_path = files_path + "\\*.*"
                files_to_delete = glob.glob(files_path)
                for file_delete in files_to_delete:
                    if os.path.exists(file_delete):
                        os.remove(file_delete)
        except WindowsError as windows_error:
            Logging.create_log("error", "The following exception was caught in \
                        module 'deleteFiles': " + str(windows_error))

    #Method to move files to a specified folder with logging
    @classmethod
    def move_files(cls, source_path, path_to_move, file_type):

        """This method is used to move files from source and destionation"""
        try:
            Logging.create_log("info","Moving files " + file_type + \
                                    " from the path " + source_path)
            if not os.path.exists(path_to_move):
                os.mkdir(path_to_move)

            source_path = source_path + "\\" + file_type
            files_to_move = glob.glob(source_path)
            for file_to_move in files_to_move:
                if os.path.exists(file_to_move):
                    shutil.move(file_to_move, path_to_move)
        except WindowsError as windows_error:
            Logging.create_log("error", "The following exception was caught in \
                        module 'deleteFiles': " + str(windows_error))

    #Function to run a program
    @classmethod
    def run_program(cls, program_path, program_name, cmd_options, script_path):

        """This function is used to run a program with supplying program path,
        name, and, any command line options. Also, need to provide script path
        to use to return once the program is finished"""
        try:
            os.chdir(program_path)
            if cmd_options:
                Logging.create_log("info","Running " + program_name + \
                                        " with cmd options : " + cmd_options)
                program_to_run = program_path +  "\\" + program_name + " " + \
                                    cmd_options
            else:
                program_to_run = program_path + "\\" + program_name
            Utilities._exit_code = os.system(program_to_run)
            os.chdir(script_path)
            Logging.create_log("info","Running " + program_name + \
                                " is completed with exitcode : " + \
                                str(Utilities._exit_code))
        except WindowsError as windows_error :
            Logging.create_log("error","Exception in run_program method " + \
                                str(windows_error))

    #Function to verify a sample or process is active or not
    @classmethod
    def is__sample_running(cls, sample_name):

        """Function to verify a sample or process is active or not"""
        try:
            wmi_object = wmi.WMI()
            found_samples = []

            process_list = wmi_object.Win32_Process()

            for running_process in process_list:
                if running_process.name == sample_name:
                    found_samples.append(sample_name)

            if sample_name in found_samples:
                Logging.create_log("info", sample_name + " is running")
                Utilities._sample_running = True
            else:
                Logging.create_log("error", sample_name + " is not running")
                Utilities._sample_running = False
        except WindowsError as windows_error :
            Logging.create_log("error","Exception in run_program method " + \
                                str(windows_error))

    #Function to run specified sample
    @classmethod
    def run_sample(cls, sample_path):

        """This method is used to run sample from the specified path"""
        try:
            Logging.create_log("info","Starting samples from " + sample_path)
            directory_contents = os.listdir(sample_path)
            for file_in_dir in directory_contents:
                file_in_dir = file_in_dir.rstrip()
                if os.path.exists(sample_path + "\\" + file_in_dir):
                    os.startfile(sample_path + "\\" + file_in_dir)
            Logging.create_log("info","Done!")

            Logging.create_log("info","Verify sample(s) running or not")
            directory_contents = os.listdir(sample_path)
            for file_in_dir in directory_contents:
                file_in_dir = file_in_dir.rstrip()
                cls.is__sample_running(file_in_dir)
        except WindowsError as windows_error :
            Logging.create_log("error","Exception in run_program method " + \
                        str(windows_error))

    #Function to kill a process
    @classmethod
    def kill_sample(cls, sample_name):
        """This method is used to kill a running sample using sample name"""

        try:
            Logging.create_log("info", "Killing sample " + sample_name)
            for process in psutil.process_iter():
                if process.name == sample_name:
                    if process.status == psutil.STATUS_RUNNING:
                        try:
                            os.system("TASKKILL /F /IM \"" + sample_name + "\"")
                        except Exception as exp:
                            print "Process not available to kill"
        except WindowsError as windows_error :
            Logging.create_log("error","Exception in run_program method " + \
                        str(windows_error))
