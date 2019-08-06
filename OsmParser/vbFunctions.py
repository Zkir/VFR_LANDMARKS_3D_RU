#=======================================================================================================================
# VB6 runtime library
#just not to invent the wheel
#=======================================================================================================================
from math import cos
from os import remove
from re import match

def Left(s, pos):
    return s[0:pos]

def Right(s, pos):
    return s[len(s)-pos:len(s)]

def Mid(s,pos):
    return s[pos-1:len(s)]

def UCase(s):
    return s.upper()

def LCase(s):
    return s.lower()

def Trim(s):
    return s.strip()

def Len(s):
    return len(s)


def Sqr(x):
    return (x**0.5)


def Cos(x):
    return cos(x)


def Sin(x):
    return sin(x)


def Abs(x):
    return abs(x)

def Round(x):
    return round(x)

def IsNumeric(s):
    return True

def Kill(s):
    remove(s)


class RegExp:
    Pattern=""
    def Test(self,s):
        result = match(self.Pattern, s)

        return result!=None


