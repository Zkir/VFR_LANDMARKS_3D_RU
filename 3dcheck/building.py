#!c:\Program Files\Python37\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *

#========================================================================
#  Web Page for individual object, with 3d model
#========================================================================
def CreateObjectPage(strQuadrantName,cells, intObjectIndex):
    strHTMLPage = ""
    strOsmID = ""
    strOSMurl = ""
    strF4url = ""
    strTemplesUrl = ""
    strTemplesID = ""
    i = 0
    strJOSMurl = ""
    strWikipediaLink = ""
    i = intObjectIndex

    lat=(float(cells[i][3])+float(cells[i][5]))/2
    lon=(float(cells[i][4])+float(cells[i][6]))/2

    strOsmID = UCase(Left(cells[intObjectIndex][1],1)) + cells[intObjectIndex][2]

    strOSMurl = 'https://www.openstreetmap.org/' + LCase(cells[i][1]) + '/' + cells[i][2]
    strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
    strOsmBurl = 'http://osmbuildings.org/?lat='+ str(lat) +'&lon=' + str(lon) + '&zoom=19.0'

    strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ cells[i][4] + "&right="+ cells[i][6] + "&top="+ cells[i][5] +"&bottom="+ cells[i][3] #"&select=object"
    strTemplesID = cells[i][9]
    if strTemplesID !="":
        strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

    strWikipediaLink = ''

    if Trim(cells[intObjectIndex][17]) != '':
        strWikipediaLink = 'http://ru.wikipedia.org/wiki/' + cells[intObjectIndex][17]
    
    #name of wikipedia article. we need to remove object name
    strWikipediaName=Mid(cells[intObjectIndex][17], 4)
    
    strObjectName=cells[intObjectIndex][7]
    if strObjectName=="" and strWikipediaName!="":
        strObjectName=strWikipediaName
    
    strStars=''
    intNumberOfParts=int(cells[intObjectIndex][24])
    if intNumberOfParts>25:
       strStars='★'
    if intNumberOfParts>100:
       strStars='★★'
    if intNumberOfParts>1000:
       strStars='★★★'
  
    print( '<!doctype html>'+ '\n')
    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    print( '  <title>' + strObjectName  +'</title>'+ '\n')
    #print( '  <meta encoding=\'utf-8\' />'+ '\n')
    print( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    #Print #4, "  <script src='http://x3dom.org/release/x3dom.js'></script>"
    #Print #4, "  <link rel='stylesheet' href='http://x3dom.org/release/x3dom.css' />"
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
    print( '</head>'+ '\n')
    print( '<body class=\'page\'>'+ '\n')
    print( '  <div class=\'page-header\'>'+ '\n')
    print( '    <h1>' + strObjectName + ' (' + strOsmID + ') ' +strStars+ '</h1>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-content\'>'+ '\n')
    print( '    <div class=\'scene\' style=\'height:520px; width:510px;float:left\'>'+ '\n')
    if cells[i][23] == "True":
        print( '      <div class=\'x3d-content\'>'+ '\n')
        print( '        <x3d id=\'x3dElem\' x=\'0px\' y=\'0px\' width=\'500px\' height=\'500px\'>'+ '\n')
        print( '          <scene>'+ '\n')
        print( "            <inline onload='fitCamera()' url='/models/" + strOsmID + ".x3d'></inline>" + "\n")
        print( '          </scene>'+ '\n')
        print( '        </x3d>'+ '\n')
        print( '      </div>'+ '\n')
    else:
        print( '      <div class=\'no_model\'>'+ '\n')
        print( '           <img src=\'/nomodel.gif\' width=\'450px\' height=\'450px\' alt=\'3d Модель отсутствует\' ><img> '+ '\n')
        print( '      </div>'+ '\n')
    print( '       <center><button id="trigger-overlay" type="button">На весь экран</button> </center>'+ '\n')
    print( '    </div>'+ '\n')
    print( '  <div class=\'Description\' style=\'float:left\' >'+ '\n')
    print( '  <table style=\'padding-left:15px\'>'+ '\n')
    print( '  <tr><td>Тип здания:  </td><td>' + cells[intObjectIndex][10] + '</td></tr>'+ '\n')
    print( '  <tr><td>Описание:  </td><td>' + cells[intObjectIndex][8] + '</td></tr>'+ '\n')
    print( '  <tr><td>Год постройки: </td><td>' + cells[intObjectIndex][16] + '</td></tr>'+ '\n')
    print( '  <tr><td>Стиль: </td><td>' + cells[intObjectIndex][15] + '</td></tr>'+ '\n')
    print( '  <tr><td>Размер, м : </td><td>' + cells[intObjectIndex][11] + '</td></tr>'+ '\n')
    print( '  <tr><td>Высота, м : </td><td>' + cells[intObjectIndex][12] + '</td></tr>'+ '\n')
    print( '  <tr><td>Цвет:  </td><td>' + cells[intObjectIndex][13] + '</td></tr>'+ '\n')
    print( '  <tr><td>Материал: </td><td>' + cells[intObjectIndex][14] + '</td></tr>'+ '\n')
    print( '  <tr><td>Адрес:</td><td>' + cells[intObjectIndex][18] + ' ' + cells[intObjectIndex][19] + '</td></tr>'+ '\n')
    print( '  <tr><td>Город:</td><td>' + cells[intObjectIndex][20] + '</td></tr>'+ '\n')
    print( '  <tr><td>Район:</td><td>' + cells[intObjectIndex][21] + '</td></tr>'+ '\n')
    print( '  <tr><td>Область:</td><td>' + cells[intObjectIndex][22] + '</td></tr>'+ '\n')
    print( '  <tr><td>Lat: </td><td>' + str(lat) + '</td></tr>'+ '\n')
    print( '  <tr><td>Lon: </td><td>' + str(lon) + '</td></tr>'+ '\n')
    print( '  <tr><td>Osm Id: </td><td><a href=\'' + strOSMurl + '\'> ' + strOsmID + '</a></td></tr>'+ '\n')
    if strWikipediaLink != '':
        print( '  <tr><td>Википедия:</td><td><a target=\'_blank\' href=\'' + strWikipediaLink + '\'>' + Mid(cells[intObjectIndex][17], 4) + '</a></td></tr>'+ '\n')
    print( '  <tr><td>temples.ru:</td><td><a target=\'_blank\' href=\'' + strTemplesUrl + '\'>' + strTemplesID + '</a></td></tr>'+ '\n')
    print( '  <tr><td>F4 Map</td><td><a target=\'_blank\' href=\'' + strF4url + '\'>' + 'demo.f4map.com' + '</a></td></tr>'+ '\n')
    print( '  <tr><td>Osm Buildings</td><td><a target=\'_blank\' href=\'' + strOsmBurl + '\'>' + 'osmbuildings.org' + '</a></td></tr>'+ '\n')
    print( '  <tr><td>Число частей:</td><td>'+cells[intObjectIndex][24]+strStars+'</td></tr>'+ '\n')

    print( '  <tr><td colspan="2"><br/><b><center>*<a target="josm" href="' + strJOSMurl + '">Редактировать в JOSM</a>*</center></b></td></tr>'+ '\n')
    print( '  </table>'+ '\n')
    print( '   '+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div style=\'clear:both;\'></div>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-footer\'>'+ '\n')
    print( '  <div class=\'navigation\'>'+ '\n')
    print( '<hr />'+ '\n')
    print( '  <a href=\'/\'>Главная страница</a> --> <a href=\'/' + strQuadrantName + '.html\'>' + strQuadrantName + '</a>'+ '\n')
    print( '  </div>'+ '\n')
    #zero frame for josm links
    print( '<div style="display: none;"><iframe name="josm"></iframe></div>'+ '\n')
    print( '<hr />'+ '\n')
    print( '<p>Дата формирования страницы: ' + getTimeStamp() + '</p>'+ '\n')
    print( '  </div>'+ '\n')
    print( '<!-- open/close -->'+ '\n')
    print( '    <div class="overlay overlay-scale">'+ '\n')
    print( '      <button type="button" class="overlay-close">Close</button>'+ '\n')
    print( '      <div style="position: absolute;top:5px;  left:20px; color: black; z-index: 100;">'+ '\n')
    print( '       <h1>' + strObjectName + ' (' + strOsmID + ') ' +strStars+ '</h1>'+ '\n')
    print( '       <p>'+cells[intObjectIndex][22]+', '+cells[intObjectIndex][20]+', '+ cells[intObjectIndex][18]+' '+  cells[intObjectIndex][19]+'</p>  '+ '\n')
    print( '       <p>Число частей:'+cells[intObjectIndex][24]+'</p>'+ '\n')
    print( '      </div>'+ '\n')
    print( '      <x3d id=\'x3dElem2\' x=\'0px\' y=\'0px\' width=\'100%\' height=\'100%\'>'+ '\n')
    print( '               <scene>'+ '\n')
    #print( '                  <inline onload=\'fitCamera2()\' url=\'R3881262.x3d\'></inline>'+ '\n')
    print( "                   <inline onload='fitCamera2()' url='/models/" + strOsmID + ".x3d'></inline>" + "\n")
    print( '               </scene>'+ '\n')
    print( '      </x3d>'+ '\n')
    print( '    </div>'+ '\n')
    print( '    <script src="/js/classie.js"></script>'+ '\n')
    print( '    <script src="/js/demo1.js"></script>'+ '\n')

    print( '</body>'+ '\n')
    print( '</html>'+ '\n')




sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print


url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
strParam=urlparse.parse_qs(parsed.query).get('param','')

s=url.split("/")

if len(s)>=2:
    strQuadrantName=s[1].strip()
    intObjectIndex=s[2][0:-5]
    #print(intObjectIndex) 
else:
    strQuadrantName="RU-MOW"
    intObjectIndex="R3030568"

cells = loadDatFile("data\\"+strQuadrantName+".dat")
for i in range(len(cells)):
    if UCase(Left(cells[i][1],1)) + cells[i][2] == intObjectIndex:
       intObjectIndex=i
       break  
    

CreateObjectPage(strQuadrantName, cells, intObjectIndex)