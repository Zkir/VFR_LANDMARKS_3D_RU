import sys
import mdlZDBI
from mdlClassify import * 

cells = mdlZDBI.loadDatFile("../work_folder/22_all_osm_objects_list/all-objects.dat") 
building_types = {}
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


print("=======================")        
print("Buildings")        
print("=======================") 
building_types=list(building_types.items())
building_types.sort(key=lambda rec: rec[1], reverse=True)

for rec in building_types:
    if buildingTypeRus(rec[0]) == rec[0].upper() and rec[1]>=3 and rec[0] not in useless_building_types:
        print("'"+rec[0].upper()+"': '"+ str(rec[1])+"'") #+ '  ('+buildingTypeRus(rec[0])+')'

print()
print()
print("=======================")        
print("Buildings inverse")        
print("=======================")        

inv_buildings = {}
for k, v in building_types_rus_names.items():
    inv_buildings[v] = inv_buildings.get(v,[])+[k]

inv_buildings=list(inv_buildings.items())
inv_buildings.sort(key=lambda rec: rec[0], reverse=False)

for rec in inv_buildings:
    print(rec[0].ljust(30),rec[1])        
        
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



        
print("="*70)        
print("Статистика по стилям")        
print("="*70)        
print("Название стиля".ljust(25), "в тегах".rjust(4)+'  ', "по дате".rjust(4)+'  ', "оригинальные теги")        
print("-"*70)        
arch_styles_dict=dict(arch_styles)        

inv_styles = {}
for k, v in achitecture_styles_rus_names.items():
    inv_styles[v] = inv_styles.get(v,[])+[k]

inv_styles=list(inv_styles.items())
inv_styles.sort(key=lambda rec: rec[0], reverse=False)

for rec in inv_styles:
    n=0
    n_auto=0
    for style in rec[1]:
        n=n+arch_styles_dict.get(style,0)
        n_auto=n_auto+arch_styles_dict.get('~'+style,0)
    print(rec[0].ljust(25), str(n).rjust(6)+'    ', str(n_auto).rjust(6)+'  ', rec[1])        