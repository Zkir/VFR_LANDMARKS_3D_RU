from osmXMLparcer import *
from osmGeometry import *
from vbFunctions import *
from mdlMisc import *
from mdlSite import *
import time


import sys

if len(sys.argv)>1:
    strQuadrantName = sys.argv[1]
else:
    strQuadrantName = composeQuadrantName(56, 38)

lat=int(strQuadrantName[1:3])
lon=int(strQuadrantName[4:7])

print(lat,lon)

CreateRegionSummaryPage(None, lat, lon)
CreateIndexPage()


#print ("Finished in "+str(t2-t1)+" seconds")
print ("Done!")
