import json
import requests
import mdlMisc
from  mdlDBMetadata import * 
import os
import sys
sys.path.append('../3dcheck/')
from mdlClassify import * 


wikidata_buildings={
                    'Q19860854': 'ruins', # building or structure that has been demolished or destroyed
                    'Q811979':   'building', 
                    'Q41176':    'building',
                    'Q35112127': 'building', # historic building
                    'Q180174':   'building', # folly does not say anything about the building unfortunatelly
                    'Q811430':   'building', # fixed construction
                    'Q3947':     'residential', #house=building usually intended for living in
                    'Q279118':   'house', # wooden house
                    'Q12104567': 'apartments',
                    'Q13402009': 'apartments',
                    'Q1577547':  'apartments',  #revenue house
                    'Q989946':   'roof',    # shelter=basic architectural structure or building providing protection from the local environment
                    'Q1802963':  'manor',   # mansion 
                    'Q879050':   'manor', 
                    'Q1365179':  'manor',   # private mansion 
                    'Q12292478': 'MANOR',   # estate
                    'Q1021645':  'office',  # office building
                    'Q2519340':  'office',  # administrative building
                    'Q16831714': 'office',  # government building 
                    'Q25550691': 'office',  # town hall= chief administrative seat of a municipality
                    'Q18761864': 'OFFICE',  # bank
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
                    'Q2385804':  'school',  # educational institution
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
                    'Q27055621': 'orthodox church', #russian wooden church !!!!!
                    'Q27055636': 'old_believers church', 
                    'Q1975485':  'orthodox chapel' ,
                    'Q56242235': 'lutheran church', 
                    'Q56242275': 'lutheran church',  
                    'Q32815':    'mosque', 
                    'Q1454820':  'mosque', #congregational mosque 
                    'Q125626250':'MOSQUE', #! takya or sufi lodge is an islamic monastery. 
                    'Q5393308':  'Buddhist temple', 
                    'Q65156015': 'Buddhist temple',  # khurul= буддийский храм (монастырь, обитель) в калмыцком ламаизме
                    'Q34627':    'synagogue',
                    'Q83405':    'industrial', #factory
                    # we do not have any better right now, smth like POWER_PLANT could be interesting                     
                    'Q1601458':  'INDUSTRIAL',  # combined heat and power station
                    'Q1781180':  'INDUSTRIAL',  # condensation power station
                    'Q15911738': 'INDUSTRIAL',  # hydroelectric power station
                    'Q30565277': 'INDUSTRIAL',  # geothermal power station
                    
                    'Q57821':    'fortification',
                    'Q57831':    'fortress',
                    'Q81917':    'DEFENSIVE TOWER', 
                    'Q1785071':  'fort',  

                    'Q483110':   'stadium',
                    'Q641226':   'stadium',  # arena !!!!! there is no proper tag for arenas in OSM.  stadium and sports_centre are used despite definitions !!!!
                    'Q1154710':  'stadium',  #association football venue
                    'Q1282870':  'ice_rink',
                    'Q2617766':  'ice_rink', # speed skating rink
                    'Q11166728': 'communication tower',#television tower 
                    'Q1435490':  'people\'s house',
                    'Q494829':   'bus station',
                    'Q55488':    'TRAIN_STATION',  # railway station
                    'Q1339195':  'TRAIN_STATION',  # station building 
                    'Q928830':   'TRAIN_STATION',  # metro station 
                    'Q2281788':  'public aquarium',
                    'Q4989906':  'monument', 
                    'Q860861':   'sculpture',
                    'Q162875':   'mausoleum',
                    'Q39715':    'lighthouse',
                    'Q46124':    'sanatorium',
                    'Q11315':    'retail', #shopping center
                    'Q27686':    'hotel',
                    'Q233324':   'seminary',
                    'Q375336':   'film studio',
                    'Q11446':    'ship',
                    'Q97377955': 'SHIP', #floating nuclear power plant
                    'Q2811':     'SHIP',  #submarine
                    'Q751876':   'palace', #château
                    'Q16560':    'palace', 
                    'Q3950':     'villa',
                    'Q17715832': 'castle ruin',
                    'Q1686006' : 'summer residence',
                    'Q1195942':  'fire_station', 
                    
                    
                    'Q685204':   'GATEHOUSE',  #gate tower
                    'Q82117':    'CITY_GATE', 
                    'Q276173':   'GAZEBO',  #pavilion, but in osm pavilion means british sports pavilion
                    'Q23413':    'castle',  
                    'Q274153':   'water tower',  
                    'Q160169':   'house', #dacha 
                    'Q148319':   'planetarium',  
                    'Q143912':   'triumphal_arch',  
                    'Q16917':    'hospital', 
                    'Q952885':   'greenhouse',  #orangery 
                    
                    'Q785952':   'public bath',  #! do we have something like this in osm?  
                    
                    # we do not have any better currently
                    'Q1181413':  'THEATRE',  #palace of culture= large house of culture, major club-house
                    'Q1329623':  'THEATRE',  #cultural center=facility where culture and arts are promoted 
                    'Q1060829':  'THEATRE',  #concert hall

                    'Q15548045': 'almshouse',  #Богадельня
                    'Q2386997':  'RETAIL',  # Gostiny Dvor = Historical Russian indoor market or shopping centre
                    
                    'Q1254933':  'astronomical observatory',  #3
                    'Q7075':     'library',
                    'Q22806':    'library',  #national library   
                    'Q1112897':  'rostral column',  #2
                    'Q623525':   'rotunda',  #???
                    'Q53060':    'gate', 
                    'Q11707':    'restaurant',  
                    

                    }

wikidata_non_buildings={
                    # buildings, but those types do not give us much
                    'Q44539':    'temple',  # temple is not a proper value for chirstian religeous buildings
                    'Q12518':    'tower',
                    'Q18142':    'tower',  #tower block
                    'Q11303':    'skyscraper', # may be can help us in case height is missing?
                    
                    #strange non-building types
                    'Q634099':   'rural settlement in Russia',
                    'Q486972':   'human settlement',
                    'Q5084':     'hamlet ',
                    'Q532':      'village',
                    'Q2319498':  'village',
                    'Q7930989':  'city or town',  #2
                    
                    'Q2088357':  'musical ensemble',
                    'Q2416217':  'theatre troupe',
                    'Q11812394': 'theatre company',
                    'Q742421':   'theatre company',  #informal group of actors                    
                    'Q1364157':  'philharmonic society', 
                    'Q20819922': 'opera company',  
                    
                    'Q4830453':  'business',
                    'Q44613':    'monastery',
                    'Q11784935': 'Eastern Orthodox monastery',
                    'Q1693568':  'skete',
                    'Q1081138':  'historic site', 
                    'Q5':        'human', #!
                    'Q473972':   'protected area',
                    'Q60176300': 'Eastern Orthodox eparchy',
                    'Q35032':    'Eastern Orthodox Church', # pure bug, should not be on buildings as it is second-largest Christian church itself 
                    'Q112872396':'type of educational institution',
                    'Q1248784':  'airport', # место, где приземляются и взлетают самолёты
                    'Q358':      'heritage site',
                    'Q2760897':  'natural monument of Russia',
                    'Q27608973': 'natural monument of Russia' ,
                    'Q570116':   'tourist attraction',
                    'Q35749':    'parliament',
                    'Q15284':    'municipality',
                    'Q192287':   'administrative territorial entity of Russia',
                    'Q3982337':  'puppetry company ', #theatre organization that produces puppetry performances
                    'Q309398':   'ground-effect vehicle',
                    'Q644371':   'international airport',
                    'Q3917681':  'embassy', 
                    'Q1497364':  'building complex', 
                    'Q4201890':  'institute of the Russian Academy of Sciences',
                    'Q79007':    'street',  #!!!
                    'Q907698':   'prospekt',  #!!!
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

wikidata_achitecture_styles = {
                    'Q2479493':  'eclectic',
                    'Q23752285': 'eclectic',          # Eclectic architecture in Russia 
                    'Q192068':   'eclectic',          # eclecticism 
                    'Q1268134':  'eclectic',          # beaux-arts
                    'Q176483':   'gothic', 
                    'Q695863':   'gothic',            # Brick Gothic
                    'Q46825':    'gothic',            # Gothic art
                    'Q38451143': 'oldrussian',        # Pskov architectural style
                    'Q112869097':'oldrussian',        # Yaroslavl school
                    'Q4070874':  'oldrussian',        # Архитектура домонгольского Смоленска
                    'Q4401046':  'uzorochye', 
                    'Q37853':    'baroque',
                    'Q840829':   'baroque',
                    'Q3635094':  'baroque',           # Russian Baroque
                    'Q4418329':  'baroque',           # Siberian Baroque
                    'Q616753':   'baroque',           # Naryshkin Baroque
                    'Q4141616':  'baroque',           # Golitsyn Baroque
                    'Q19910996': 'baroque',           # Moscow baroque
                    'Q2636415':  'baroque',           # Petrine Baroque
                    'Q2359372':  'baroque',           # Elizabethan Baroque  
                    'Q1542287':  'baroque',           # Cossack Baroque
                    'Q122960':   'rococo',   
                    'Q863679':   'chinoiserie', 
                    'Q264649':   'neoclassicism',     #Palladian architecture, early neoclassicism, in Russia -- during reight of Ekaterine the Great                                
                    'Q3621606':  'neoclassicism',     # Neoclassical architecture in Russia
                    'Q14378':    'neoclassicism',     # neoclassicism  
                    'Q170292':   'neoclassicism',     # "classicism" 
                    'Q54111':    'neoclassicism',     # Neoclassical architecture
                    'Q4198718':  'neoclassicism',     # classical architecture 
                    'Q7382246':  'neoclassicism',     # Russian neoclassical revival 
                    'Q1513688':  'neoclassicism',     # Greek Revival architecture
                    'Q16191884': 'neoclassicism',     # Neo-Grec. seems to be the same thing in architecture as Greek Revival
                    'Q191105':   'empire',            # Empire style
                    'Q112711827':'empire',            # Russian Empire style
                    'Q2860359':  'russian-byzantine',
                    'Q106225044':'russian-byzantine', # Neo-Byzantine architecture in the Russian Empire
                    'Q966571':   'pseudo-russian',    # Byzantine Revival architecture
                    'Q2026876':  'pseudo-russian',    # Russian Revival architecture
                    'Q744373':   'neo-romanesque',    # Romanesque Revival architecture  #!!!! style of building employed beginning in the mid-19th century
                    'Q186363':   'neo-gothic',  
                    'Q942123':   'russian_gothic',    # Russian pseudo-gothic
                    'Q4221815':  'brick style', 
                    'Q173782':   'art_deco', 
                    'Q1295040':  'art_nouveau',
                    'Q34636':    'art_nouveau',
                    'Q1077702':  'nothern_modern',    # national Romantic style
                    'Q117005626':'nothern_modern',    # Northern modern -- fix wikidata !!
                    'Q502163':   'neo-renaissance',   # Renaissance Revival 
                    'Q841977':   'constructivism',  
                    'Q207103':   'constructivism',
                    'Q994776':   'brutalist',         # brutalist architecture
                    'Q1967635':  'postconstructivism',                                 
                    'Q1134824':  'stalinist_neoclassicism',  #Stalinist architecture 
                    'Q4439247':  'stalinist_neoclassicism',  #Stalinist Empire style
                    'Q47942':    'functionalism',  
                    'Q245188':   'modern',  
                    'Q24935410': 'modernism',                # Soviet Modernist architecture
                    'Q47783':    'postmodern',               # postmodernism
                    'Q238255':   'postmodern',               # deconstructivism
                    'Q595448':   'postmodern',               # postmodern architecture
                    'Q527449':   'ottoman',
                    'Q212940':   'islamic', 
                    'Q74156':    'moorish_revival',          # Moorish Revival architecture
                    'Q911397':   'neo-baroque',              #The Baroque Revival, also known as Neo-Baroque (or Second Empire architecture in France and Wilhelminism in Germany), late 19th and early 20th centuries.
                    'Q845318':   'high-tech',  
                    
                    'Q2600188':  '',  #Russian architecture = architectural styles within Russian sphere of influence ! Not a style! 
                    'Q37068':    '',  #Romanticism
                    'Q384177':   '',  #Egyptian Revival architecture
                    'Q2860299':  '',  #Armenian architecture 
                    'Q2535546':  '',  #rationalism. I do not think it's a real architectural style

                    }

                            

   
def print_sorted_dict(a_dict, limit=0):
    bubu = list( a_dict.items())
    bubu.sort(reverse=True, key=lambda x: int(x[1]) )
    for (key, value) in bubu:
        if int(value)>=limit:
            print("'"+key+"':'',  #"+ str(value)) 

def get_wikidata(qid):
    wikidata =None
    wdfilename="d:/_VFR_LANDMARKS_3D_RU/work_folder/23_wikidata/" + qid + '.json'
    
    if os.path.exists(wdfilename):
        with open(wdfilename,'r', encoding='utf-8') as f:
            wikidata = json.load(f)
    else:
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+qid+"&format=json" 
        r = requests.get(url)
        wikidata=json.loads(r.content.decode('utf-8'))
        
        with open(wdfilename, 'w', encoding='utf-8') as f:
            json.dump(wikidata, f, ensure_ascii=False, indent=4)

    return wikidata['entities'][qid]

def get_from_wikimedia_api(url):
    r = requests.get(url)
    response=json.loads(r.content.decode('utf-8'))
    return(response)

def download_file(url, filename):
    full_save_path = "d:/_VFR_LANDMARKS_3D_RU/work_folder/23_wikidata/" +  filename
    if os.path.exists(full_save_path):
        return
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers )
    if not r.ok:
        raise Exception("Unable to download file. Status "+str(r.status_code))
    
    with open(full_save_path, mode="wb") as file:
       file.write(r.content)

def get_wikidata_organized(qid):    
    wd={}

    wikidata = get_wikidata(qid)

    if 'en' in wikidata['labels']:
        wd["label"] = wikidata['labels']['en']['value']
        
    if 'ru' in wikidata['labels']:
        wd["label_ru"] = wikidata['labels']['ru']['value']    
    else:    
        wd["label_ru"] = ''
        
    if 'en' in wikidata['descriptions']:
        wd["description"]=wikidata['descriptions']['en']['value']
    else:  
        wd["description"]=""
        
    if 'ru' in wikidata['descriptions']:
        wd["description_ru"]=wikidata['descriptions']['ru']['value']
    else:  
        wd["description_ru"]=""
        
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
        wd["wikipedia"] = 'ru:'+wikidata['sitelinks']['ruwiki']['title']
    else:    
        wd["wikipedia"] = ""
        
    if 'P84' in wikidata['claims']:
        architect_id = wikidata['claims']['P84'][0]['mainsnak']['datavalue']['value']["id"]    
        architect_data = get_wikidata(architect_id)
        
        if 'en' in architect_data['labels']:
            wd["architect"] = architect_data['labels']['en']['value']
        else:
            wd["architect"] = ''
        
        if 'ru' in architect_data['labels']:
            wd["architect_ru"] = architect_data['labels']['ru']['value']    
        else:    
            wd["architect_ru"] = ''

    else:
        wd["architect"] = ''
        wd["architect_ru"] = ''
        
    if 'P149' in wikidata['claims']:
        wd["architecture"] = wikidata['claims']['P149'][0]['mainsnak']['datavalue']['value']["id"]            
    else:
        wd["architecture"] = ''
        
        
        
    return wd


# ============
# main block 
# ============
def main():
    unmatched_building_types_with_osm = {}

            
    cells=mdlMisc.loadDatFile("../work_folder/22_all_osm_objects_list/all-objects.dat") 

    n=0
    for rec in cells:
        if rec[QUADDATA_WIKIDATA_ID] !="":
            n += 1
    print("total objects with wikidata tag: ", n)
            
    wikidata_buildings_unknown = {}
    wikidata_architectures = {}

    for rec in cells:
        if rec[QUADDATA_WIKIDATA_ID]!="" :
            
            # Get info from wikidata DB
            wikidata = get_wikidata_organized(rec[QUADDATA_WIKIDATA_ID]) 
            
            # update missing fields, if possible
            wd_building_type =  wikidata_buildings.get(wikidata["instance_of"], '')
            wb_architecture = wikidata_achitecture_styles.get(wikidata["architecture"], '')
            
            
            # those descriptions from wikidata are really dumb!!!
            #if not rec[QUADDATA_DESCR]:
            #    rec[QUADDATA_DESCR] =  wikidata["description_ru"]
                
            if not rec[QUADDATA_WIKIPEDIA]:
                rec[QUADDATA_WIKIPEDIA] = wikidata["wikipedia"]
                
            if not rec[QUADDATA_NAME]:
                # name should be different from wikipeda article name, otherwise it is superfluous. 
                if 'ru:'+wikidata["label_ru"]!=rec[QUADDATA_WIKIPEDIA]:
                    rec[QUADDATA_NAME] =  wikidata["label_ru"]
                
            if not rec[QUADDATA_BUILDING_TYPE] and wd_building_type.upper() in building_types_rus_names:
                #original building type is empty and wd building type is among osm-matched building types 
                rec[QUADDATA_BUILDING_TYPE] = wd_building_type.upper()
                
            if not rec[QUADDATA_STYLE]:
                rec[QUADDATA_STYLE] = wb_architecture
                
            if not rec[QUADDATA_ARCHITECT]:
                rec[QUADDATA_ARCHITECT] = wikidata["architect_ru"]
             
            # calculate some usage statistics             
            if wd_building_type != 'building' and wd_building_type.upper() not in building_types_rus_names:
                if wd_building_type not in unmatched_building_types_with_osm:
                    unmatched_building_types_with_osm[wd_building_type] = 0
                unmatched_building_types_with_osm[wd_building_type] += 1
                
            value = wikidata["instance_of"]
            if value not in wikidata_buildings and value not in wikidata_non_buildings:
                if value not in wikidata_buildings_unknown:
                    wikidata_buildings_unknown[value] = 0
                wikidata_buildings_unknown[value] += 1 
           
            value = wikidata["architecture"]
            building_architecture =  wikidata_achitecture_styles.get(value,value)
            if building_architecture:
                if building_architecture not in wikidata_architectures:
                    wikidata_architectures[building_architecture] = 0 
                wikidata_architectures[building_architecture] += 1

                
                
            
            
            building_text_description =  ( 
                    rec[QUADDATA_COLOUR] + " " +
                    rec[QUADDATA_MATERIAL] + " " +
                    rec[QUADDATA_BUILDING_TYPE] + " " +
                    rec[QUADDATA_STYLE] + " " +
                    rec[QUADDATA_BUILD_DATE] + " " + 
                    rec[QUADDATA_ARCHITECT]
                    ).strip()
                    
            if building_text_description != '' and 'image' in wikidata:
                api_url ="https://commons.wikimedia.org/w/api.php?action=query&format=json" +"&prop=imageinfo&iiprop=url&titles=File:" + wikidata['image']
                print(rec[QUADDATA_OBJ_TYPE][0]+rec[QUADDATA_OBJ_ID], rec[QUADDATA_WIKIDATA_ID] )
                print('  ' + building_text_description)
                print('  ' + wikidata['image'])
                #print('  ' +'https://commons.wikimedia.org/wiki/File:'+wikidata['image'])
                #print('  ' + api_url)
                
                # we need to obtain actual download url via api, because it is hidden.           
                image_metadata = get_from_wikimedia_api(api_url)
                for _, yyy in image_metadata["query"]["pages"].items():
                    break # we just need one image, and expect only one
                image_download_url = yyy["imageinfo"][0]["url"] 
                print('  '+str(image_download_url))
                #download_file(image_download_url, wikidata['image'])
                           
                print()
               

    print()
    print('unrecognized wikidata building types:')    
    print_sorted_dict(wikidata_buildings_unknown,limit=2)
    print('unrecognized wikidata building types total: ', len(wikidata_buildings_unknown))        

    print()
    print("unmatched building types with osm")
    print_sorted_dict(unmatched_building_types_with_osm, limit=4)

    print()
    print("wikidata_architectures:")
    print_sorted_dict(wikidata_architectures,limit=3)

    mdlMisc.saveDatFile(cells, "../work_folder/22_all_osm_objects_list/all-objects-wd.dat")

#SF3D_USE_CPU=1
if __name__ == '__main__':
    main()
