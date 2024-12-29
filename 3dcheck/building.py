#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
import time 
from mdlMisc import *
import os.path
import json
from mdlClassify import buildingTypeRus, achitectureStylesRus
from misc2 import region_names
import cgi

#========================================================================
#  Web Page for individual object, with 3d model
#========================================================================
def CreateObjectPage(strQuadrantName,obj_rec, page_time_stamp, validation_errors, urlPrevious, urlNext, urlTop):
    strHTMLPage = ""
    strOSMurl = ""
    strF4url = ""
    strTemplesUrl = ""
    strTemplesID = ""
    strJOSMurl = ""
    strWikipediaLink = ""    

    lat=(float(obj_rec[3])+float(obj_rec[5]))/2
    lon=(float(obj_rec[4])+float(obj_rec[6]))/2

    strOsmID = UCase(Left(obj_rec[1],1)) + obj_rec[2]

    strOSMurl = 'https://www.openstreetmap.org/' + LCase(obj_rec[1]) + '/' + obj_rec[2]
    strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
    strOsmBurl = 'http://osmbuildings.org/?lat='+ str(lat) +'&lon=' + str(lon) + '&zoom=19.0'

    strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ obj_rec[4] + "&right="+ obj_rec[6] + "&top="+ obj_rec[5] +"&bottom="+ obj_rec[3] #"&select=object"
    strTemplesID = obj_rec[9]
    if strTemplesID !="":
        strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

    strWikipediaLink = ''

    if Trim(obj_rec[17]) != '':
        strWikipediaLink = 'http://ru.wikipedia.org/wiki/' + obj_rec[17]
    
    #name of wikipedia article. we need to remove object name
    strWikipediaName=Mid(obj_rec[17], 4)
    
    strObjectName=obj_rec[7]
    if strObjectName=="" and strWikipediaName!="":
        strObjectName=strWikipediaName
        
    if strObjectName == '':
        strObjectName = '&lt;&lt;' + buildingTypeRus(obj_rec[10]).upper() + '&gt;&gt;'    
    
    strStars=''
    intNumberOfParts=int(obj_rec[24])
    if intNumberOfParts>25:
       strStars='★'
    if intNumberOfParts>100:
       strStars='★★'
    if intNumberOfParts>1000:
       strStars='★★★'
       
    strSoboryID   = obj_rec[27]
    if strSoboryID !="":
        strSoboryUrl="https://sobory.ru/article/?object=" +strSoboryID 
    else: 
        strSoboryUrl = ""
    
    strWikidata   = obj_rec[28]
    if strWikidata !="":
        strWikidataLink = "https://www.wikidata.org/wiki/"+strWikidata
    else:
        strWikidataLink = ""
    strArchitect   = obj_rec[29]
  
    print( '<!doctype html>'+ '\n')
    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    print( '  <title>' + strObjectName  +'</title>'+ '\n')
    #print( '  <meta encoding=\'utf-8\' />'+ '\n')
    print( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    ##print ( "  <script src='https://x3dom.org/release/x3dom.js'></script>")
    ##print ( "  <link rel='stylesheet' href='https://x3dom.org/release/x3dom.css' />")
    print( '  <script src=\'/x3dom/x3dom.js\'></script>'+ '\n')
    print( '  <link rel=\'stylesheet\' href=\'/x3dom/x3dom.css\' />'+ '\n')
    
    print( '  <script>'+ '\n')
    print( '    function fitCamera()'+ '\n')
    print( '    {'+ '\n')
    print( '       var x3dElem = document.getElementById(\'x3dElem\');'+ '\n')
    print( '       x3dElem.runtime.showAll(\'posX\');'+ '\n')
    print( '    }'+ '\n')
    print( '    function fitCamera2()'+ '\n')
    print( '    {'+ '\n')
    print( '       var x3dElem = document.getElementById(\'x3dElem2\');'+ '\n')
    print( '       x3dElem.runtime.showAll(\'posX\');'+ '\n')
    print( '    }'+ '\n')
    print( '  </script>'+ '\n')
    print( '  <link rel="stylesheet" type="text/css" href="/css/style5.css" />'+ '\n')
    print( '  <script src="/js/modernizr.custom.js"></script>'+ '\n')
    print( '  <link rel="stylesheet" type="text/css" href="/css/building.css" />'+ '\n')
    print( '</head>'+ '\n')
    print( '<body class=\'page\'>'+ '\n')
    print( '  <div class=\'page-header\'>'+ '\n')
    strPageTitle=strObjectName + ' '  +strStars # ' (' + strOsmID + ') '
    print( '    <h1 title="'+strPageTitle+'">' + strPageTitle + '</h1>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-content\'>'+ '\n')

    print( '  <div class=\'descr\'  >'+ '\n')
    print( '  <table style=\'padding:15px;\'>'+ '\n')
    print( '  <tr><td>Тип здания:  </td><td>' + buildingTypeRus(obj_rec[10]) + '</td></tr>'+ '\n')
    if obj_rec[8] != "":
        print( '  <tr><td>Описание:  </td><td>' + obj_rec[8] + '</td></tr>'+ '\n')
    print( '  <tr><td>Год постройки: </td><td>' + obj_rec[16] + '</td></tr>'+ '\n')
    print( '  <tr><td>Стиль: </td><td>' + achitectureStylesRus(obj_rec[15]) + '</td></tr>'+ '\n')
    if strArchitect != "":    
        print( '  <tr><td>Архитектор: </td><td>' + strArchitect + '</td></tr>'+ '\n')
    print( '  <tr><td>Размер, м : </td><td>' + obj_rec[11] + '</td></tr>'+ '\n')
    print( '  <tr><td>Высота, м : </td><td>' + obj_rec[12] + '</td></tr>'+ '\n')
    print( '  <tr><td>Цвет:  </td><td>' + obj_rec[13] + '</td></tr>'+ '\n')
    print( '  <tr><td>Материал: </td><td>' + obj_rec[14] + '</td></tr>'+ '\n')
    print( '  <tr><td>Адрес:</td><td>' + obj_rec[18] + ' ' + obj_rec[19] + '</td></tr>'+ '\n')
    print( '  <tr><td>Город:</td><td>' + obj_rec[20] + '</td></tr>'+ '\n')
    if obj_rec[21] != "":    
        print( '  <tr><td>Район:</td><td>' + obj_rec[21] + '</td></tr>'+ '\n')
    print( '  <tr><td>Область:</td><td>' + obj_rec[22] + '</td></tr>'+ '\n')
    print( '  <tr><td>Lat: </td><td>' + str(lat) + '</td></tr>'+ '\n')
    print( '  <tr><td>Lon: </td><td>' + str(lon) + '</td></tr>'+ '\n')
    print( '  <tr><td>Osm Id: </td><td><a href=\'' + strOSMurl + '\'> ' + strOsmID + '</a></td></tr>'+ '\n')
    if strWikipediaLink != '':
        print( '  <tr><td>Википедия:</td><td><a target=\'_blank\' href=\'' + strWikipediaLink + '\'>' + Mid(obj_rec[17], 4) + '</a></td></tr>'+ '\n')
        
    if strWikidata != "":    
        print( '  <tr><td>Викидата:</td><td><a target=\'_blank\' href=\'' + strWikidataLink + '\'>' + strWikidata + '</a></td></tr>'+ '\n')    
        
    if strTemplesID != "":    
        print( '  <tr><td>temples.ru:</td><td><a target=\'_blank\' href=\'' + strTemplesUrl + '\'>' + strTemplesID + '</a></td></tr>'+ '\n')
        
    if strSoboryID != "":    
        print( '  <tr><td>sobory.ru:</td><td><a target=\'_blank\' href=\'' + strSoboryUrl + '\'>' + strSoboryID + '</a></td></tr>'+ '\n')    
        
    
        
        
        
    print( '  <tr><td>F4 Map</td><td><a target=\'_blank\' href=\'' + strF4url + '\'>' + 'demo.f4map.com' + '</a></td></tr>'+ '\n')
    #osmbuildings are blocked in RF
    #print( '  <tr><td>Osm Buildings</td><td><a target=\'_blank\' href=\'' + strOsmBurl + '\'>' + 'osmbuildings.org' + '</a></td></tr>'+ '\n')
    print( '  <tr><td>Число частей:</td><td>'+obj_rec[24]+strStars+'</td></tr>'+ '\n')
    print( '  <tr><td>Дата редактирования:</td><td>'+obj_rec[25][0:10]+'</td></tr>'+ '\n')
    
    n_errors=int(obj_rec[26])
    if n_errors > 0:
        print( '  <tr><td>Ошибки валидации:</td><td><a href="'+strOsmID+'/errors"> '+str(n_errors)+'</a></td></tr>'+ '\n')
    else:
        print( '  <tr><td>Ошибки валидации:</td><td> 0 </td></tr>'+ '\n')
    print( '  <tr><td colspan="2"><br/><b><center>*<a target="josm" href="' + strJOSMurl + '">Редактировать в JOSM</a>*</center></b></td></tr>'+ '\n')
    print( '  </table>'+ '\n')
    print( '   '+ '\n')
    print( '  </div>'+ '\n')

    print( '    <div class=\'scene\' >'+ '\n')
    if obj_rec[23] == "True":
        print( '      <div class=\'x3d-content\'>'+ '\n')
        print( '        <x3d id=\'x3dElem\' x=\'0px\' y=\'0px\' width=\'100%\' height=\'100%\'>'+ '\n')
        print( '          <scene>'+ '\n')
        if strQuadrantName == "TOP_WINDOWS":
            print( "            <inline onload='fitCamera()' url='/data/models2/" + strOsmID + ".x3d'></inline>" + "\n")
        else:
            print( "            <inline onload='fitCamera()' url='/data/models/" + strOsmID + ".x3d'></inline>" + "\n")
        
        print( '          </scene>'+ '\n')
        print( '        </x3d>'+ '\n')
        print( '      </div>'+ '\n')
    else:
        if obj_rec[28]:
            print( '      <div class=\'no_model\'>'+ '\n')
            print( '           <img src=\'/data/building_images/'+obj_rec[28]+'.png\'  height=\'512px\' alt=\'3d Модель отсутствует\' ><img> '+ '\n')
            print( '      </div>'+ '\n')
        else:
            print( '      <div class=\'no_model\'>'+ '\n')
            print( '           <img src=\'/nomodel.gif\' width=\'450px\' height=\'450px\' alt=\'3d Модель отсутствует\' ><img> '+ '\n')
            print( '      </div>'+ '\n')
    if strQuadrantName == "TOP_WINDOWS":        
        print( '       <button id="trigger-overlay" type="button">blosm</button>'+ '\n')
    else: 
        print( '       <button id="trigger-overlay" type="button">Osm2World</button>'+ '\n')
    print( '    </div>'+ '\n')

    print( '  <div style=\'clear:both;\'></div>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-footer\'>'+ '\n')
    print( '  <div class=\'navigation\'>'+ '\n')
    print( '<hr />'+ '\n')
    #urlPrevious, urlNext
    #print( '<center>')
    print( '  <a href="'+urlPrevious+'"> << Предыдущее </a> -- \n')
    print( '  <a href=\'/\'>Главная страница</a> --> <a href=\'' + urlTop + '\'>' + region_names.get(strQuadrantName, strQuadrantName) + '</a>'+ '\n')
    print( '  -- <a href="'+urlNext+'"> Следущее >> </a> \n')
    #print( '</center>')
    print( '  </div>'+ '\n')
    #zero frame for josm links
    print( '<div style="display: none;"><iframe name="josm"></iframe></div>'+ '\n')
    print( '<hr />'+ '\n')
    print( '<p>Дата формирования страницы: ' + page_time_stamp + '</p>'+ '\n')    
    print( '  </div>'+ '\n')
    print( '<!-- open/close -->'+ '\n')
    print( '    <div class="overlay overlay-scale">'+ '\n')
    print( '      <button type="button" class="overlay-close">Close</button>'+ '\n')
    print( '      <div style="position: absolute;top:5px;  left:20px; color: black; z-index: 100;">'+ '\n')
    print( '       <h1>' + strObjectName + ' (' + strOsmID + ') ' +strStars+ '</h1>'+ '\n')
    print( '       <p>'+obj_rec[22]+', '+obj_rec[20]+', '+ obj_rec[18]+' '+  obj_rec[19]+'</p>  '+ '\n')
    print( '       <p>Число частей:'+obj_rec[24]+'</p>'+ '\n')
    print( '      </div>'+ '\n')
    print( '      <x3d id=\'x3dElem2\' x=\'0px\' y=\'0px\' width=\'100%\' height=\'100%\'>'+ '\n')
    print( '               <scene>'+ '\n')
    
    #print( "                   <inline onload='fitCamera2()' url='/data/models_gltf/" + strOsmID + ".gltf'></inline>" + "\n")
    if strQuadrantName == "TOP_WINDOWS":
        print( "                   <inline onload='fitCamera2()' url='/data/models/" + strOsmID + ".x3d'></inline>" + "\n")
    else: 
        print( "                   <inline onload='fitCamera2()' url='/data/models2/" + strOsmID + ".x3d'></inline>" + "\n")
    print( '               </scene>'+ '\n')
    print( '      </x3d>'+ '\n')
    print( '    </div>'+ '\n')
    print( '    <script src="/js/classie.js"></script>'+ '\n')
    print( '    <script src="/js/demo1.js"></script>'+ '\n')

    print('''<!-- Yandex.Metrika counter -->
             <script type="text/javascript" >
             (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
             m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
             (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
             ym(65563393, "init", {
             clickmap:true,
             trackLinks:true,
             accurateTrackBounce:true
             });
             </script>
             <noscript><div><img src="https://mc.yandex.ru/watch/65563393" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
             <!-- /Yandex.Metrika counter -->''')

    print( '</body>'+ '\n')
    print( '</html>'+ '\n')




sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print ()


url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
strParam=urlparse.parse_qs(parsed.query).get('param','')
s=url.split("/")

#if len(s)>=2:
#    strQuadrantName=s[3].strip()
#    intObjectIndex=s[4]#[0:-5]
#    #print(intObjectIndex) 
#else:
#    strQuadrantName= "TOP" # "RU-MOW"
#    intObjectIndex= "R1645496" # "R3030568"
strCountry      = cgi.FieldStorage().getvalue('country')    
strQuadrantName = cgi.FieldStorage().getvalue('quadrant')    
intObjectIndex  = cgi.FieldStorage().getvalue('object')    

QN={'building_top':         'TOP',
    'building_top_windows': 'TOP_WINDOWS',
    'recent_changes':       'LATEST',
    'no_type':              'photo_wo_type' 
    }
strQuadrantName= QN.get(strQuadrantName, strQuadrantName)

if strCountry:
    strInputFile = "data\\countries\\"+strCountry+"\\"+strQuadrantName+".dat"
else:    
    strInputFile = "data\\world\\"+strQuadrantName+".dat"

if not os.path.exists(strInputFile):
    print(f'File {strInputFile} does not exist')
    exit()

cells = loadDatFile(strInputFile)
page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)


# sort by number of building parts - we need it for proper navigation 
if strQuadrantName != "LATEST":
    cells.sort(key=lambda row: int(row[24]), reverse=True)
else:
    pass
    #for the latest changes list is already sorted by date    
    
idx=0    
for rec in cells:
    if UCase(Left(rec[1],1)) + rec[2] == intObjectIndex:
       obj_rec = rec
       break  
    idx += 1   
        
#validation errors
validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'




if os.path.exists(validation_errors_file_name):
    with open(validation_errors_file_name) as f:
        validation_errors = json.load(f)
else:
    validation_errors = []
    
#print(idx,len(cells))

#urlTop = '/countries/' + strQuadrantName 
urlTop = '.'

if idx>0:      
    urlPrevious = UCase(Left(cells[idx-1][1],1)) + cells[idx-1][2] + ''  
else:
    urlPrevious = urlTop


if idx+1<len(cells):
    urlNext =   UCase(Left(cells[idx+1][1],1)) + cells[idx+1][2] + '' #cells[idx+1]
else:     
    urlNext =  urlTop
    
CreateObjectPage(strQuadrantName, obj_rec, page_time_stamp, validation_errors, urlPrevious, urlNext, urlTop)