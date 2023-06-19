#*********************************************************************
# join dat/csv transformer
# Primary key to join is hardcoded: 1+2 
# 0 is counter 
#*********************************************************************

import os
import zDatInterface as zdi

source_path = "work_folder\\10_osm_extracts"
output_file_name = "work_folder\\all-objects.dat" 


with os.scandir(source_path) as entries:
    output = [] 
    output_hash = set()
    i = 0
    j = 0
    k = 0
    for entry in entries:
        if entry.is_file():
                 
            records = zdi.loadDatFile(os.path.join(source_path,entry.name))
            k = k + 1
            for row in records:
                obj_type = row[1]
                obj_id = row[2]
                key=obj_type+'|'+obj_id
                
                if not (key in output_hash):
                    i = i + 1
                    row[0] = str(i)
                    output.append(row)
                    output_hash.add(key)
                else:
                    j = j + 1
            
            
    zdi.saveDatFile(output, output_file_name)      
    print (str(k) + ' dat files processed' )
    print (str(i) + ' object(s) written, '+str(j)+' duplicates rejected' )