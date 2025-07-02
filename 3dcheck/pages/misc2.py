
from .mdlMisc import *

region_names = {'rus_top':'Топ зданий, Россия',
                'rus_top_windows':'Топ зданий с ОКНАМИ, Россия',
                'rus_latest': 'Последние изменения, Россия',
                'photo_wo_type': 'Здания без типа, Россия',
               }
               
def get_region_name(quadrant_code):
    
    regions = loadDatFile("data/quadrants/Quadrants.dat")
    strQuadrantTitle = ""
    for region in regions:
        if region[0]== quadrant_code:
            strQuadrantTitle = region[1]
            break
    else:
        strQuadrantTitle = region_names.get(quadrant_code.lower(), quadrant_code)
    
    return strQuadrantTitle