import mdlMisc

import sys
sys.path.append('../3dcheck/')
from mdlClassify import buildingTypeRus, achitectureStylesRus




cells=mdlMisc.loadDatFile("../work_folder/22_all_osm_objects_list/all-objects.dat") 
building_types={}
arch_styles = {}

for rec in cells:
    if rec[10].strip()!="":
        if rec[10] not in building_types:
            building_types[rec[10]]=0
        building_types[rec[10]] += 1    
    
    style=rec[15].strip()
    if style!="":
        if style not in arch_styles:
            arch_styles[style]=0
        arch_styles[style] += 1    


building_types=list(building_types.items())
building_types.sort(key=lambda rec: rec[1], reverse=True)

for rec in building_types:
    if buildingTypeRus(rec[0]) == rec[0].upper() and rec[1]>=5:
        print(rec[0].upper()+": "+ str(rec[1])) #+ '  ('+buildingTypeRus(rec[0])+')'
        
print()
print()
print("=======================")        
print("Styles")        
print("=======================")        

arch_styles=list(arch_styles.items())
#arch_styles.sort(key=lambda rec: rec[1], reverse=True)
arch_styles.sort(key=lambda rec: rec[0], reverse=False)

for rec in arch_styles:
    if rec[1]>=2 and  achitectureStylesRus(rec[0]) == rec[0]:
        print("'"+rec[0]+"': '"+ str(rec[1])+"',")        