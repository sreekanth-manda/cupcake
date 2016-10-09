#-------------------------------------------------------------------------------
# Name:        uiautomation.py
# Purpose:     Contains automation functions
#
# Author:      Sreekanth Manda
# Version:     1.0
# Created:     20/09/2013
# Copyright:   (c) Sreek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pywinauto
from pywinauto import timings

mainApp = None
applicationDialog = None
eulaDialog = None
updateDialog = None
prefDialog = None

class UIAutomation:

    def __init__(self):
        self._application_dialog = False

    def startProgram(self, programTitle, programPath):
        try:
            print "Starting application..."
            global mainApp
            mainApp = pywinauto.application.Application()
            mainApp.start_(programPath)
            global updateDialog
            global applicationDialog
            updateDialog = mainApp.window_(title_re = programPath + " Update")
            timings.WaitUntilPasses(60, 2, updateDialog.Exists)
            if updateDialog.Exists():
                if updateDialog['Static'].Texts():
                    dlgText = updateDialog['Static'].Texts()
                    updateDialog['Button2'].Click()
                    applicationDialog = mainApp.window_(title_re = programTitle)
                    timings.WaitUntilPasses(60, 2, applicationDialog.Exists)
                    if applicationDialog.Exists():
                        print programTitle + " Dialog found..."
                        self._application_dialog = True
            else:
                applicationDialog = mainApp.window_(title_re =programTitle)
                timings.WaitUntilPasses(60, 2, applicationDialog.Exists)
                if applicationDialog.Exists():
                    print programTitle + " Dialog found..."
                    self._application_dialog = True
        except Exception as exp:
            print str(exp)

    def initiateScan(self):
        print "Starting scan..."
        status = mainApp.applicationDialog["statu bar"].GetPartText(0)
        if (status == u'Ready'):
            mainApp.applicationDialog["tool bar"].Button(0).Click()
            eulaDialog = applicationDialog.window_(title_re = ".*License.*")
            mainApp.applicationDialog["RadioButton1"].Click()
            mainApp.applicationDialog["OK"].Click()

    def waitForScanComplete():
        status = mainApp.applicationDialog["statu bar"].GetPartText(0)
        while (True):
            if status == 'Ready':
                break;
            else:
                warningDialog = mainApp.window_(title_re = "Warning")
                timings.WaitUntilPasses(30, 2, warningDialog.Exists)
                if warningDialog.Exists():
                    if warningDialog['Cancel']:
                        warningDialog['Cancel'].Click()
                    elif warningDialog['OK']:
                        warningDialog['OK'].Click()
                else:
                    status = mainApp.applicationDialog["statu bar"].GetPartText(0)
                    continue
        print "Scan completed"

    def chkNewVersionDialog(programPath):
        print "Starting application..."
        mainApp = pywinauto.application.Application()
        mainApp.start_(programPath)
        global updateDialog
        updateDialog = mainApp.window_(title_re = "GetSusp Update")
        timings.WaitUntilPasses(30, 2, updateDialog.Exists)
        if updateDialog.Exists():
            if updateDialog['Static'].Texts():
                dlgText = updateDialog['Static'].Texts()
                updateDialog['Button2'].Click()
                return dlgText
            else:
                return None
        else:
            print "Update Dialog not found"
            return None

    def setPreferences():
        global prefDialog
        if applicationDialog.Exists():
            mainApp.applicationDialog["tool bar"].Button(3).Click()
            prefDialog = mainApp.window_(title_re = "Preferences")
            timings.WaitUntilPasses(60, 2, prefDialog.Exists)

    def submitSample():
        if prefDialog.Exists():
            if not prefDialog['Submit results to McAfee'].GetCheckState():
                prefDialog['Submit results to McAfee'].Check()
            prefDialog['OK'].Click()

    def dontSubmitSample():
        if prefDialog.Exists():
            if prefDialog['Submit results to McAfee'].GetCheckState():
                prefDialog['Submit results to McAfee'].UnCheck()
            prefDialog['OK'].Click()

