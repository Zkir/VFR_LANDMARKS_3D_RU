
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
    
def shortenDistrictName(strDistrict):
    strDistrict = strDistrict.replace('район', 'р-н')
    strDistrict = strDistrict.replace('городской округ', 'го')
    strDistrict = strDistrict.replace('муниципальный округ', 'мо')
    return strDistrict
    
def composeAddressLine(rec):
    strDistrict = shortenDistrictName(rec[21])
    
    address = []
    for address_element in (rec[20].strip(), strDistrict.strip(), rec[22].replace('область', 'обл.').strip()):
        address_element_alias = address_element.replace('Челябинский го', 'Челябинск').strip()
        address_element_alias = (' '+address_element_alias+ ' ').replace(' го ', '').strip()
        address_element_alias = (' '+address_element_alias+ ' ').replace(' мо ', '').strip()
        if address_element and (address_element not in address and address_element_alias not in address ):
            address.append(address_element)
    
    address = ", ".join(address)
            
    return address