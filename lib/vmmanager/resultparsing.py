#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Akash_Bhatt
#
# Created:     12-06-2012
# Copyright:   (c) Akash_Bhatt 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import xml.etree.ElementTree as xml

output_directory = r"D:\\Output"
scriptDir = r'D:\\Builds'

dictNames = {
    "Windows-XP-5.1.2600-SP3": 'Windows XP Pro x86 SP3',
    "Windows-2003Server-5.2.3790-SP2": 'Windows XP Pro x64 SP2',
    "Windows-7-6.1.7600": 'Windows 7 Home Basic x86',
    "Windows-7-6.1.7601-SP1": 'Windows 7 Pro SP1 x64',
    "Windows-2008ServerR2-6.1.7601-SP1": 'Windows 2008 R2 x64 SP1',
    "Windows-XP-5.1.2600-SP3": 'Windows XP x86 SP3',
    }
global bvt_flag

bvt_flag = "PASS"

def getTestCaseNameList(xmlResultFile):
    try:
        testCaseNamesList = []
        tree = xml.parse(xmlResultFile)
        root = tree.getroot()
        for node in root.getchildren():
            if 'OS'==node.tag:
                continue
            else:
                testCaseNamesList.append(node.tag)
        return testCaseNamesList
    except Exception,e:
        print e

def startResultParsing(xmlResultFile):
    try:
        testCaseNamesList = getTestCaseNameList(xmlResultFile)
        ver_file = open( scriptDir+r"\32bit\ver_file.txt", 'r')
        version_number_in_zip = ver_file.read()
        ver_file.close()
        htmlText="<html><body><center>\
        <table cellspacing='0' cellpadding='5' border='2' style='empty-cells:show;' align='center'>\
        <tr bgcolor='#B30626'>\
        <td align='center' colspan='"+ str(len(testCaseNamesList)+1)+ "'>\
        <font face='calibri' size=3 color='#FFFFFF' align='center'>\
        <b>Stinger v12 "+version_number_in_zip+" aBVT Test Results</b>\
        </td>\
        </tr>"
        htmlText+="<tr bgcolor='#B30626'>\
        <td><font face='calibri' size=2 color='#FFFFFF'><b>Operating System </b></td>"
        for test in testCaseNamesList:
            htmlText+="<td align='center'><font face='calibri' size=2 color='#FFFFFF'><b>"+str(test)+"</b></td>"
        return htmlText
    except Exception,e:
        print e

def addResults(xmlResultFile, htmlText):
    tree=xml.parse(xmlResultFile)
    OS = tree.find('OS').text
    htmlText+="<tr><td bgcolor='#808080' align='left'><font face='calibri' size=2 color='#FFFFFF'><b>"+ str(OS) +"</b></td>"
    for test in getTestCaseNameList(xmlResultFile):
        result = tree.find(test).text
        if result == "PASS":
            htmlText+="<td align='center'><font face='calibri' size=2 color='#008000'><b>"+ result +"</b></td>"
        elif result == "FAIL":
            global bvt_flag
            bvt_flag = "FAIL"
            htmlText+="<td align='center'><font face='calibri' size=2 color='#FF0000'><b>"+ result +"</b></td>"
        else:
            htmlText+="<td align='center'><font face='calibri' size=2 color='#0000A0'><b>"+ result +"</b></td>"
    htmlText += "</tr>"
    return htmlText

def addSkippedResults(OS, htmlText, numberOfTestCases):
    htmlText+="<tr><td bgcolor='#808080' align='left'><font face='calibri' size=2 color='#FFFFFF'><b>"+ str(OS) +"</b></td>"
    for i in range(0, numberOfTestCases):
        htmlText+="<td align='center'><font face='calibri' size=2 color='#B30626'><b> SKIPPED </b></td>"
    htmlText+="</tr>"
    return htmlText

def finaliseResults(htmlText):
    htmlText+="</table></html>"
    return htmlText

def consolidatedResult(xmlResultFilesList, expectedOSList):
    try:
        actualOSList=[]
        if xmlResultFilesList:
            htmlText = startResultParsing(xmlResultFilesList[0])
            testCaseNamesList = getTestCaseNameList(xmlResultFilesList[0])
            numberOfTestCases = len(testCaseNamesList)
            for xmlResultFile in xmlResultFilesList:
                print "Parsing XML file " + xmlResultFile
                tree=xml.parse(xmlResultFile)
                actualOSList.append(tree.find('OS').text)
                htmlText = addResults(xmlResultFile, htmlText)
            if actualOSList != expectedOSList:
                for listElement in expectedOSList:
                    if listElement in actualOSList:
                        continue
                    else:
                        htmlText = addSkippedResults(listElement, htmlText, numberOfTestCases)
            htmlText = finaliseResults(htmlText)
            res_file = open(os.path.join(output_directory, os.listdir(output_directory)[0]),'w')
            res_file.write("===RESULT:BVT_RESULT:"+bvt_flag.upper())
            res_file.close()
            return htmlText
        else:
            return False
    except Exception,e:
        return str(e)