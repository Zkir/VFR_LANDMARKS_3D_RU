#*********************************************************************
# filter by bbox transformer
# Primary key to join is hardcoded: 1+2 
# 0 is counter 
#*********************************************************************

import os
import sys
import zDatInterface as zdi

output_file_name = sys.argv[1]
source_file_name = sys.argv[2]
quadrant_code = sys.argv[3]

#print ("filter by quadrant_code")
print (source_file_name)
#print (output_file)
#print (quadrant_code)

i = 0
j = 0

records = zdi.loadDatFile(source_file_name)
output = [] 


bbox_min_lat = 56
bbox_min_lon = 38
bbox_max_lon = bbox_min_lon + 1
bbox_max_lat = bbox_min_lat + 1

for row in records:
    j = j + 1
    min_lat = float(row[3])
    min_lon = float(row[4])
    max_lat = float(row[5])
    max_lon = float(row[6])
    
    lat = (min_lat+max_lat)/2
    lon = (min_lon+max_lon)/2
    
    if (lon>=bbox_min_lon) and (lon<bbox_max_lon) and (lat>=bbox_min_lat) and (lat<bbox_max_lat) :
        i = i + 1
        row[0] = str(i)
        output.append(row)
        
    
        

zdi.saveDatFile(output, output_file_name)
print (str(j) + ' object(s) read, '+str(i)+' objects written' )      