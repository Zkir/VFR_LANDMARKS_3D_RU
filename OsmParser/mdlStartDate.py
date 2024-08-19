
# see https://wiki.openstreetmap.org/wiki/Key:start_date#Formatting 
# for start_date syntax

from vbFunctions import *
# we really extract just YEAR from the start date.
# and it would be nice to extract also interval, to recieve smth like 1978 ± 2

#wrapper -- the code expects, that result is string, 
# and original value is returned if unable to parse
def parseStartDateValue(strDate:str) -> str:
    y = parseStartDate(strDate)
    if y is not None:
        s = str(y)
    else:
        s = strDate
    return s


# core function
# return integer if parsed and None if not!
def parseStartDate(strDate:str) -> int:

    strResult = ""
    strModifier = ""
    myRegExp = RegExp()
    
    # empty
    if strDate == '':
        return None 
    
          
    #interval XX..YY 
    # XX ans YY can be any tokens (magic!)
    if ".." in strDate:
        tokens = strDate.split("..",1) # 1 equals 2 in python. split in two!
        s1 = parseStartDateValue(tokens[0].strip())
        s2 = parseStartDateValue(tokens[1].strip())
        #print("INTERVAL: " ,int(s1), int(s2))
        try:
            strResult = (int(s1)+int(s2))/2 
           
            strResult = int(strResult)
        except:
            strResult = None          
        return strResult
        
    #1941-1945
    myRegExp.Pattern = '^[0-9]{4}\\s?[-]\\s?[0-9]{4}$'
    if myRegExp.Test(strDate):
        y1 = int(Left(strDate, 4))
        y2 = int(Right(strDate, 4))
        return  int((y1+y2)/2)
  
    #BC 
    myRegExp.Pattern = r'^.*\s?BC$'
    if myRegExp.Test(strDate):
        strDate = strDate[:-3].strip()
             
        strResult = parseStartDateValue(strDate)
        try:
            strResult= -int(strResult) 
        except:
            strResult= None 
            
        return strResult 
  
    #Julian Calendar prefix
    #just ignore it.
    #just 13 days difference is insignificant
    if Left(strDate, 2) == 'j:':
        strDate = Mid(strDate, 3)

    
    #Modifiers
    if Left(strDate, 1) == '~':
        strDate = Mid(strDate, 2)
        
    if Left(strDate, 7) == 'before ':
        strDate = Mid(strDate, 8)
        
    if Left(strDate, 6) == 'after ':
        strDate = Mid(strDate, 7)    
    
    #we do not need "mid", because we use a middle of the interval anyway.
    if Left(strDate, 4) == 'mid ':
        strDate = Mid(strDate, 5)
    if Left(strDate, 6) == 'early ':
        strDate = Mid(strDate, 7)
        strModifier = 'early'
    if Left(strDate, 5) == 'late ':
        strDate = strDate[5:len(strDate)]
        strModifier = 'late'
    
    
    #1234
    myRegExp.Pattern = '^[0-9]{4}$'
    if myRegExp.Test(strDate):
        strResult = strDate
        return int(strResult)
    
    #1234-12
    myRegExp.Pattern = r'^[0-9]{4}-[0-9]{2}$'
    if myRegExp.Test(strDate):
        strResult = Left(strDate,4)
        return int(strResult)
    
    #1234-12-07
    myRegExp.Pattern = '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    if myRegExp.Test(strDate):
        strResult = Left(strDate, 4)
        return int(strResult)


    #C18
    myRegExp.Pattern = '^C[0-9]{2}$'
    if myRegExp.Test(strDate):
        if strModifier == "early":
            strResult = str(int(Mid(strDate, 2)) - 1)   + '10'
        elif strModifier == "late":
            strResult = str(int(Mid(strDate, 2)) - 1)   + '90'
        else: 
            strResult = str(int(Mid(strDate, 2)) - 1)   + '50'
        return int(strResult)    



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
        
        return int(strResult)
 
                     
    return None

def psd(s):
    y = parseStartDateValue(s)
    try: 
        y=int(y)
    except:
        pass
    print(s + " --> "+str(y))
    return y

def tests():
    print("Tests:")
    
    #exect dates 
    assert psd("2010") == 2010                   # where the year is known, but no more
    assert psd("0897") == 897                    #(for 897 CE)
    assert psd("1848-07") == 1848                # where the year and month are known
    assert psd("2010-03-31") == 2010             # for where the full date is known, using the format yyyy-mm-dd
    
    #approximations
    assert psd("~1855") == 1855                  # (some time around 1855)
    assert psd("1860s") == 1865                  # (during the 1860s (i.e 1860 → 1869 inclusive) ==
    assert psd("~1940s") == 1945                 # (probably during the 1940s)
    assert psd("480 BC") == -480                 # (for something that happened in that year)
    assert psd("before 1855") ==  1855           # (during 1854 or before)
    assert psd("before 1910-01-20") == 1910      # (before a specific date - possibly when a photo was taken)
    assert psd("after 1823") == 1823             # (after 1 January 1823 - possibly based on the year in which a map was produced)
    assert psd("C18") == 1750                    # (during the 18th century)
    assert psd("mid C14") == 1350                # (some time during the middle of the 14th century)
    assert psd("late 1920s") == 1927             #   
    assert psd("~C13") == 1250                   # (probably in the 13th century)
    assert psd("1914..1918") == 1916             # indicates some time during WW1.
    assert psd("1914-1918") == 1916              # non standart, but used too frequently to ignore
    assert psd("2008-08-08..2008-08-24") == 2008 # indicates some time during the Beijing Olympics.
    assert psd("C13..C15") == 1350               #
    assert psd("mid C17..late C17") == 1670      #
    assert psd("j:1918-01-31") == 1918           # (a date using the Julian calendar, equivalent to 1918-02-13 in the Gregorian calendar)
    #assert psd("jd:2455511") == #(Using the Julian day system, equivalent to 2010-11-10 in the Gregorian calendar)
    assert psd("753 BC..476") == -138            # ancient Rome period
    assert psd("") == ""                         # blank value is still blank
    assert psd("Abrakadabra") == "Abrakadabra"   # the original string if unable to parse
    assert psd("Abrak..adabra") == "Abrak..adabra"   # the original string if unable to parse    
   
    print("Tests OK")
    
    
if __name__ == '__main__':
    tests()    
