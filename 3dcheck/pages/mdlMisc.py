from .vbFunctions import *
from datetime import datetime

#====================================================================================
# home-brew relational DB interface
# plain files pipe (|) separated
#====================================================================================
def loadDatFile(strInputFile):
    cells=[]  
    filehandle = open(strInputFile, 'r', encoding="utf-8")
    txt = filehandle.readline().strip()
    while len(txt) != 0:
        row = txt.strip().split("|")
        if len(row)>1:
            cells.append(row)
        txt = filehandle.readline()
    # end of while
    filehandle.close()
    return cells

def saveDatFile(cells,strOutputFile):

    filehandle = open(strOutputFile, 'w', encoding="utf-8" )
    for row in cells:
        txt = "" 
        for field in row: 
            if txt!="":
                txt = txt + "|"   
            txt = txt + field
        filehandle.write(txt+'\n') 
    filehandle.close()   
