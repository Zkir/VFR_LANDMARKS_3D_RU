#====================================================================================
# home-brew relational DB interface
# plain files pipe (|) separated
#====================================================================================
def loadDatFile(strInputFile, encoding="utf-8"):
    cells = []
    filehandle = open(strInputFile, 'r', encoding=encoding)
    txt = filehandle.readline().strip()
    while len(txt) != 0:
        if txt[0] != "#":
            row = txt.strip().split("|")
            for i in range(len(row)):
                row[i] = row[i].strip()
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