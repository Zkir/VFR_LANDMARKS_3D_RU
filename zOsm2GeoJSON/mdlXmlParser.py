#***********************************************************************************************************************
# Very simple osm-xml parcer. Minimal funtionality, compartible with output of osmconvert tool.
#***********************************************************************************************************************
class clsXMLparser:
    filehandle=""
    bEOF=False
    node=""

    def OpenFile(self, strFileName):
        self.filehandle = open(strFileName, 'r', encoding='UTF-8' )
         

    def CloseFile(self):
        self.filehandle.close() 
    
    def ReadNextNode(self):
        self.node = self.filehandle.readline().strip()
        if not self.node:
            self.bEOF=True
        #print(self.node)
        

    def GetTag(self):
        i = self.node.find(" ")
        if i < 0:
            i = self.node.find(">")
        return (self.node[1:i])
  
    def GetAttribute(self,strAttrName):
        txt=""
        strToken = strAttrName + "=\""
        i = self.node.find(strToken)
        if i<0:
            strToken = strAttrName + "='"
            i = self.node.find(strToken)
        if i>=0:
            txt = self.node[i + len(strToken):len(self.node)]
            #print(txt)
            i = txt.find ("\"")
            if i<0:
                i = txt.find("'")
            txt = txt[0:i]
            txt = decodeXmlString(txt)

        return(txt)


def encodeXmlString(txt):
    txt = txt.replace("\"","&quot;" )
    txt = txt.replace("'","&apos;")
    return txt


def decodeXmlString(txt):
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&apos;", "'")
    txt = txt.replace("&#34;", "\"")
    return txt