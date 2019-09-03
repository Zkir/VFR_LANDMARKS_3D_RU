from vbFunctions import *
from mdlMisc import *
from mdlGeocoder import *


"""****************************************************
 xls sheet is analysed and saved as html page
****************************************************
"""
class TSummaryRec:

    def __init__(self):
        self.DistrictName = ""

        self.RegionName = ""
        self.TotalObjects = 0  
        self.ObjectsWith3D = 0


BUILD_PATH = 'd:\\_VFR_LANDMARKS_3D_RU'
GEOCODER_SOURCE_OSM = "d:\\_planet.osm\\geocoder.osm"



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

    strHTMLPage = BUILD_PATH + '\\work_folder\\'+ strQuadrantName +'\\osm_3dmodels\\' + strOsmID + '.html'
    fo=open(strHTMLPage, 'w', encoding="utf-8") 
    fo.write( '<!doctype html>'+ '\n')
    fo.write( '<html>'+ '\n')
    fo.write( '<head>'+ '\n')
    fo.write( '  <title>' + cells[intObjectIndex][7] + '</title>'+ '\n')
    #fo.write( '  <meta encoding=\'utf-8\' />'+ '\n')
    fo.write( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    #Print #4, "  <script src='http://x3dom.org/release/x3dom.js'></script>"
    #Print #4, "  <link rel='stylesheet' href='http://x3dom.org/release/x3dom.css' />"
    fo.write( '  <script src=\'/x3dom/x3dom.js\'></script>'+ '\n')
    fo.write( '  <link rel=\'stylesheet\' href=\'/x3dom/x3dom.css\' />'+ '\n')
    fo.write( '  <script>'+ '\n')
    fo.write( '    function fitCamera()'+ '\n')
    fo.write( '    {'+ '\n')
    fo.write( '       var x3dElem = document.getElementById(\'x3dElem\');'+ '\n')
    fo.write( '       x3dElem.runtime.showAll(\'posX\');'+ '\n')
    fo.write( '    }'+ '\n')
    fo.write( '  </script>'+ '\n')
    fo.write( '</head>'+ '\n')
    fo.write( '<body class=\'page\'>'+ '\n')
    fo.write( '  <div class=\'page-header\'>'+ '\n')
    fo.write( '    <h1>' + strObjectName + ' (' + strOsmID + ')</h1>'+ '\n')
    fo.write( '  </div>'+ '\n')
    fo.write( '  <div class=\'page-content\'>'+ '\n')
    fo.write( '    <div class=\'scene\' style=\'height:510px; width:510px;float:left\'>'+ '\n')
    if cells[i][23] == "True":
        fo.write( '      <div class=\'x3d-content\'>'+ '\n')
        fo.write( '        <x3d id=\'x3dElem\' x=\'0px\' y=\'0px\' width=\'500px\' height=\'500px\'>'+ '\n')
        fo.write( '          <scene>'+ '\n')
        fo.write( '            <inline onload=\'fitCamera()\' url=\'' + strOsmID + '.x3d\'></inline>'+ '\n')
        fo.write( '          </scene>'+ '\n')
        fo.write( '        </x3d>'+ '\n')
        fo.write( '      </div>'+ '\n')
    else:
        fo.write( '      <div class=\'no_model\'>'+ '\n')
        fo.write( '           <img src=\'/nomodel.gif\' width=\'450px\' height=\'450px\' alt=\'3d Модель отсутствует\' ><img> '+ '\n')
        fo.write( '      </div>'+ '\n')
    fo.write( '    </div>'+ '\n')
    fo.write( '  <div class=\'Description\' style=\'float:left\' >'+ '\n')
    fo.write( '  <table style=\'padding-left:15px\'>'+ '\n')
    fo.write( '  <tr><td>Тип здания:  </td><td>' + cells[intObjectIndex][10] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Описание:  </td><td>' + cells[intObjectIndex][8] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Год постройки: </td><td>' + cells[intObjectIndex][16] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Стиль: </td><td>' + cells[intObjectIndex][15] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Размер, м : </td><td>' + cells[intObjectIndex][11] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Высота, м : </td><td>' + cells[intObjectIndex][12] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Цвет:  </td><td>' + cells[intObjectIndex][13] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Материал: </td><td>' + cells[intObjectIndex][14] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Адрес:</td><td>' + cells[intObjectIndex][18] + ' ' + cells[intObjectIndex][19] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Город:</td><td>' + cells[intObjectIndex][20] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Район:</td><td>' + cells[intObjectIndex][21] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Область:</td><td>' + cells[intObjectIndex][22] + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Lat: </td><td>' + str(lat) + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Lon: </td><td>' + str(lon) + '</td></tr>'+ '\n')
    fo.write( '  <tr><td>Osm Id: </td><td><a href=\'' + strOSMurl + '\'> ' + strOsmID + '</a></td></tr>'+ '\n')
    if strWikipediaLink != '':
        fo.write( '  <tr><td>Википедия:</td><td><a target=\'_blank\' href=\'' + strWikipediaLink + '\'>' + Mid(cells[intObjectIndex][17], 4) + '</a></td></tr>'+ '\n')
    fo.write( '  <tr><td>temples.ru:</td><td><a target=\'_blank\' href=\'' + strTemplesUrl + '\'>' + strTemplesID + '</a></td></tr>'+ '\n')
    fo.write( '  <tr><td>F4 Map</td><td><a target=\'_blank\' href=\'' + strF4url + '\'>' + 'demo.f4map.com' + '</a></td></tr>'+ '\n')
    fo.write( '  <tr><td colspan="2"><br/><b><center>*<a target="josm" href="' + strJOSMurl + '">Редактировать в JOSM</a>*</center></b></td></tr>'+ '\n')
    fo.write( '  </table>'+ '\n')
    fo.write( '   '+ '\n')
    fo.write( '  </div>'+ '\n')
    fo.write( '  <div style=\'clear:both;\'></div>'+ '\n')
    fo.write( '  </div>'+ '\n')
    fo.write( '  <div class=\'page-footer\'>'+ '\n')
    fo.write( '  <div class=\'navigation\'>'+ '\n')
    fo.write( '<hr />'+ '\n')
    fo.write( '  <a href=\'/\'>Главная страница</a> --> <a href=\'/' + strQuadrantName + '.html\'>' + strQuadrantName + '</a>'+ '\n')
    fo.write( '  </div>'+ '\n')
    #zero frame for josm links
    fo.write( '<div style="display: none;"><iframe name="josm"></iframe></div>'+ '\n')
    fo.write( '<hr />'+ '\n')
    fo.write( '<p>Дата формирования страницы: ' + getTimeStamp() + '</p>'+ '\n')
    fo.write( '  </div>'+ '\n')
    fo.write( '</body>'+ '\n')
    fo.write( '</html>'+ '\n')
    fo.close()



def GetSummary(cells):
    summary = [] 
    total= TSummaryRec()
    total.DistrictName = ""
    total.RegionName= "Всего в квадрате"
    total.TotalObjects = 0
    total.ObjectsWith3d= 0

    for i in range(len(cells)):
        #find existing record
        blnFound=False
        for j in range(len(summary)):  
            if summary[j].DistrictName == cells[i][21] and summary[j].RegionName == cells[i][22] :
                sumrec = summary[j]  
                blnFound = True
                break  
        if not blnFound:
            sumrec= TSummaryRec()
            sumrec.DistrictName = cells[i][21]
            sumrec.RegionName= cells[i][22]
            sumrec.TotalObjects = 0
            sumrec.ObjectsWith3d = 0
            summary.append (sumrec) 
          
        sumrec.TotalObjects=sumrec.TotalObjects+1
        total.TotalObjects=total.TotalObjects+1

        if cells[i][23] == "True": 
            sumrec.ObjectsWith3D=sumrec.ObjectsWith3D+1
            total.ObjectsWith3D=total.ObjectsWith3D+1

    # sort alphabetically
    summary.sort(key=lambda row: row.RegionName, reverse=False)
    summary.insert(0, total)
    return summary

#========================================================================
#  Web Page for Area(quadrant) summary
#========================================================================

def CreateRegionSummaryPage(dsfLat, dsfLon):
    strHTMLPage = ""

    i = 0
    strOsmID = ""
    strModelUrl = ""
    strF4url = ""
    strOSMurl = ""
    strTemplesUrl = ""
    strTemplesID = ""
    strJOSMurl = ""
    strDescription = ""
    strDistrict = ""
    strQuadrantName = ""

    dblPercentage = 0
    strQuadrantName = composeQuadrantName(dsfLat, dsfLon)

    strInputFile="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\" + strQuadrantName +"\\" + strQuadrantName + ".dat"
    

    cells = loadDatFile(strInputFile)


    # ==========================================================================
    # find addresses of our osm-objects
    # ==========================================================================
    if len(cells)>0:
        print("Loading geocoder...")
        t1 = time.time()
        geocoder = Geocoder()
        geocoder.loadDataFromOsmFile(GEOCODER_SOURCE_OSM)
        t2 = time.time()
        print("Geocoder loaded in " + str(t2 - t1) + " seconds")

        for i in range(len(cells)):
            lat = (float(cells[i][3]) + float(cells[i][5])) / 2
            lon = (float(cells[i][4]) + float(cells[i][6])) / 2
            geocodes = geocoder.getGeoCodes(lat, lon)
            cells[i][20] = geocodes.get('place', '')  # город
            cells[i][21] = geocodes.get('adminlevel_6', '')  # район
            cells[i][22] = geocodes.get('adminlevel_4', '')  # область
        t3 = time.time()
        # we still need to save results, we will need them in future.
        saveDatFile(cells, strInputFile)
        print("objects geocoded in " + str(t3 - t2) + " seconds")
    else:
        print("No objects, geocoding skipped")
    # ==========================================================================
    # sort by number of building parts
    # ==========================================================================
    cells.sort(key=lambda row: int(row[24]), reverse=True)

    #==========================================================================
    # create individual object pages
    #==========================================================================

    for i in range(len(cells)):
        if (cells[i][23] == "True") or (int(cells[i][24])>0) :
            CreateObjectPage(strQuadrantName, cells, i)	


    #==========================================================================
    # create quadrant summary page
    #==========================================================================

    arrSummary = GetSummary(cells)

    strHTMLPage = BUILD_PATH + '\\3dcheck\\' + strQuadrantName + '.html'
    fo=open(strHTMLPage, 'w', encoding="utf-8")
    fo.write( '<html>'+ '\n')
    fo.write( '<head>'+ '\n')
    #fo.write( '<meta charset=\'utf-8\' />'+ '\n')
    fo.write( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')

    fo.write( '<title>Валидатор 3D:' + strQuadrantName + '</title>'+ '\n')
    fo.write( '<script src="/sorttable.js" type="Text/javascript"></script>'+ '\n')
    fo.write( '<style>'+ '\n')
    fo.write( 'table {border: 1px solid grey;}'+ '\n')
    fo.write( 'th {border: 1px solid grey; }'+ '\n')
    fo.write( 'td {border: 1px solid grey; padding:5px}'+ '\n')
    fo.write( '</style>'+ '\n')
    fo.write( '</head>'+ '\n')
    fo.write( '<body>'+ '\n')
    fo.write( '<h1>Валидатор 3D: квадрат ' + strQuadrantName + '</h1>'+ '\n')
    fo.write( '<p>Данный валидатор проверяет <b>наличие</b> 3d-моделей для церквей и некоторых других исторических зданий.'+ '\n')
    fo.write( 'Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии на temples.ru.</p>'+ '\n')
    # Print #3, "<p>На данный момент в валидацию включены отдельные районы Московской, Владимирской и Ярославской областей, т.е. то, что попадает в квадратный градус [56&deg;, 38&deg;]</p>"
    fo.write( '<h2>Cтатистика по квадрату</h2>'+ '\n')
    fo.write( '<table class="sortable">'+ '\n')
    fo.write( '<tr><th>Область</th><th>Район</th><th>Всего объектов</th> <th>С 3D моделью</th> <th>% </th></tr>'+ '\n')
    
    N=len(arrSummary)
    for i in range(1, N):
        if arrSummary[i].TotalObjects > 0:
            dblPercentage = arrSummary[i].ObjectsWith3D / arrSummary[i].TotalObjects * 100
        else:
            dblPercentage = 0
        fo.write( '<tr><td>' + IIf(arrSummary[i].RegionName != '', arrSummary[i].RegionName, '???') + '</td>'+ '\n')
        fo.write( '<td>' + arrSummary[i].DistrictName + '</td>'+ '\n')
        fo.write( '<td>' + str(arrSummary[i].TotalObjects) + '</td><td>' + str(arrSummary[i].ObjectsWith3D) + '</td><td> ' + str(Round(dblPercentage)) + ' </td></tr>'+ '\n')
    if arrSummary[0].TotalObjects > 0:
        dblPercentage = arrSummary[0].ObjectsWith3D / arrSummary[0].TotalObjects * 100
    else:
        dblPercentage = 0
    fo.write( '<tr><td><b>Всего в квадрате<b></td>'+ '\n')
    fo.write( '<td></td>'+ '\n')
    fo.write( '<td><b>' + str(arrSummary[0].TotalObjects) + '</b></td><td><b>' + str(arrSummary[0].ObjectsWith3D) + '<b></td>'+ '\n')
    fo.write( '<td><b>' + str(Round(dblPercentage)) + '</b></td></tr>'+ '\n')
    fo.write( '</table>'+ '\n')
    fo.write( '<h2>Объекты</h2>'+ '\n')
    fo.write( '<p><small>Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</small><p>'+ '\n')
    fo.write( '<table class="sortable">'+ '\n')
    fo.write( '<tr><th>OSM ID</th><th>Название</th><th>Год постройки</th><th>Temples.ru</th><th>Размер, м</th><th>Высота, м</th><th>Цвет</th><th>Материал</th>' + '<th>Стиль</th><th>Город</th> <th>Район</th> <th>Область</th><th>OSM 3D </th><th>Число частей</th><th>J</th></tr>'+ '\n')
   
    for i in range(len(cells)):

        if ( cells[i][10] != 'DEFENSIVE WALL' )  and  ( cells[i][10] != 'CHURCH FENCE' )  and  ( cells[i][10] != 'WATER TOWER' )  and  ( cells[i][10] != 'HISTORIC WALL' ) :
            if cells[i][23]=="True":
                if int(cells[i][24])>1: 
                    #there is model, and there are more than one building part   
                    fo.write( '<tr style="background: #DDFFCC" > '+ '\n')
                else:
                    #there is just one building part, which is very suspisious.   
                    fo.write( '<tr style="background: #FFFFAA" > '+ '\n')
            else:
                if (cells[i][23] == "False") and (int(cells[i][24])>0) :
                    #there are some building parts but they do not have height. Model cannot be created.
                    fo.write( '<tr style="background: #FFBBBB" > '+ '\n')
                else:
                    #there are no building parts and a model is not created. Sad, but it's not an error
                    fo.write( '<tr>'+ '\n')
            strOSMurl = 'https://www.openstreetmap.org/' + LCase(cells[i][1]) + '/' + cells[i][2]
            lat=(float(cells[i][3])+float(cells[i][5]))/2
            lon=(float(cells[i][4])+float(cells[i][6]))/2
            strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
            strTemplesID = cells[i][9]
            if strTemplesID !="":
                strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

            strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ cells[i][4] + "&right="+ cells[i][6] + "&top="+ cells[i][5] +"&bottom="+ cells[i][3] #"&select=object"
            #object name, by default 
            strDescription = Trim(cells[i][7])

            if strDescription == '':
                strDescription = Mid(cells[i][17], 4) #wikipedia article name, if any
            #last resort -- building type
            if strDescription == '':
                strDescription = '&lt;&lt;' + cells[i][10] + '&gt;&gt;'
            #ID and link to osm site
            strOsmID = Left(UCase(cells[i][1] ), 1) + ':' + cells[i][2]
            strModelUrl = 'models/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '.html'
            fo.write( '<td><a href="' + strOSMurl + '">' + strOsmID + '</a></td>'+ '\n')
            #Print #3, "<td>" & strOsmID & "</td>"
            #Name/description
            if (cells[i][23] == "True") or (int(cells[i][24])>0):
                #Better check here that the model exists!
                fo.write('<td width="350px"><a href="' + strModelUrl + '">' + strDescription + '</a></td>'+ '\n')
            else:
                fo.write('<td width="350px">' + strDescription + '</td>'+ '\n')

            #year of construction
            fo.write( '<td>' + cells[i][16] + '</td>'+ '\n')
            #temples.ru ref
            if strTemplesUrl != '':
                fo.write( '<td><a href="' + strTemplesUrl + '" target="_blank">' + strTemplesID + '</a></td>'+ '\n')
            else:
                fo.write( '<td></td>'+ '\n')
            #Size
            fo.write( '<td>' + IIf(cells[i][11] != 0, cells[i][11], '???') + '</td>'+ '\n')
            #height
            fo.write( '<td>' + IIf(cells[i][12] != "0", cells[i][12], '?') + '</td>'+ '\n')
            #Materials
            fo.write( '<td>' + cells[i][13] + '</td><td>' + cells[i][14] + '</td><td>' + cells[i][15] + '</td>'+ '\n')
            #Address: city-district-region
            fo.write( '<td>' + cells[i][20] + '</td>'+ '\n')
            strDistrict = cells[i][21]
            strDistrict = strDistrict.replace('район', 'р-н')
            strDistrict = strDistrict.replace('городской округ', 'го')
            fo.write('<td>' + strDistrict + '</td>'+ '\n')
            fo.write('<td>' + cells[i][22].replace('область', 'обл') + '</td>'+ '\n')
            fo.write('<td><a href="' + strF4url + '">' + cells[i][23] + '</a></td>'+ '\n')
            fo.write('<td>' + cells[i][24] + '</td>' )
            fo.write('<td><a href="' + strJOSMurl + '" target = "josm" >' + 'J' + '</a></td>'+ '\n')
            fo.write('</tr>'+ '\n')
    fo.write( '</table>'+ '\n')
    fo.write( '<hr />'+ '\n')
    fo.write( '<p>Дата формирования страницы: ' + getTimeStamp() + '</p>' + '\n')
    #zero frame for josm links
    fo.write( '<div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    fo.write( '</body>'+ '\n')
    fo.write( '<html>' + '\n')
    fo.close()


def CreateIndexPage():

    strInputFile="d:\\_VFR_LANDMARKS_3D_RU\\work_folder\\Quadrants.dat"
    cells = loadDatFile(strInputFile)


    strHTMLPage = BUILD_PATH + '\\3dcheck\\' + 'index' + '.html'
    fo=open(strHTMLPage, 'w', encoding="utf-8")


    fo.write( '<html>' + '\n')
    fo.write( '<head>' + '\n')
    fo.write( '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    fo.write( '  <title>Валидатор 3D: церкви и другие здания</title>' + '\n')
    fo.write( '  <script src="/sorttable.js" type="Text/javascript"></script>' + '\n')
    fo.write( '  <style>' + '\n')
    fo.write( '    table {border: 1px solid grey;}' + '\n')
    fo.write( '    th {border: 1px solid grey; }' + '\n')
    fo.write( '    td {border: 1px solid grey; padding:5px}' + '\n')
    fo.write( '  </style>' + '\n')
    fo.write( '</head>' + '\n')
    fo.write( '<body>' + '\n')
    fo.write( '  <h1>Валидатор 3D: Церкви и другие здания</h1>' + '\n')
    fo.write( '  <p>Данный валидатор проверяет <b>наличие</b> 3d-моделей для церквей и некоторых других исторических зданий.' + '\n')
    fo.write( '     Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии на temples.ru.</p>' + '\n')
    fo.write( '  <p>Данные нарезаются по квадратным градусам (этот валидатор таким родился)</p>' + '\n')
    fo.write( '  <h2>Список квадратов</h2>' + '\n')
    fo.write( '  <table class="sortable">' + '\n')
    fo.write( '    <tr><th>Квадрат</th><th>Описание</th><th>Всего объектов</th><th>С 3D моделью</th><th>Процент</th><th>Дата последнего обновления</th></tr>' + '\n')
    
    for i in range(len(cells)):
        if cells[i][4]>'1900.01.01 00:00:00': 
            intRate=0
            if int(cells[i][2]) !=0:
                intRate = Round(100.0*int(cells[i][3])/int(cells[i][2])) 
            fo.write( '    <tr><td>'+cells[i][0]+'</td><td><a href="'+cells[i][0]+'.html">'+ cells[i][1] +'</a> </td><td>'+cells[i][2]+'</td><td>' + cells[i][3]+ '</td><td>' + str(intRate)+ '</td><td>' + cells[i][4]+ '</td></tr>' + '\n')

    fo.write( '  </table>' + '\n')
    fo.write( '  <h2>Полезные ссылки</h2>' + '\n')
    fo.write( '  <ul>' + '\n')
    fo.write( '    <li><a href="https://www.openstreetmap.org/user/Zkir/diary/390256" >Задать вопросы по этому валидатору можно тут</a></li> ' + '\n')
    fo.write( '    <li><a href="https://wiki.openstreetmap.org/wiki/Simple_3D_buildings" >Спецификация Simple Buildings, т.е. то, как рисовать 3D-здания в OSM</a></li>' + '\n')
    fo.write( '    <li><a href="https://wiki.openstreetmap.org/wiki/User:Zkir">Дополнительные теги для церквей</a></li>' + '\n')
    fo.write( '    <li><a href="https://demo.f4map.com/#lat=56.3099201&amp;lon=38.1301151&amp;zoom=18&amp;camera.theta=58.228&amp;camera.phi=-41.93">3D карта, ака F4map</a></li>' + '\n')
    fo.write( '  </ul>' + '\n')
    fo.write( '  <hr />' + '\n')
    fo.write( '  <p>Дата формирования страницы: ' + getTimeStamp() + '</p>' + '\n')
    fo.write( '  <div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    fo.write( '</body>' + '\n')
    fo.write( '</html>' + '\n')

    fo.close()