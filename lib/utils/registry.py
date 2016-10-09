#-------------------------------------------------------------------------------
# Name:        registry
# Purpose:
#
# Author:      Akash_Bhatt
#
# Created:     08-11-2013
# Copyright:   (c) Akash_Bhatt 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""This module contains all registry handling utilities"""

class registry():

    """Contains all the registry utility functions for performing automation
    tasks"""

    #Class member functions
    @classmethod
    def AddSample(samplePath,valueName,Key,Sub_Key):
        """Adds provided sample to the registry"""
        if samplePath:
            samplePath="\""+samplePath+"\""
        else:
            samplePath="(value not set)"
        try:
            key = _winreg.OpenKey(Key, Sub_Key, 0, KEY_ALL_ACCESS)
        except:
            key = _winreg.CreateKey(Key, Sub_Key)
        _winreg.SetValueEx(key, valueName, 0, _winreg.REG_SZ, samplePath)
        _winreg.CloseKey(key)

    @classmethod
    def RemoveSample(valueName,Key,Sub_Key):
        """Removes a sample from the registry with the given name"""
        aReg = _winreg.ConnectRegistry(None,Key)
        targ = Sub_Key
        aKey = _winreg.OpenKey(aReg, targ, 0, _winreg.KEY_WRITE)
        _winreg.DeleteValue(aKey, valueName)
        _winreg.CloseKey(aKey)
        _winreg.CloseKey(aReg)