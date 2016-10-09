#-------------------------------------------------------------------------------
# Name:        xml
# Purpose:     This class will be used for XML operations
#
# O.Author:    Akash Bhatt
# Maintainer:  Akash Bhatt
# Created:     08/11/2013
# Copyright:   (c) Akash Bhatt 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#Class with functions to be used for XML operations

"""This module is for XML operations"""

import xml.dom.minidom

class xml(object):

    #Class variable


    #Init the Class variable (if any)
    #def __init__(self, log_file_path):


    #Class member functions

    @classmethod
    def CheckXMLFormat(filePath):
        """CHECKS IF THE XML IS WELL FORMED, RETURNS TRUE IF IT IS"""
        try:
            parse(filePath)
            return True
        except Exception,e:
            print "%s not well formatted: %s" % (filePath,str(e))
            return False

    @classmethod
    def tagContentValidation(XMLFullPath,Tag_Name,Expected_Tag_Content):
        """Checks whether provided Tag_name has the provided Expected_Tag_Content
        or not by parsing the XML at XMLFullPath and returns True/False"""
    try:
        dom = xml.dom.minidom.parse(XMLFullPath)
        nodes = dom.getElementsByTagName(Tag_Name)
        for node in nodes:
            value = node.getAttribute("value")
            if(value==Expected_Tag_Content):
                return True
        return False
    except Exception as e:
        print e
        return False

    @classmethod
    def getTagContent(XMLFullPath,Tag_Name):
        """Returns the content in the provided Tag_name and
        False if Tag_Name does not exist in XML"""
    try:
        dom = xml.dom.minidom.parse(XMLFullPath)
        nodes = dom.getElementsByTagName(Tag_Name)
        for node in nodes:
            value = node.getAttribute("value")
            return value
        return False
    except Exception as e:
        print e
        return False

