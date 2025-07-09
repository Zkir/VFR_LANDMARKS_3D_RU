import json
import requests
import mdlMisc
from  mdlDBMetadata import * 
import os
import sys
from mdlClassify import * 
import argparse
from PIL import Image, ImageFile, UnidentifiedImageError
from pathlib import Path
from io import BytesIO
from tqdm import tqdm

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

WIKIDATA_DIRECTORY = "d:/_VFR_LANDMARKS_3D_RU/work_folder/23_wikidata"
IMAGE_DIRECTORY =    "d:/_VFR_LANDMARKS_3D_RU/work_folder/25_images"

LIMIT=150000

wikidata_buildings={
                    'Q19860854': 'ruins',       # building or structure that has been demolished or destroyed
                    'Q811979':   'building', 
                    'Q41176':    'building',
                    'Q35112127': 'building',    # historic building
                    'Q180174':   'building',    # folly does not say anything about the building unfortunatelly
                    'Q811430':   'building',    # fixed construction
                    'Q655686':   'building',    # commercial building
                    'Q11755880': 'residential', 
                    'Q3947':     'residential', # house=building usually intended for living in
                    'Q1498804':  'residential', # multifamily residential 
                    'Q279118':   'house',       # !!! wooden house  !!!
                    'Q160169':   'house',       # dacha 
                    'Q1307276':  'house',       # single-family detached home 
                    'Q41955438': 'building',    # !!! brick building  = building made out of bricks !!!
                    'Q12104567': 'apartments',
                    'Q13402009': 'apartments',
                    'Q1577547':  'apartments',  # revenue house
                    'Q105681016':'apartments',  # condominium
                    'Q847950':   'dormitory',  
                    'Q3661265':  'dormitory',  #university dormitory
                    'Q131263':   'barracks', 
                    'Q989946':   'roof',        # shelter=basic architectural structure or building providing protection from the local environment
                    'Q1802963':  'manor',       # mansion 
                    'Q879050':   'manor', 
                    'Q1365179':  'manor',       # private mansion 
                    'Q12292478': 'manor',       # estate
                    'Q15848826': 'palace',      # city palace
                    'Q751876':   'palace',      # château
                    'Q16560':    'palace', 
                    'Q3950':     'villa',
                    'Q1686006':  'summer residence',
                    'Q1021106':  'mansion',     # bourgeois house 
                    'Q875016':   'terrace',     # terrace house 
                    
                    'Q1021645':  'office',      # office building
                    'Q203180':   'office',      # serviced office (Бизнес-центр)
                    'Q2519340':  'office',      # administrative building
                    'Q16831714': 'office',      # government building 
                    'Q25550691': 'office',      # town hall= chief administrative seat of a municipality
                    'Q294422':   'office',      # public building = owned and operated by a governing body, carrying out official duties, and often occupied by a governmental agency
                    'Q18761864': 'OFFICE',      # bank
                    'Q4453481':  'theatre',
                    'Q24354':    'theatre',
                    'Q153562':   'theatre',     # opera house 
                    'Q84860894': 'theatre',     # puppet theatre 
                    'Q1698619':  'theatre',     # theatre intended primarily to show plays
                    'Q41253':    'cinema',      # movie theater 
                    'Q56195017': 'circus',
                    'Q16889960': 'circus',      # circus building
                    'Q38723':    'university',
                    'Q3918':     'university',
                    'Q180958':   'university',  # faculty 
                    'Q125569386':'university',  # university branch
                    'Q4315006':  'university',  # national research university
                    'Q875538':   'university',  # public university
                    'Q917182':   'university',  # military academy
                    'Q3551775':  'university',  # university in France
                    'Q3914':     'school',      # school as institution
                    'Q1244442':  'school',      # school as building
                    'Q1935049':  'school',      # military school
                    'Q2385804':  'school',      # educational institution
                    'Q7692354':  'school',      # техникум
                    'Q55043':    'school',      # gymnasium
                    'Q55008603': 'school',      # children's music school
                    'Q189004':   'school',      # college 
                    'Q4438531':  'school',      # specialized secondary school
                    'Q233324':   'school',      # seminary
                    'Q132834':   'school',      # madrasa  
                    'Q1542966':  'school',      # secondary school in Germany
                    'Q9842':     'school',      # primary school 
                    'Q20860083': 'school',      # educational facility 
                    
                    'Q108325':   'chapel',
                    'Q1457501':  'chapel',                #cemetery chapel
                    'Q16970':    'church',
                    'Q200334':   'campanile',             # free-standing bell tower
                    'Q2977':     'church',                # cathedral
                    'Q317557':   'church',                # parish church - church which acts as the religious centre of a parish
                    'Q334383':   'church',                # abbey church 
                    'Q56242215': 'catholic church',       # Catholic cathedral 
                    'Q1129743':  'catholic church',       # filial church - in the Roman Catholic Church, a church building that is not the main church of a parish
                    'Q10631691': 'catholic church',       # catholic pilgrimage church
                    'Q1088552':  'catholic church',       # catholic church building
                    'Q1509716':  'catholic church',       # collegiate church
                    'Q120560':   'catholic church',       # minor basilica -- title given to some Roman Catholic churches
                    'Q2031836':  'orthodox church',
                    'Q56242225': 'orthodox church',
                    'Q25416095': 'orthodox church',       # sobor 
                    'Q27055621': 'orthodox church',       # russian wooden church !!!!!
                    'Q27055636': 'old_believers church', 
                    'Q1975485':  'orthodox chapel' ,
                    'Q56242235': 'lutheran church', 
                    'Q56242275': 'lutheran church',  
                    'Q56242063': 'protestant church', 
                    'Q32815':    'mosque', 
                    'Q1454820':  'mosque',                # congregational mosque 
                    'Q125626250':'mosque',                #! takya or sufi lodge is an islamic monastery. 
                    'Q5393308':  'buddhist temple', 
                    'Q65156015': 'buddhist temple',       # khurul= буддийский храм (монастырь, обитель) в калмыцком ламаизме
                    'Q34627':    'synagogue',
                    'Q44613':    'monastery',
                    'Q11784935': 'monastery',             # Eastern Orthodox monastery
                    'Q160742':   'monastery',             # abbey 
                    'Q1128397':  'monastery',             # convent 
                    'Q2750108':  'monastery',             # priory 
                    #industrial 
                    'Q83405':    'industrial',            # factory
                    'Q1662011':  'industrial',            # industrial building
                    # we do not have any better right now, smth like POWER_PLANT could be interesting    
                    'Q159719':   'industrial',            # power station = facility generating electric power               
                    'Q1601458':  'industrial',            # combined heat and power station
                    'Q1781180':  'industrial',            # condensation power station
                    'Q15911738': 'industrial',            # hydroelectric power station
                    'Q30565277': 'industrial',            # geothermal power station
                    'Q200297':   'industrial',            # thermal power station  
                    'Q1411996':  'industrial',            # Run-of-river hydroelectricity 
                    # other industrial building
                    'Q131734':   'brewery',               # brewery 
                    'Q798436':   'bakehouse',             # bakehouse 
                    
                    'Q57821':    'fortification',
                    'Q57831':    'fortress',
                    'Q81917':    'defensive tower',
                    'Q20034791': 'defensive tower',                     
                    'Q1785071':  'fort',  
                    'Q947103':   'watchtower',            # watchtower
                    'Q16748868': 'citywalls',             # city walls                     

                    'Q483110':   'stadium',
                    'Q641226':   'stadium',               # arena !!!!! there is no proper tag for arenas in OSM.  stadium and sports_centre are used despite definitions !!!!
                    'Q1154710':  'stadium',               # association football venue
                    'Q1282870':  'ice_rink',
                    'Q2617766':  'ice_rink',              # speed skating rink
                    'Q12019965': 'ice_rink',              # indoor ice rink
                    'Q7579839':  'sports_centre',         # sports complex !!! we do not really know what it (or osm 'sports_centre') is. 
                    'Q11166728': 'communication tower',   # television tower 
                    'Q1435490':  'people\'s house',
                    'Q494829':   'bus_station',
                    'Q55488':    'train_station',         # railway station
                    'Q1339195':  'train_station',         # station building 
                    'Q928830':   'subway_entrance',       # metro station 
                    'Q2921357':  'subway_entrance',       # we do not have this in OSM currently. 
                    'Q67183571': 'transportation',        # terminal 
                    'Q2281788':  'public_aquarium',
                    'Q4989906':  'monument', 
                    'Q860861':   'sculpture',
                    'Q162875':   'mausoleum',
                    'Q1578744':  'tomb',                  # burial vault
                    'Q39715':    'lighthouse',
                    'Q46124':    'sanatorium',
                    'Q18760388': 'retail',
                    'Q213441':   'retail',  # shop = place where items or services are sold
                    'Q11315':    'retail',  # shopping center
                    'Q132510':   'retail',  # market 
                    'Q216107':   'retail',  # department store
                    'Q2386997':  'retail',  # Gostiny Dvor = Historical Russian indoor market or shopping centre
                    'Q27686':    'hotel',   # hotel as business enterprise 
                    'Q63099748': 'hotel',   # hotel as building
                    'Q256020':   'hotel',   # inn
                    'Q5526694':  'hotel',   # gasthaus 
                    
                    'Q24699794': 'museum',  # museum building - relevant!
                    

                    'Q375336':   'film_studio',
                    'Q11446':    'ship',
                    'Q97377955': 'ship',  # floating nuclear power plant
                    'Q2811':     'ship',  # submarine
                    'Q17715832': 'ruined castle', #castle ruin
                    'Q1195942':  'fire_station', 
                    
                    'Q685204':   'gatehouse',  #gate tower
                    'Q82117':    'city_gate', 
                    'Q276173':   'gazebo',  #pavilion, but in osm pavilion means british sports pavilion
                    'Q23413':    'castle',  
                    'Q615810':   'castle',  #water castle
                    'Q274153':   'water tower',  
                    'Q148319':   'planetarium',  
                    'Q143912':   'triumphal_arch',  
                    'Q16917':    'hospital', 
                    'Q39364723': 'hospital', 
                    'Q1774898':  'clinic',  
                    'Q952885':   'greenhouse',  #orangery 
                    
                    'Q785952':   'bath',  # corresponds to osm building=bath
                    
                    # we do not have any better currently
                    'Q1181413':  'theatre',  # palace of culture = large house of culture, major club-house
                    'Q5061188':  'theatre',  # house of culture = cultural building; cultural institution
                    'Q1329623':  'theatre',  # cultural center = facility where culture and arts are promoted 
                    'Q1060829':  'theatre',  # concert hall

                    'Q15548045': 'almshouse',           # Богадельня

                    
                    'Q1254933':  'observatory',         # astronomical observatory 
                    'Q7075':     'library',
                    'Q22806':    'library',             # national library   
                    'Q856584':   'library',             # library building
                    'Q2326815':  'library',             # municipal library 
                    'Q1112897':  'rostral_column',  
                    'Q623525':   'rotunda',             #???
                    'Q53060':    'gate', 
                    'Q11707':    'restaurant',  
                    'Q30022':    'coffeehouse',          # establishment that serves coffee and tea
                    'Q184644':   'conservatory', 
                    'Q57659484': 'exhibition_hall', 
                    'Q199451':   'pagoda',  
                    'Q383092':   'art_academy',  
                    'Q13107184': 'retail',               # pharmacy 
                    'Q861951':   'police',  
                    'Q55485':    'dead-end railway station',  #dead-end railway station
                    'Q184356':   'radio_telescope',  
                    
                    'Q543654':   'townhall',              # rathaus
                    'Q1303167':  'barn',                  # barn
                    'Q185187':   'watermill',             # watermill 
                    'Q38720':    'windmill',              # windmill
                    'Q3044808':  'outbuilding',           # outbuilding
                    'Q182676':   'mountain_hut',          # mountain hut
                    
                    'Q489357':   'farm',                  # chief dwelling-house attached to a farm
                    'Q2588110':  'farm',                  # type of a farmhouse combining living quarters and stables
                    'Q131596':   'farm',                  # area of land for farming, or, for aquaculture, lake, river or sea, including various structures
                    
                    #German specific types
                    'Q1362233':  'upper_lusatian house',  # Upper Lusatian house  --  combines log house, timber-framing and building stone methods of construction 
                    'Q12020836': 'timber_frame house',    # residential building constructed using the timber framing method
                    'Q607241':   'presbytery',            # where priests live and work
                    'Q18760306': 'commercial',            # combined residential and commercial house or building
                    'Q907632':   'house',                 # !!!! Bremer Haus !!!! 
                    'Q16823155': 'castle',                # Schloss 
                    'Q1440300':  'observation tower',     # civilian structure used to view the surrounding landscape --different form OSM. In OSM observation_tower is military structure
                    
                    'Q1220959':  'government',            # building of public administration
                    
                    'Q30114662': 'nursing_home',          # accommodation facility for dependent elderly people, corresponds to amenity=nursing_home
                    'Q83554028': 'barracks',              # Gendarmerie barracks (FRENCH)
                    'Q2080521':  'marketplace',           # covered space used as a marketplace
                    
                    'Q948878':   'dovecote',              # FR:89
                    'Q846451':   'caisson ',              # FR:88
                    
                    'Q1408475':  'fortified_house',       # fortified house
                    'Q1137809':  'courthouse',            # courthouse  !!!! amenity=courthouse!!!
                    'Q483453':   'fountain',              # fountain !!!! man_made???
                    
                    'Q18674739': 'event_venue ',          # FR:51
                    
                    'Q1523545': 'manor',  #FR:49
                    'Q1690211': 'lavoir ',  #FR:44
                    'Q91165':   'defensive tower',        # keep
                    'Q1502700': 'defensive tower',        # Genoese towers in Corsica

                    'Q133215':  'casino',                 # casino
                    
                    ##'Q1424583': 'chapel',  # sepulchral chapel

                    'Q815448':  'bell_tower',             # belfry  -- Вечевая башня
                    'Q493694':  'tide_mill',              # tide mill
                    'Q575759':  'memorial',               # war memorial 
                    'Q14092':   'sports_hall',            # building designed and equipped for athletics and fitness
                    'Q12323':   'dam',                    #
                    'Q126807':  'kindergarten',  
                    
                    #'Q156362':  'winery',                 # winery  -- WTF???
                    #'Q1434544': 'commandry',              # is it a castle???
                    #'Q2945655': '',  # centre hospitalier (France) 


                    }

wikidata_non_buildings={
                    # buildings, but those types do not give us much
                    'Q44539':    'temple',  # temple is not a proper value for chirstian religeous buildings
                    'Q12518':    'tower',
                    'Q18142':    'tower',  #tower block
                    'Q11303':    'skyscraper', # may be can help us in case height is missing?
                    'Q11755959': 'multi-story urban building',  #french item, we do not have similar value in osm
                    
                    # museum can be created from any type of building
                    'Q33506':    'museum',
                    'Q2087181':  'museum',      # historic house museum
                    'Q207694':   'museum',      # art museum
                    'Q2772772':  'museum',      # military museum
                    'Q588140':   'museum',      # science museum 
                    'Q10624527': 'museum',      # biographical museum
                    'Q2398990':  'museum',      # technology museum
                    'Q1595639':  'museum',      # local museum
                    'Q17431399': 'museum',      # national museum
                    'Q3329412':  'museum',      # archaeological museum 
                    'Q16735822': 'museum',      # history museum
                    
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
                    'Q44782':    'port',                      
                    'Q43501':    'zoo', 
                    'Q1348006':  'city block',   #= central element of urban planning and urban design; smallest area that is surrounded by streets
                    'Q126916836':'Solnceva street',  #s treet in Ramenskoye
                    'Q327333':   'government agency', 
                    
                    'Q1516079':  'cultural heritage ensemble',
                    'Q13406463': 'Wikimedia list article', 
                    'Q253019':   'Ortsteil',      #named subdivision or section of a human settlement in Germany, Austria or Switzerland
                    'Q123705':   'neighborhood',  #neighborhood
                    'Q839954':   'archaeological site', 
                    'Q521458':   'railway infrastructure manager',  #railway infrastructure manager
                    'Q39614':    'cemetery',  
                    'Q36794':    'door',  
                    'Q484170':   'commune of France ',    # commune of France 
                    'Q18706073': 'EPCI with own taxation',  #EPCI with own taxation
                    'Q2001305':  'television channel ',  
                    'Q1735655':  'Ministry of Emergency Situations',  

}

wikidata_achitecture_styles = {
                    'Q2479493':  'eclectic',
                    'Q23752285': 'eclectic',          # Eclectic architecture in Russia 
                    'Q192068':   'eclectic',          # eclecticism 
                    'Q1268134':  'eclectic',          # beaux-arts
                    'Q708807':   'pre-romanesque',    #FR, no such thing in OSM!!!
                    'Q46261':    'romanesque',        # romanesque 
                    'Q46805':    'romanesque',        # romanesque art 
                    'Q2864731':  'romanesque',        # Romanesque art of Provence 
                    'Q4692':     'renaissance',       # renaissance in general 
                    'Q236122':   'renaissance ',      # renaissance as architecture
                    'Q176483':   'gothic', 
                    'Q695863':   'gothic',            # Brick gothic
                    'Q46825':    'gothic',            # Gothic art
                    'Q10924220': 'gothic',            # Late gothic
                    'Q3111491':  'gothic',            # FR Meridional Gothic 
                    'Q1351624':  'gothic',            # Flamboyant i.e. florid style of late Gothic architecture
                    
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
                    'Q20192147': 'neoclassicism',     # Neoclassicalism 
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
                    'Q12720942': 'art_deco',          # Art Deco architecture
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
                    'Q24935410': 'modernist',                # Soviet Modernist architecture
                    'Q162324':   'international',            # International style, type of modernist architecture
                    'Q1962399':  'modern',                   # post WW2 modernism in Germany and Switzerland
                    'Q47783':    'postmodern',               # postmodernism
                    'Q238255':   'postmodern',               # deconstructivism
                    'Q595448':   'postmodern',               # postmodern architecture
                    'Q527449':   'ottoman',
                    'Q212940':   'islamic', 
                    'Q74156':    'moorish_revival',          # Moorish Revival architecture
                    'Q911397':   'neo-baroque',              # The Baroque Revival, also known as Neo-Baroque (or Second Empire architecture in France and Wilhelminism in Germany), late 19th and early 20th centuries.
                    'Q845318':   'high-tech',  
                    'Q12020836': 'timber_frame',             #timber-framed house  
                    
                    'Q1323065':  'louis_xiii',               # FR: Louis XIII style 
                    'Q174419':   'second_empire',            # FR: Second Empire style-- ??neo-baroque??
                    'Q466887':   'belle_epoque',             # FR: Belle Époque
                    
                    'Q384177':   'egyptian_revival',         # Egyptian Revival architecture
                    'Q97382697': 'caprom',                   # post-soviet postmodernism
                    
                    #'Q2600188':  '',  #Russian architecture = architectural styles within Russian sphere of influence ! Not a style! 
                    #'Q37068':    '',  #Romanticism
                    
                    #'Q2860299':  '',  #Armenian architecture 
                    #'Q2535546':  '',  #rationalism. I do not think it's a real architectural style
                    #'Q1349760':  'medieval',                # medieval architecture -- not really a style

                    }

                            

   
def print_sorted_dict(a_dict, limit=0):
    bubu = list( a_dict.items())
    bubu.sort(reverse=True, key=lambda x: int(x[1]) )
    for (key, value) in bubu:
        if int(value)>=limit:
            print("'"+key+"':'',  #"+ str(value)) 

def get_wikidata(qid):
    wikidata =None
    wdfilename=WIKIDATA_DIRECTORY + "/" + qid + '.json'
    
    if os.path.exists(wdfilename):
        with open(wdfilename,'r', encoding='utf-8') as f:
            wikidata = json.load(f)
    else:
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids="+qid+"&format=json" 
        r = requests.get(url)
        wikidata=json.loads(r.content.decode('utf-8'))
        
        with open(wdfilename, 'w', encoding='utf-8') as f:
            json.dump(wikidata, f, ensure_ascii=False, indent=4)
    if 'entities' in wikidata:
        return wikidata['entities'][qid]
    else:
        return None         

def get_from_wikimedia_api(url):
    r = requests.get(url)
    response=json.loads(r.content.decode('utf-8'))
    return(response)

def download_image(url, filename):
    NEW_SIZE = 512
    # setup
    short_filename = Path(filename).stem
    extension      = Path(filename).suffix
    if extension in ['.svg']:
        # vector images are not supported either by PIL nor by pytorch
        # so we cannot do much with them, just skip
        return
    
    #full_save_path = os.path.join(IMAGE_DIRECTORY, filename) #filepath with original extension
    full_save_path = os.path.join(IMAGE_DIRECTORY , short_filename+".png")
    
    if os.path.exists(full_save_path):
        #if file exists already, no need to redownload it. 
        return
    
    # download    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers )
    if not r.ok:
        raise Exception("Unable to download file. Status "+str(r.status_code))
    
    # open from memory    
    try:
        img = Image.open(BytesIO(r.content))  
    except UnidentifiedImageError as e:
        print("\nError catched:")
        print(e)
        print(url, filename)
        exit(1)

    if img.mode != "RGB":    
        img=img.convert("RGB")
    
    #resize
    try:
        ratio = NEW_SIZE / min(img.size[0], img.size[1])
        new_width = int(ratio*img.size[0]) 
        new_height= int(ratio*img.size[1])
        img = img.resize((new_width, new_height), Image.LANCZOS)
    except OSError as e:
        print("\nError catched:")
        print(e)
        print(url, filename)
        return
        
    except ValueError as e:
        print("\nError catched:")
        print(e)
        print(url, img.mode)
        exit(1)
        return    


    #save to file
    
    img.save(full_save_path, "PNG")       
    
    
       
def save_description(txt, filename):
    full_save_path = IMAGE_DIRECTORY + "/" +  filename
    with open(full_save_path, mode="w",encoding="utf-8") as file:
       file.write(txt)

def get_wikidata_organized(qid):    
    wd={}
    wd["label"] = ''
    wd["label_ru"] = ''
    wd["description"]=""
    wd["description_ru"]=""
    wd["instance_of"] = ''
    wd["coordinates"] = None # coordinates may be missing in case object in wikidata is not a building, but 'Q2088357': 'musical ensemble'  for example
    wd["architect"] = ''
    wd["architect_ru"] = ''
    wd["architecture"] = ''
    wd["wikipedia"] = "" 

    wikidata = get_wikidata(qid)
    if not wikidata:
        #this means that error was returned by wikidata API
        return wd
        
    if 'labels' in wikidata: 
        if  'en' in wikidata['labels']:
            wd["label"] = wikidata['labels']['en']['value']
            
        if 'labels' in wikidata and 'ru' in wikidata['labels']:
            wd["label_ru"] = wikidata['labels']['ru']['value']    
        
    if 'descriptions' in wikidata:
        if 'en' in wikidata['descriptions']:
            wd["description"]=wikidata['descriptions']['en']['value']
        
        if 'ru' in wikidata['descriptions']:
            wd["description_ru"]=wikidata['descriptions']['ru']['value']
            
    if 'claims' in wikidata:
        if 'P31' in wikidata['claims']:
            wd["instance_of"] = wikidata['claims']['P31'][0]['mainsnak']['datavalue']['value']['id']
    
        if 'P18' in wikidata['claims'] and 'datavalue' in wikidata['claims']['P18'][0]['mainsnak']:     
            wd["image"] = wikidata['claims']['P18'][0]['mainsnak']['datavalue']['value']
            
        if 'P856' in wikidata['claims']:
            wd["website"] = wikidata['claims']['P856'][0]['mainsnak']['datavalue']['value']
        
        if 'P625' in wikidata['claims']:
            wd["coordinates"] = wikidata['claims']['P625'][0]['mainsnak']['datavalue']['value']

        if 'P571' in wikidata['claims'] and 'datavalue' in wikidata['claims']['P571'][0]['mainsnak']:
            wd["start_date"] = wikidata['claims']['P571'][0]['mainsnak']['datavalue']['value']['time'][1:5]

        
        if 'P84' in wikidata['claims'] and 'datavalue' in wikidata['claims']['P84'][0]['mainsnak']:
            architect_id = wikidata['claims']['P84'][0]['mainsnak']['datavalue']['value']["id"]    
            architect_data = get_wikidata(architect_id)
            
            if 'en' in architect_data['labels']:
                wd["architect"] = architect_data['labels']['en']['value']
            
            if 'ru' in architect_data['labels']:
                wd["architect_ru"] = architect_data['labels']['ru']['value']    
        
        if 'P149' in wikidata['claims'] and 'datavalue' in wikidata['claims']['P149'][0]['mainsnak']:
            wd["architecture"] = wikidata['claims']['P149'][0]['mainsnak']['datavalue']['value']["id"]            
            
        
    if 'sitelinks' in wikidata and 'ruwiki' in wikidata['sitelinks']:    
        wd["wikipedia"] = 'ru:'+wikidata['sitelinks']['ruwiki']['title']
    
    return wd


# ============
# main block 
# ============
def update_region(input_file_name, output_file_name):
   
    all_objects=mdlMisc.loadDatFile(input_file_name) 
    objects_with_wikidata = []
    
    for rec in all_objects:
        if rec[QUADDATA_WIKIDATA_ID] != "" :
            objects_with_wikidata.append(rec)
    n = 0
    for rec in tqdm(objects_with_wikidata):
                 
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
            
            n += 1
            if n>= LIMIT:
                print(f"Limit of {LIMIT} objects has been exceeded")
                break
           

    mdlMisc.saveDatFile(all_objects, output_file_name)
    print (f'{n} objects processed out of {len(objects_with_wikidata)}')
    
def count(a_dict, value):  
    if value not in a_dict:
        a_dict[value] = 0
    a_dict[value] += 1     
 
def print_stats(input_file_name):
    cells=mdlMisc.loadDatFile(input_file_name) 
    
    n=0
    wikidata_buildings_known =  {}
    wikidata_buildings_unknown = {}
    wikidata_architectures = {}
    unmatched_building_types_with_osm = {}
    
    for rec in cells:
        if rec[QUADDATA_WIKIDATA_ID] !="":
            n += 1
            # calculate some usage statistics             
            wikidata = get_wikidata_organized(rec[QUADDATA_WIKIDATA_ID]) 
            wd_building_type =  wikidata_buildings.get(wikidata["instance_of"], '')
            if wd_building_type and wd_building_type != 'building':
                if wd_building_type.upper() not in building_types_rus_names:
                    count(unmatched_building_types_with_osm, wd_building_type.lower())
                else:
                    count(wikidata_buildings_known, wd_building_type.lower())
                
            value = wikidata["instance_of"]
            if value and value not in wikidata_buildings and value not in wikidata_non_buildings:
                count(wikidata_buildings_unknown, value)
                
           
            value = wikidata["architecture"]
            building_architecture =  wikidata_achitecture_styles.get(value,value)
            if building_architecture:
                count(wikidata_architectures, building_architecture)
                
            
            
    print("total objects with wikidata tag: ", n)
            
    
    print()
    print('unrecognized wikidata building types:')    
    print_sorted_dict(wikidata_buildings_unknown,limit=2)
    print('unrecognized wikidata building types total: ', len(wikidata_buildings_unknown))        

    print()
    print("unmatched building types with osm")
    print_sorted_dict(unmatched_building_types_with_osm, limit=4)
    
    print()
    print("wikidata building types")
    print_sorted_dict(wikidata_buildings_known)

    print()
    print("wikidata_architectures:")
    print_sorted_dict(wikidata_architectures,limit=3)
    
    
    
def get_images(input_file_name):
    all_objects = mdlMisc.loadDatFile(input_file_name) 
    objects_with_wikidata = []
    for rec in all_objects:
        if rec[QUADDATA_WIKIDATA_ID]!="" :
            objects_with_wikidata.append (rec)
    
    working_loop = tqdm(objects_with_wikidata)
    n=0
    k=0
    for rec in working_loop:
        if os.path.exists(os.path.join(IMAGE_DIRECTORY , rec[QUADDATA_WIKIDATA_ID]+".png")):
            #if file exists already, no need to redownload it. 
            continue
        n+=1
        building_text_description =  ( 
                rec[QUADDATA_COLOUR] + " " +
                rec[QUADDATA_MATERIAL] + " " +
                rec[QUADDATA_BUILDING_TYPE] + " " +
                rec[QUADDATA_STYLE] + " " +
                rec[QUADDATA_BUILD_DATE] + " " + 
                rec[QUADDATA_ARCHITECT]
                ).strip()
        
        wikidata = get_wikidata_organized(rec[QUADDATA_WIKIDATA_ID])             
        if building_text_description != '' and 'image' in wikidata:
            #building_text_description += " " + wikidata["label"] + " " +wikidata["description"]
            #building_text_description += " " +wikidata["label"]
            #building_text_description = building_text_description.strip()
            
            api_url ="https://commons.wikimedia.org/w/api.php?action=query&format=json" +"&prop=imageinfo&iiprop=url&titles=File:" + wikidata['image']
            #print(rec[QUADDATA_OBJ_TYPE][0]+rec[QUADDATA_OBJ_ID], rec[QUADDATA_WIKIDATA_ID] )
            #print('  ' + building_text_description)
            #print('  ' + wikidata['image'])
            ##print('  ' +'https://commons.wikimedia.org/wiki/File:'+wikidata['image'])
            ##print('  ' + api_url)
            
            # we need to obtain actual download url via api, because it is hidden.           
            image_metadata = get_from_wikimedia_api(api_url)
            for _, yyy in image_metadata["query"]["pages"].items():
                break # we just need one image, and expect only one
            if "imageinfo" in yyy:
                image_download_url = yyy["imageinfo"][0]["url"] 
            else:
                #print('ERROR: wikimedia site did not provided url for the image '+ api_url)
                continue
            #print('  '+str(image_download_url))
            _, extension = os.path.splitext(wikidata['image'])
            download_image(image_download_url, rec[QUADDATA_WIKIDATA_ID] + extension)
            
            #save_description(building_text_description, rec[QUADDATA_WIKIDATA_ID]+'.txt')
            #print()
            k+=1
            
        working_loop.set_description(f"{n} buildings processed, {k} images_downloaded")

def update_quadrant_stats(input_file_name):
    
    stats = {}
    source_path = "d:/_VFR_LANDMARKS_3D_RU/work_folder/21_osm_objects_list"
    with os.scandir(source_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".dat"):
                quadrant_name = entry.name.replace(".dat", "")
                if quadrant_name not in stats:
                    stats[quadrant_name] = {'total': 0, 'photos': 0}
                
                records = mdlMisc.loadDatFile(os.path.join(source_path, entry.name))
                for rec in records:
                    stats[quadrant_name]['total'] += 1
                    if rec[QUADDATA_WIKIDATA_ID] and os.path.exists(os.path.join(IMAGE_DIRECTORY , rec[QUADDATA_WIKIDATA_ID]+".png")):
                        stats[quadrant_name]['photos'] += 1

    # miracle: update totals file
    totals = mdlMisc.loadDatFile(input_file_name)

    # filter by quadrant name
    for i in range(len(totals)):
        # verify that all necessary fields are present
        totals[i] += ["0"] * (10 - len(totals[i]))
        quadrant_name = totals[i][0]
        if quadrant_name in stats:
            totals[i][2] = str(stats[quadrant_name]['total']) # Update total objects from regional file
            totals[i][9] = str(stats[quadrant_name]['photos'])
            
    mdlMisc.saveDatFile(totals, input_file_name)
    print("Quadrant stats updated")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='wikidata',
        description='this script is a part of 3DCHECK/VFR_LANDMARKS_3D_RU pipeline',
        epilog='Created by zkir (c) 2024')
        
    parser.add_argument('command', choices=['update-region', 'get-images', 'print-stats', 'update-quad-stats'],  help='update-region updates region from wikidata, \n get-images gets images from wikimedia commons' )
    parser.add_argument('-i', '--input', required=True, type=str, help='input file, should be dat-csv file' )
    parser.add_argument('-r', '--rewrite', required=False, action='store_true', help='rewrite the input file with updated data' )
    parser.add_argument('-o', '--output', required=False, type=str, help='output osm-xml with created parts' )
    
    args = parser.parse_args()

    command=args.command
    input_file_name = args.input
    output_file_name = args.output
    
    if not output_file_name:
        if args.rewrite:
            output_file_name = input_file_name
        else:
            output_file_name = input_file_name + '-rewrite.dat'
    
    if not os.path.exists(input_file_name):
        print("ERROR: specified input file does not exist: " + input_file_name )
        exit(1)
        
    if command == 'update-region':
        update_region(input_file_name, output_file_name)
    elif command == 'get-images':
        get_images(input_file_name)
    elif command == 'print-stats':
        print_stats(input_file_name)
    elif command == 'update-quad-stats':
        update_quadrant_stats(input_file_name)
    else:
        print("unknown command " + command )
    



