#Function to log errors, warnings, info messages etc

"""This module is for logging"""

import logging
import traceback

class Logging(object):

    #Class variable
    log_file_path = None

    #Init the log path
    def __init__(self, log_file_path):
        Logging.log_file_path = log_file_path

    #Class member functions
    @classmethod
    def create_log(self, level, message):
        """Method to enable logging"""
        try:
            #print "Log file name :" + Logging.log_file_path
            logging.basicConfig(filename = Logging.log_file_path, level=logging.DEBUG)
            if level.lower() == 'debug':
            	logging.debug(message)
            elif level.lower() == 'info':
            	logging.info(message)
            elif level.lower() == 'warning':
            	logging.warning(message)
            elif level.lower() == 'error':
            	logging.error(message)
            elif level.lower() == 'critical':
            	logging.critical(message)
            else:
            	logging.info("Log could not be created because the supplied \
                    level name: "+ level +" is not a valid level name")
        except WindowsError as windows_error:
            print("Log could not be created due to WindowsError \
                            exception: " + windows_error)
        except Exception, e:
            print("Log could not be created due to unhandled \
                            exception: " + str(e))
