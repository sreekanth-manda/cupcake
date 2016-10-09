#-------------------------------------------------------------------------------
# Name:        vmmanager.py
# Purpose:
#
# Author:      Sreekanth Manda
#
# Created:     15/11/2013
# Copyright:   (c)
# Licence:     GPL
#-------------------------------------------------------------------------------

import sys
import os
import re
import zipfile
import shutil
import threading
import time
import datetime
import logging
import cPickle as pickle

#import from framework
from .threadpool_manager import ThreadPool, NoResultsPending, WorkRequest, \
    makeRequests
from vmrunhandler import VMRun

#Initializing logger
from Framework.CUPCAKE.lib.utils.logger import Logging
logger_object = Logging(r"Framework\CUPCAKE\logs\CUPCAKE.log")

class VMManager:

    def __init__(self, pickle_file_path, log_file_path):
        """
        """
        logger_object.create_log("info","CUPCAKE initializing VMManager")
        self._pickle_file_path = pickle_file_path
        self._log_file_path = log_file_path
        self._messenger_dict = {}
        self._vms = {}
        logger_object.create_log("info","CUPCAKE setting max threads to 5")
        self._MAX_THREADS = 5
        self.run()

    def run(self):
        logger_object.create_log("info","CUPCAKE running VMManager")
        self.unpickler()
        self.prepare_vms()
        self.initiate_thread()

    def unpickler(self):
        try:
            logger_object.create_log("info",
                                "CUPCAKE unpickling messenger unit data")
            logger_object.create_log("info","CUPCAKE opening pickle file " + \
                                self._pickle_file_path)
            fHandle = open(self._pickle_file_path, 'rb')
            self._messenger_dict = pickle.load(fHandle)
            fHandle.close()
        except WindowsError as exception:
            logger_object.create_log("error",
            "CUPCAKE encountered error " + str(exception) + \
            "in vmmanager.unpickler")
            print str(exception)

    def prepare_vms(self):
        logger_object.create_log("info","CUPCAKE retrieving VM details from " +\
                            "messenger unit pickle file")
        self._vms = self._messenger_dict['vm_info']

    def GetDataFromFile(field,delimiter,filePath):
        """Retrieves data from a file for a given field and the delimiter the
        file uses, Returns "not found" if field not present in file"""
        print "Trying VMrun command again"
        try:
            file = open(filePath,'r')
            pattern = field+delimiter
            value = 'not found'
            for line in file:
                match=re.search(pattern,line)
                if match:
                    value = line[match.end():]
                    value = Strip(value,"\n")
                    break
            file.close()
            return Strip(value," ")
        except Exception as e:
            return str(e)

    def Strip(str,char):
        """Strips the given string if the given character is present"""
        if str[-1] == char:
            return Strip(str[:-1],char)
        elif str[0] == char:
            return Strip(str[1:],char)
        else:
            return str

    def PrepareFolders(folderPath):
        print "Deleting files inside.. " + folderPath
        filesList = os.listdir(folderPath)
        for file in filesList:
            if os.path.isfile(folderPath + "\\" + file):
                os.remove(folderPath + "\\" + file)

    def initiate_thread(self):
        threadPool = ThreadPool(self._MAX_THREADS)

        for vm_settings in self._vms:
            vm_details =  self._vms[vm_settings]

            threadPool.putRequest(
                                WorkRequest(
                                    self.runVM,
                                    args = [vm_details, vm_settings]
                                )
                            )
        while True:
            try:
                threadPool.poll()
                active_threads = threading.activeCount() - 1
                if active_threads < self._MAX_THREADS:
                    threadPool.createWorkers(self._MAX_THREADS - active_threads)

                if active_threads > self._MAX_THREADS:
                    threadPool.dismissWorkers(active_threads - self._MAX_THREADS)

            except NoResultsPending:
                threadPool.dismissWorkers(threading.activeCount() - 1)
                break

    def runVM(self, vm_details, vm_settings):

        isVMRunning = True

        #print vm_settings
        vmrun = VMRun(vm_details)

        print "\nStarting VM " + vm_settings
        vmRunResult =  vmrun.start()

        print "\nReverting to snapshot " + vm_details['base_snap'] + " in " + \
                                            vm_settings
        vmRunResult = vmrun.revertToSnapshot(vm_details['base_snap'])

        print "\nResuming VM after revert " + vm_settings
        vmRunResult =  vmrun.start()

        print "\nCreating Tools_Automation Directory in VM " + vm_settings
        vmRunResult = vmrun.createDirectoryInGuest("C:\Tools_Automation")

##        print "\nCreating logFile Directory in VM " + vm_settings
##        vmRunResult = vmrun.createDirectoryInGuest("C:\StingerV11_aBVT\logFile")

        print "\nCopying framework to VM " + vm_settings
        vmRunResult = vmrun.copyFileFromHostToGuest(r"D:\Tools_Automation",
                                            r'C:\Tools_Automation')
##
##        print "\nCopying scripts to VM " + vm_settings
##        vmRunResult = vmrun.copyFileFromHostToGuest(scriptFilesDirectory,
##                                            r'C:\StingerV11_aBVT')

        print "\nExecuting tests in " + vm_settings +", Please wait"
        vmRunResult = vmrun.runProgramInGuest(r"C:\Python27\python.exe", "nb",
        r"C:\Tools_Automation\Framework\CUPCAKE\lib\vmmanager\serializer.py",
            vm_settings)

        time_difference = 0
        start_time = datetime.datetime.now()

        while time_difference <= 7200:
            #Checking for file existence in VM
            if (vmrun.fileExistsInGuest(os.path.abspath(
                    'C:\Tools_Automation\Framework\CUPCAKE\data\Done.txt'))):
                print "\nFound Done.txt in " + vm_settings
##                print "\nCopying result.xml from " + vm_settings + " to host"
##                vmRunResult = vmrun.copyFileFromGuestToHost(
##                                "C:\\StingerV11_aBVT\\result.xml",
##                                tempFolderPath + "\\" + vm_settings + ".xml")
##                print "\nCopying result.log from " + vm_settings + " to host"
##                vmRunResult = vmrun.copyFileFromGuestToHost(
##                                "C:\\StingerV11_aBVT\\logFile\\result.log",
##                                zipFilesPath + "\\" + vm_settings + ".log")
                break
            else:
                #print "\nno Done.txt found in " + vm_settings
                #Checking whether VM is running or not
                runningVMsList = vmrun.list_running_vm()
##                print runningVMsList
##                print vm_details['vmx_path']
                if vm_details['vmx_path'] in runningVMsList:
                    #Sleep if VM is running
                    time.sleep(30)
                    revised_time = datetime.datetime.now()
                    time_delta_obj = revised_time - start_time
                    time_difference = time_delta_obj.seconds
                else:
                    isVMRunning = False
                    print "VM " + vm_settings + " is not running, " + \
                            "probably in paused/powered off state\n"
                    break

        if isVMRunning == False:
            print "Starting VM operation again to run aBVT tests"
            self.runVM(vm_details, vm_settings)
        else:
            if time_difference == 7200:
                print "Exiting script as it's been running for ~2hrs"

            print "Turning off VM " + vm_settings
            #vmrun.stop('soft')

        print "\nCopying result pickle file from guest to host..."
        vmRunResult = vmrun.copyFileFromGuestToHost(
            r"C:\Tools_Automation\Framework\CUPCAKE\data\results",
            os.path.abspath(r"Framework\CUPCAKE\data\results\\" + vm_settings))

##if __name__ == '__main__':
##    try:
##        startTime = datetime.datetime.now()
##        print "aBVT started at : " + str(startTime) + "\n"
##        self._MAX_THREADS = 5
##        threadPool = ThreadPool(self._MAX_THREADS)
##        PrepareFolders(tempFolderPath)
##        PrepareFolders(notDonePath)
##        if os.path.exists(zipFilesPath):
##            shutil.rmtree(zipFilesPath, ignore_errors=True)
##        os.mkdir(zipFilesPath)
##
##
##        expectedOSList = []
##        resultFiles =[]
##        print "aBVT tests completed on all platforms\n"
##        if os.path.exists (scriptDir + r"\32bit\ver_file.txt"):
##            ver_file = open( scriptDir + r"\32bit\ver_file.txt", 'r')
##            version_number_in_zip = ver_file.read()
##            ver_file.close()
##        elif os.path.exists (scriptDir + r"\64bit\ver_file.txt"):
##            ver_file = open( scriptDir + r"\64bit\ver_file.txt", 'r')
##            version_number_in_zip = ver_file.read()
##            ver_file.close()
##
##        print "Parsing XML files and consolidating results... \n",
##        if os.listdir(tempFolderPath):
##            print "Creating email attachment (zip file) with log files ... " ,
##            attachmentZipName = "Stingerv12_"+ version_number_in_zip + "_" + \
##                                bit_info + "_logs.zip"
##            attachmentZip = zipfile.ZipFile(os.path.join(zipFilesPath, \
##                                attachmentZipName), mode='w')
##
##            for file in os.listdir(zipFilesPath):
##                if attachmentZipName == file:
##                    continue
##                else:
##                    attachmentZip.write(os.path.join(zipFilesPath,file),
##                                            arcname=file)
##            for file in os.listdir(notDonePath):
##                if attachmentZipName==file:
##                    continue
##                else:
##                    attachmentZip.write(os.path.join(notDonePath,file),
##                                            arcname=file)
##
##            attachmentZip.close()
##            print "Done!"
##
##            #Generating expected OS list
##            for osName in VMs.iterkeys():
##                osName = osName.strip('STI-')
##                osName = osName.strip('.xml')
##                expectedOSList.append(osName)
##
##            #Adding result XMLs file to resultFiles for parsing
##            for resultFileName in os.listdir(tempFolderPath):
##                resultFiles.append(tempFolderPath + "\\" + resultFileName)
##
##            htmlText = resultParsing.consolidatedResult(resultFiles,
##                                                            expectedOSList)
##            mailObj = SendEmail.SendMail()
##            contentTemp = htmlText
##
##            subject = "Stinger v12 12.1.0."+ version_number_in_zip + bit_info +\
##                         "aBVT Results"
##
##            print "Sending email with results and attachments... ",
##            mailObj.sendEmail(hostName, sendMailToList, sendMailFromID,
##                                    subject, contentTemp,
##                                    [os.path.join(zipFilesPath,
##                                    attachmentZipName)])
##            print "done"
##            finishTime = datetime.datetime.now()
##            print "aBVT finished at : " + str(finishTime)
##        else:
##            print "No XMLs found to publish results, aBVT process completed"
##            print "Creating zip file with log files ... " ,
##            attachmentZipName = "Stingerv12_"+ version_number_in_zip + "_" + \
##                            bit_info + "_logs.zip"
##            attachmentZip = zipfile.ZipFile(os.path.join(notDonePath, \
##                            attachmentZipName), mode='w')
##
##            for file in os.listdir(notDonePath):
##                if attachmentZipName==file:
##                    continue
##                else:
##                    attachmentZip.write(os.path.join(notDonePath,file), arcname=file)
##
##            attachmentZip.close()
##            print "Done"
##            mailObj = SendEmail.SendMail()
##            htmlText="<html><body>\
##                        <font face='calibri' size=3 color='#FF0000' align='center'>\
##                        <b>BVT process completed, No XMLs found to publish results.\
##                        <b>Refer to the attached log files for all OS completed for specific errors</b>\
##                        </body></html>"
##
##            subject = "Stinger v12 12.1.0"+ version_number_in_zip + bit_info + "aBVT Results"
##
##            print "Sending email with results and attachments... ",
##            mailObj.sendEmail(hostName, sendMailToList, sendMailFromID,
##                                    subject, htmlText,
##                                    [os.path.join(notDonePath, attachmentZipName)])
##            print "Done"
##            finishTime = datetime.datetime.now()
##            print "aBVT finished at : " + str(finishTime)
##    except Exception, e:
##        print "The following exception was caught in module 'Main': "+ type(e).__name__+ " : " + str(e)