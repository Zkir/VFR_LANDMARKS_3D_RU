import json
import requests
import mdlMisc
from  mdlDBMetadata import * 
import os


wikidata_buildings={
                    'Q19860854': 'ruin', # building or structure that has been demolished or destroyed
                    'Q811979':   'building', 
                    'Q41176':    'building',
                    'Q35112127': 'building', #historic building
                    'Q3947':     'residential', #house=building usually intended for living in
                    'Q279118':   'wooden house',
                    'Q12104567': 'apartments',
                    'Q13402009': 'apartments',
                    'Q1577547':  'apartments',  #revenue house
                    'Q989946':   'roof',    # shelter=basic architectural structure or building providing protection from the local environment
                    'Q1802963':  'manor',   # mansion 
                    'Q879050':   'manor', 
                    'Q1365179':  'manor',   # private mansion 
                    'Q1021645':  'office',  # office building
                    'Q2519340':  'office',  # administrative building
                    'Q16831714': 'office',  # government building 
                    'Q25550691': 'office',  # town hall= chief administrative seat of a municipality
                    'Q33506':    'museum',
                    'Q2087181':  'museum',  # historic house museum
                    'Q207694':   'museum',  # art museum
                    'Q2772772':  'museum',  # military museum
                    'Q588140':   'museum',  # science museum 
                    'Q10624527': 'museum',  # biographical museum
                    'Q2398990':  'museum',  # technology museum
                    'Q1595639':  'museum',  # local museum
                    'Q17431399': 'museum',  # national museum
                    'Q4453481':  'theatre',
                    'Q24354':    'theatre',
                    'Q153562':   'theatre', # opera house 
                    'Q84860894': 'theatre', # puppet theatre 
                    'Q1698619':  'theatre', # theatre intended primarily to show plays
                    'Q41253':    'cinema',  # movie theater 
                    'Q56195017': 'circus',
                    'Q38723':    'university',
                    'Q3918':     'university',
                    'Q180958':   'university',  #faculty 
                    'Q125569386':'university', # university branch
                    'Q4315006':  'university',  #national research university
                    'Q3914':     'school',
                    'Q1935049':  'school', # military school
                    'Q2385804':  'educational institution', 
                    'Q7692354':  'school', # техникум
                    'Q55043':    'school',  #gymnasium
                    'Q55008603': 'school',  #children's music school
                    'Q189004':   'school',  #college 
                    'Q1244442':  'school', 
                    'Q4438531':  'school',  #specialized secondary school
                    'Q108325':   'chapel',
                    'Q16970':    'church',
                    'Q200334':   'CAMPANILE',  #bell tower
                    'Q2977':     'church', #cathedral
                    'Q2031836':  'orthodox church',
                    'Q56242225': 'orthodox church',
                    'Q25416095': 'orthodox church', # sobor 
                    'Q27055621': 'russian wooden church', #!
                    'Q27055636': 'Old Believers church', 
                    'Q1975485':  'orthodox chapel' ,
                    'Q56242235': 'lutheran church', 
                    'Q56242275': 'lutheran church',  
                    'Q44539':    'temple', 
                    'Q32815':    'mosque', 
                    'Q1454820':  'mosque', #congregational mosque 
                    'Q5393308':  'Buddhist temple', 
                    'Q65156015': 'Buddhist temple',  # khurul= буддийский храм (монастырь, обитель) в калмыцком ламаизме
                    'Q34627':    'synagogue',
                    'Q12292478': 'estate',
                    'Q1601458':  'combined heat and power station',
                    'Q1781180':  'condensation power station',
                    'Q15911738': 'hydroelectric power station', 
                    'Q30565277': 'geothermal power station',
                    'Q57821':    'fortification',
                    'Q57831':    'fortress',
                    'Q81917':    'fortified tower', 
                    'Q1785071':  'fort',  
                    'Q83405':    'industrial', #factory
                    'Q483110':   'stadium',
                    'Q641226':   'arena', #!
                    'Q1154710':  'stadium',  #association football venue
                    'Q1282870':  'ice rink',
                    'Q2617766':  'ice rink', # speed skating rink
                    'Q11166728': 'communication tower',#television tower 
                    'Q11303':    'skyscraper',
                    'Q1435490':  'people\'s house',
                    'Q494829':   'bus station',
                    'Q55488':    'railway station',
                    'Q1339195':  'station building',  
                    'Q2281788':  'public aquarium',
                    'Q4989906':  'monument', 
                    'Q860861':   'sculpture',
                    'Q162875':   'mausoleum',
                    'Q180174':   'folly',
                    'Q12518':    'tower',
                    'Q18142':    'tower',  #tower block
                    'Q39715':    'lighthouse',
                    'Q46124':    'sanatorium',
                    'Q11315':    'retail', #shopping center
                    'Q27686':    'hotel',
                    'Q97377955': 'floating nuclear power plant',
                    'Q233324':   'seminary',
                    'Q375336':   'film studio',
                    'Q11446':    'ship',
                    'Q751876':   'château', #!
                    'Q16560':    'palace', 
                    'Q3950':     'villa',
                    'Q17715832': 'castle ruin',
                    'Q1686006' : 'summer residence',
                    'Q1195942':  'fire_station', 
                    
                    
                    'Q1181413':  'palace of culture',  #11
                    'Q685204':   'GATEHOUSE',  #gate tower
                    'Q82117':    'CITY_GATE', 
                    'Q276173':   'GAZEBO',  #pavilion, but in osm pavilion means british sports pavilion
                    'Q23413':    'castle',  
                    'Q928830':   'metro station',  
                    'Q274153':   'water tower',  
                    'Q160169':   'dacha',
                    'Q148319':   'planetarium',  
                    'Q143912':   'triumphal_arch',  
                    'Q16917':    'hospital', 
                    'Q952885':   'greenhouse',  #orangery 
                    
                    'Q1060829':  'concert hall',  #! do we have something like this in osm?
                    'Q785952':   'public bath',  #! do we have something like this in osm?  
                    'Q1329623':  'cultural center',  #facility where culture and arts are promoted 
                    'Q18761864': 'bank',  

                    'Q15548045': 'almshouse',  #Богадельня
                    'Q2386997':  'Gostiny Dvor',  #Historical Russian indoor market or shopping centre
                    'Q2811':     'submarine',  #3
                    'Q1254933':  'astronomical observatory',  #3
                    'Q7075':     'library',
                    'Q22806':    'library',  #national library   
                    'Q1112897':  'rostral column',  #2
                    'Q623525':   'rotunda',  #???
                    'Q53060':    'gate', 
                    'Q11707':    'restaurant',  
                    
                    'Q125626250':'takya', #! Islamic term
                    
                    #strange non-building types
                    'Q532':      'village',
                    'Q2319498':  'village',
                    'Q2088357':  'musical ensemble',
                    'Q2416217':  'theatre troupe',
                    'Q4830453':  'business',
                    'Q44613':    'monastery',
                    'Q11784935': 'Eastern Orthodox monastery',
                    'Q1693568':  'skete',
                    'Q1081138':  'historic site', 
                    'Q5':        'human', #!
                    'Q473972':   'protected area',
                    'Q60176300': 'Eastern Orthodox eparchy',
                    'Q634099':   'rural settlement in Russia',
                    'Q112872396':'type of educational institution',
                    'Q1248784':  'airport', # место, где приземляются и взлетают самолёты
                    'Q358':      'heritage site',
                    'Q2760897':  'natural monument of Russia',
                    'Q27608973': 'natural monument of Russia' ,
                    'Q486972':   'human settlement',
                    'Q5084':     'hamlet ',
                    'Q7930989':  'city or town',  #2                    
                    'Q570116':   'tourist attraction',
                    'Q35749':    'parliament',
                    'Q15284':    'municipality',
                    'Q192287':   'administrative territorial entity of Russia',
                    'Q3982337':  'puppetry company ', #theatre organization that produces puppetry performances
                    'Q35032':    'Eastern Orthodox Church', # pure bug, should not be on buildings as it is second-largest Christian church itself 
                    'Q309398':   'ground-effect vehicle',
                    'Q644371':   'international airport',
                    'Q3917681':  'embassy', 
                    'Q1497364':  'building complex', 
                    'Q4201890':  'institute of the Russian Academy of Sciences',
                    'Q11812394': 'theatre company',
                     'Q742421':  'theatre company',  #informal group of actors                    
                    'Q79007':    'street',  #!!!
                    'Q907698':   'prospekt',  #!!!
                    'Q1364157':  'philharmonic society', 
                    'Q20819922': 'opera company',  
                    'Q31855':    'research institute',  
                    'Q875157':   'resort',  
                    'Q1076486':  'sports venue',  #!!!facility (building, structure, or place) dedicated to sports -- to general!
                    'Q43229':    'organization ',  #to general!
                    'Q166118':   'archive', 
                    'Q6881511':  'enterprise',  
                    'Q1664720':  'institute',  #organizational body created for a certain purpose - to general!
                    'Q13226383': 'facility',  #place, equipment, or service to support a specific function -- too general
                    'Q2116450':  'manor estate',  #estate in land to which is incident the right to hold a manorial court -- ??
                    'Q22698':    'park ',  
                    'Q15056993': 'aircraft family',  #lolwut?
                    'Q176799':   'military unit', 
                    'Q98798598': 'tourist facility', # to general!
                    'Q1959314':  'protected area of Russia',  
                    'Q1616075':  'television station', 
                    'Q13417114': 'noble family',                     
                    'Q270791':   'state-owned enterprise', 
                    'Q52341833': 'state archives',  
                    'Q988108':   'club',  #association of people united by a common interest or goal
                    'Q163740':   'nonprofit organization',  
                    'Q4671277':  'academic institution', 
                    'Q1497375':  'architectural ensemble',
                    'Q863915':   'inland port',                      
                    'Q43501':    'zoo', 

}

"""
'Q184356':'radio telescope',
'Q12019965':'indoor ice rink', #! possibly sport_centre?

"""
                    
   


def get_wikidata(qid):

    wdfilename="d:/_VFR_LANDMARKS_3D_RU/work_folder/23_wikidata/" + rec[QUADDATA_WIKIDATA_ID] + '.json'
    
    if os.path.exists(wdfilename):
        with open(wdfilename,'r', encoding='utf-8') as f:
            wikidata = json.load(f)
    else:
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+qid+"&format=json" 
        r = requests.get(url)
        wikidata=json.loads(r.content.decode('utf-8'))
        
        with open(wdfilename, 'w', encoding='utf-8') as f:
            json.dump(wikidata, f, ensure_ascii=False, indent=4)
        

    ##with open('Q4500809.json', 'r') as file:
    ##    wikidata = json.load(file)
    return wikidata['entities'][qid]

def get_wikidata_organized(qid):    
    wd={}

    wikidata = get_wikidata(qid)

    # Print the data
    if 'en' in wikidata['labels']:
        wd["label"] = wikidata['labels']['en']['value']
    
    if 'en' in wikidata['descriptions']:
        wd["description"]=wikidata['descriptions']['en']['value']
    elif 'ru' in wikidata['descriptions']:
        wd["description"]=wikidata['descriptions']['ru']['value']
    else:  
        wd["description"]=""
        
    if 'P31' in wikidata['claims']:
        wd["instance_of"] = wikidata['claims']['P31'][0]['mainsnak']['datavalue']['value']['id']
    else:
        wd["instance_of"] = '???'
        
    
    if 'P18' in wikidata['claims']:     
        wd["image"] = wikidata['claims']['P18'][0]['mainsnak']['datavalue']['value']
    if 'P856' in wikidata['claims']:
        wd["website"] = wikidata['claims']['P856'][0]['mainsnak']['datavalue']['value']
        
    if 'P625' in wikidata['claims']:
        wd["coordinates"] = wikidata['claims']['P625'][0]['mainsnak']['datavalue']['value']
    else:
        # coordinates may be missing in case object in wikidata is not a building, but 'Q2088357': 'musical ensemble'  for example
        wd["coordinates"] = None

    if 'P571' in wikidata['claims'] and 'datavalue' in wikidata['claims']['P571'][0]['mainsnak']:
        wd["start_date"] = wikidata['claims']['P571'][0]['mainsnak']['datavalue']['value']['time'][1:5]
        
    if 'ruwiki' in wikidata['sitelinks']:    
        wd["wikipedia"] = wikidata['sitelinks']['ruwiki']['title']
    else:    
        wd["wikipedia"] = ""
    return wd


cells=mdlMisc.loadDatFile("../work_folder/22_all_osm_objects_list/all-objects.dat") 

n=0
for rec in cells:
    if rec[QUADDATA_WIKIDATA_ID] !="":
        n += 1
print("total wikidata: ", n)
        
wikidata_buildings_unknown = {}

for rec in cells:
    if rec[QUADDATA_WIKIDATA_ID]!="":
    
        #print(rec[QUADDATA_OBJ_TYPE][0]+rec[QUADDATA_OBJ_ID], rec[QUADDATA_WIKIDATA_ID] )
        
        #print( 
        #    rec[QUADDATA_COLOUR] + " " +
        #    rec[QUADDATA_MATERIAL] + " " +
        #    rec[QUADDATA_BUILDING_TYPE] + " " +
        #    rec[QUADDATA_STYLE] + " " +
        #    rec[QUADDATA_BUILD_DATE]
        #    )

        
        #if rec[QUADDATA_ARCHITECT]!="":
        #    print(rec[QUADDATA_ARCHITECT])

        for key, value in get_wikidata_organized(rec[QUADDATA_WIKIDATA_ID]).items():
            #print (key+': "'+ str(value)+'"')
            
            if key== "instance_of":
                if value not in wikidata_buildings:
                    if value not in wikidata_buildings_unknown:
                        wikidata_buildings_unknown[value] = 0
                        #print("'"+value+"':'',")
                        
                    wikidata_buildings_unknown[value] += 1 
            
        #print()    
        #print()
    
bubu = list( wikidata_buildings_unknown.items())

bubu.sort(reverse=True, key=lambda x: int(x[1]) )

for (key, value) in bubu:
    if int(value)>1:
        print("'"+key+"':'',  #"+ str(value)) 
        
print( len(bubu))        

#SF3D_USE_CPU=1