
# see https://wiki.openstreetmap.org/wiki/Key:start_date#Formatting 
# for start_date syntax

from vbFunctions import *

def parseStartDateValue(strDate, returnSameForUnparsed=True):

    strResult = ""
    strModifier = ""
    fn_return_value=""
    myRegExp = RegExp()
    if strDate == '':
        return fn_return_value
    #Julian Calendar prefix
    #just ignore it.
    if Left(strDate, 2) == 'j:':
        strDate = Mid(strDate, 3)
    #Modifiers
    if Left(strDate, 1) == '~':
        strDate = Mid(strDate, 2)
    if Left(strDate, 7) == 'before ':
        strDate = Mid(strDate, 8)
    #we do not need "mid", because we use a middle of the interval anyway.
    if Left(strDate, 4) == 'mid ':
        strDate = Mid(strDate, 5)
    if Left(strDate, 6) == 'early ':
        strDate = Mid(strDate, 7)
        strModifier = 'early'
    if Left(strDate, 5) == 'late ':
        strDate = strDate[5:len(strDate)]
        strModifier = 'late'
    #C18
    myRegExp.Pattern = '^C[0-9]{2}$'
    if myRegExp.Test(strDate):

        strDate = str(int(Mid(strDate, 2)) - 1)   + '50'
    #1234
    myRegExp.Pattern = '^[0-9]{4}$'
    if myRegExp.Test(strDate):
        strResult = strDate
    else:
        #1234..4321
        myRegExp.Pattern = '^[0-9]{4}\\.\\.[0-9]{4}$'
        if myRegExp.Test(strDate):
            strResult = Left(strDate, 4)
        else:
            #1234 - 4321
            myRegExp.Pattern = '^[0-9]{4}\\s?[-]\\s?[0-9]{4}$'
            if myRegExp.Test(strDate):
                strResult = Left(strDate, 4)
            else:
                #1990s
                myRegExp.Pattern = '^[0-9]{3}0s$'
                if myRegExp.Test(strDate):
                    select_variable_0 = strModifier
                    if (select_variable_0 == 'early'):
                        strResult = Left(strDate, 3) + '2'
                    elif (select_variable_0 == 'late'):
                        strResult = Left(strDate, 3) + '7'
                    else:
                        strResult = Left(strDate, 3) + '5'
                else:
                    myRegExp.Pattern = '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
                    if myRegExp.Test(strDate):
                        strResult = Left(strDate, 4)
                    else:
                        if returnSameForUnparsed:
                            strResult = strDate
                        else:
                            strResult = ""                         
                        
    fn_return_value = strResult
    return fn_return_value
