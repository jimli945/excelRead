import pandas as pd
from pandas import DataFrame
import numpy as np
import utils


class newCustExcel(object):
    def __init__(self, sheetpath="example.xlsx"):
        self.sheet = pd.read_excel(sheetpath, skiprows=1, sheet_name=None)
        self.tagLTE = self.sheet.get('LTE')

        tmp = self.tagLTE.drop([0])  # drop NaN row (the second row of Sub-Category(row3))
        tmp.reset_index(drop=True, inplace=True)  # reset index
        self.tagLTE = tmp
    #
    # def getDefaultValues(self):
    #     superUserDisplay = self.tagLTE["Superuser"][1:]
    #     superUserModify = self.tagLTE["Unnamed: 5"][1:]
    #     superUserModify = superUserModify.fillna(-1)
    #     tSuperUser = pd.concat([superUserDisplay, superUserModify], axis=1)
    #
    #     endUserDisplay = self.tagLTE["Enduser"][1:]
    #     endUserModify = self.tagLTE["Unnamed: 7"][1:]
    #     endUserModify = endUserModify.fillna(-1)
    #     tEndUser = pd.concat([endUserDisplay, endUserModify], axis=1)
    #
    #     defaultValue = self.tagLTE["Default Values"].drop([0])
    #     defaultSetting = pd.concat([tSuperUser, tEndUser, defaultValue], axis = 1)
    #     defaultSetting.columns = ['SupDis', 'SupModi', 'EndDis', 'EndModi','Default Values']
    #
    #     return defaultSetting
    #
    #     pass
    #
    # def getCustValues(self):
    #     superUserDisplay = self.tagLTE["Superuser.1"][1:]
    #     superUserModify = self.tagLTE["Unnamed: 10"][1:]
    #     superUserModify = superUserModify.fillna(-1)
    #     tSuperUser = pd.concat([superUserDisplay, superUserModify], axis=1)
    #
    #     endUserDisplay = self.tagLTE["Enduser.1"][1:]
    #     endUserModify = self.tagLTE["Unnamed: 12"][1:]
    #     endUserModify = endUserModify.fillna(-1)
    #     tEndUser = pd.concat([endUserDisplay, endUserModify], axis=1)
    #
    #     defaultValue = self.tagLTE["Default Values.1"].drop([0])
    #     custSetting = pd.concat([tSuperUser, tEndUser, defaultValue], axis=1)
    #     custSetting.columns = ['cSupDis', 'cSupModi', 'cEndDis', 'cEndModi', 'cDefault Values']
    #     print(custSetting)
    #     return custSetting

    def printSheet(self):
        # print(xlsx.sheet_names)

        # print(self.sheet)
        print(self.sheet.get("LTE").iloc[1])
        pass
    def newGetDefaultSetting(self, workSheet='LTE'):
        wSheet = self.sheet.get(workSheet)
        pd.set_option("display.max_columns", None)
        # defaultSheet = wSheet.loc[1:, 'Superuser':'Default Values']
        # defaultSheet = defaultSheet.fillna(-1)
        # below is to align the yes, YES, Yes, don't know why it's not consistent in customization sheet
        testSheet = wSheet.loc[1:, 'Superuser':'Default Values']
        testSheet = testSheet.drop(columns=[testSheet.columns[-1]])
        for c in testSheet.columns:
            testSheet[c] = testSheet[c].str.title()
        testSheet = testSheet.fillna(-1)
        tmp = wSheet.loc[1:, "Default Values"]
        tmp = tmp.fillna(-1)
        testSheet = pd.concat([testSheet, tmp], axis=1)
        # End
        defaultSheet = testSheet
        
        
        defaultSheet.columns = ['sDisplay', 'sModi', 'eDisplay', 'eModi', 'sDefaultValues']
        defaultSheet.reset_index(drop=True, inplace=True)
        return defaultSheet

    def newGetCustSetting(self, workSheet='LTE'):
        wSheet = self.sheet.get(workSheet)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)
        # custSheet = wSheet.loc[1:, 'Superuser.1':'Default Values.1']
        # custSheet = custSheet.fillna(-1)

        # below is to align the yes, YES, Yes, don't know why it's not consistent in customization sheet
        testSheet = wSheet.loc[1:, 'Superuser.1':'Default Values.1']    
        # print(testSheet)
        testSheet = testSheet.drop(columns=[testSheet.columns[-1]])
        for c in testSheet.columns:
            testSheet[c] = testSheet[c].str.title()
        testSheet = testSheet.fillna(-1)
        tmp = wSheet.loc[1:, "Default Values.1"]
        tmp = tmp.fillna(-1)
        testSheet = pd.concat([testSheet, tmp], axis=1)
        # End
        # print(testSheet)
        custSheet = testSheet
        # print(custSheet)
        custSheet.columns = ['sDisplay', 'sModi', 'eDisplay', 'eModi', 'sDefaultValues']
        custSheet.reset_index(drop=True, inplace=True)
        return custSheet
        pass
    
    def createLookupArray2(self, whichPD):
        whichPD = self.tagLTE["Sub-Category"]
        # print(whichPD)
        # Current index value = excel - 4
        MaxRow = len(whichPD.index)
        mask = whichPD.notnull()
        notNullofPD = whichPD[mask]
        # print(notNullofPD)
        tmpStr = []
        pre = 0
        firstItem = notNullofPD[0] # Get the first item
    
        for i in notNullofPD.index:
            if i == 0: # Skip first item
                pre = i
                name = firstItem # First category name
    
                continue
    
            now = i # next round i
            diff = now-pre # calculate how many items in pre category
            tmpStr = tmpStr + [name]*diff # Create array with pre category
            name = (whichPD.loc[i]) # Next category name
            pre = i # Record current i
    
        diff = MaxRow - pre # The last one category
        tmpStr = tmpStr + [name] * diff
        tmpStr = pd.Series(tmpStr)
        return tmpStr
    def _compareBetweenSheet(self,sheet1, sheet2):
        resultSheet = pd.DataFrame()
        for columns in list(sheet1.columns):
            mask = sheet1[columns] == sheet2[columns]
            resultSheet = pd.concat([resultSheet, mask], axis=1)
        return resultSheet

    def getDifferentItems(self, tag):
        print("Current Sheet:", tag)
        defaultSheet = self.newGetDefaultSetting(tag)
        custSheet = self.newGetCustSetting((tag))
        diffSheet = self._compareBetweenSheet(defaultSheet, custSheet)
        for c in diffSheet.columns:
            falseItem = utils.changedItem(diffSheet[c])
            print(c, ":", falseItem)





