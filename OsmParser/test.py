from osmXMLparcer import *
from osmGeometry import *
from vbFunctions import *
from mdlMisc import *
import time
import sys
import subprocess


BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'
CYCLE=24*60*60*3

def sortRecordset(cells, sort_field):
    cells.sort(key=lambda row: row[sort_field])
    pass


strInputFile="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat"
cells = loadDatFile(strInputFile)

print("Planner and dispatcher")
print("total number of quadrants: "+str(len(cells)))
print("Validator cycle: " + str(CYCLE)) 

# sort by date 
sortRecordset(cells, 4)
curtime=time.time()

for row in cells:
   if row[4].strip()!="":
       time_diff= curtime-time.mktime(time.strptime(row[4],"%Y.%m.%d %H:%M:%S"))
       time_diff=int(time_diff)
       if time_diff>CYCLE:
           past_due=True
       else: 
           past_due=False
   else:
       past_due=True
       time_diff=CYCLE


   print(row[0]+" " +row[4] + " " + str(time_diff) + " " + str(past_due) )
   
   if past_due:
       strQuadrantName = row[0]
       lat1=str(int(strQuadrantName[1:3]))
       lon1=str(int(strQuadrantName[4:7]))
       lat2=str(int(lat1)+1)
       lon2=str(int(lon1)+1)

 
       strCommand='process.bat ' + strQuadrantName +' "'+lon1+','+lat1+','+lon2+','+lat2+'"'
       print(strCommand)
       #subprocess.call(BUILD_PATH + '\\'+strCommand, cwd=BUILD_PATH)   

print ("Done!")
