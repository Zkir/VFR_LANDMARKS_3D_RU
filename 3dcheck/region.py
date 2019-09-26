#!c:\Program Files\Python37\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
from mdlMisc import *
import cgi


class TSummaryRec:

    def __init__(self):
        self.DistrictName = ""

        self.RegionName = ""
        self.TotalObjects = 0  
        self.ObjectsWith3D = 0


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

def CreateRegionSummaryPage(strQuadrantName, strInputFile, blnCreateObjectPages, blnGeocode):
    strHTMLPage = ""

    i = 0

    strTemplesUrl = ""


    cells = loadDatFile(strInputFile)


   
    # ==========================================================================
    # sort by number of building parts
    # ==========================================================================
    cells.sort(key=lambda row: int(row[24]), reverse=True)



    #==========================================================================
    # create quadrant summary page
    #==========================================================================

    arrSummary = GetSummary(cells)

    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    #print( '<meta charset=\'utf-8\' />'+ '\n')
    print( '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')

    print( '<title>Валидатор 3D:' + strQuadrantName + '</title>'+ '\n')
    print( '<script src="/sorttable.js" type="Text/javascript"></script>'+ '\n')
    print( '<style>'+ '\n')
    print( 'table {border: 1px solid grey;}'+ '\n')
    print( 'th {border: 1px solid grey; }'+ '\n')
    print( 'td {border: 1px solid grey; padding:5px}'+ '\n')
    print( '</style>'+ '\n')
    print( '</head>'+ '\n')
    print( '<body>'+ '\n')
    print( '<h1>Валидатор 3D: квадрат ' + strQuadrantName + '</h1>'+ '\n')
    print( '<p>Данный валидатор проверяет <b>наличие</b> 3d-моделей для церквей и некоторых других исторических зданий.'+ '\n')
    print( 'Почему церкви? Потому что это наиболее заметные объекты и для их моделирования есть фотографии на temples.ru.</p>'+ '\n')
    # Print #3, "<p>На данный момент в валидацию включены отдельные районы Московской, Владимирской и Ярославской областей, т.е. то, что попадает в квадратный градус [56&deg;, 38&deg;]</p>"
    print( '<h2>Cтатистика по квадрату</h2>'+ '\n')
    print( '<table class="sortable">'+ '\n')
    print( '<tr><th>Область</th><th>Район</th><th>Всего объектов</th> <th>С 3D моделью</th> <th>% </th></tr>'+ '\n')
    
    N=len(arrSummary)
    for i in range(1, N):
        if arrSummary[i].TotalObjects > 0:
            dblPercentage = arrSummary[i].ObjectsWith3D / arrSummary[i].TotalObjects * 100
        else:
            dblPercentage = 0
        print( '<tr><td>' + IIf(arrSummary[i].RegionName != '', arrSummary[i].RegionName, '???') + '</td>'+ '\n')
        print( '<td>' + arrSummary[i].DistrictName + '</td>'+ '\n')
        print( '<td>' + str(arrSummary[i].TotalObjects) + '</td><td>' + str(arrSummary[i].ObjectsWith3D) + '</td><td> ' + str(Round(dblPercentage)) + ' </td></tr>'+ '\n')
    if arrSummary[0].TotalObjects > 0:
        dblPercentage = arrSummary[0].ObjectsWith3D / arrSummary[0].TotalObjects * 100
    else:
        dblPercentage = 0
    print( '<tr><td><b>Всего в квадрате<b></td>'+ '\n')
    print( '<td></td>'+ '\n')
    print( '<td><b>' + str(arrSummary[0].TotalObjects) + '</b></td><td><b>' + str(arrSummary[0].ObjectsWith3D) + '<b></td>'+ '\n')
    print( '<td><b>' + str(Round(dblPercentage)) + '</b></td></tr>'+ '\n')
    print( '</table>'+ '\n')
    print( '<h2>Объекты</h2>'+ '\n')
    print( '<p><small>Между прочим, таблица сортируется. Достаточно кликнуть на заголовок столбца.</small><p>'+ '\n')
    print( '<table class="sortable">'+ '\n')
    print( '<tr><th>OSM ID</th><th>Название</th><th>Год постройки</th><th>Temples.ru</th><th>Размер, м</th><th>Высота, м</th><th>Цвет</th><th>Материал</th>' + '<th>Стиль</th><th>Город</th> <th>Район</th> <th>Область</th><th>OSM 3D </th><th>Число частей</th><th>J</th></tr>'+ '\n')
   
    for i in range(len(cells)):

        if ( cells[i][10] != 'DEFENSIVE WALL' )  and  ( cells[i][10] != 'CHURCH FENCE' )  and  ( cells[i][10] != 'WATER TOWER' )  and  ( cells[i][10] != 'HISTORIC WALL' ) :
            if cells[i][23]=="True":
                if int(cells[i][24])>1: 
                    #there is model, and there are more than one building part   
                    print( '<tr style="background: #DDFFCC" > '+ '\n')
                else:
                    #there is just one building part, which is very suspisious.   
                    print( '<tr style="background: #FFFFAA" > '+ '\n')
            else:
                if (cells[i][23] == "False") and (int(cells[i][24])>0) :
                    #there are some building parts but they do not have height. Model cannot be created.
                    print( '<tr style="background: #FFBBBB" > '+ '\n')
                else:
                    #there are no building parts and a model is not created. Sad, but it's not an error
                    print( '<tr>'+ '\n')
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
            strModelUrl = strQuadrantName + '/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '.html'
            print( '<td><a href="' + strOSMurl + '">' + strOsmID + '</a></td>'+ '\n')
            #Print #3, "<td>" & strOsmID & "</td>"
            #Name/description
            if (cells[i][23] == "True") or (int(cells[i][24])>0):
                #Better check here that the model exists!
                print('<td width="350px"><a href="' + strModelUrl + '">' + strDescription + '</a></td>'+ '\n')
            else:
                print('<td width="350px">' + strDescription + '</td>'+ '\n')

            #year of construction
            print( '<td>' + cells[i][16] + '</td>'+ '\n')
            #temples.ru ref
            if strTemplesUrl != '':
                print( '<td><a href="' + strTemplesUrl + '" target="_blank">' + strTemplesID + '</a></td>'+ '\n')
            else:
                print( '<td></td>'+ '\n')
            #Size
            print( '<td>' + IIf(cells[i][11] != 0, cells[i][11], '???') + '</td>'+ '\n')
            #height
            print( '<td>' + IIf(cells[i][12] != "0", cells[i][12], '?') + '</td>'+ '\n')
            #Materials
            print( '<td>' + cells[i][13] + '</td><td>' + cells[i][14] + '</td><td>' + cells[i][15] + '</td>'+ '\n')
            #Address: city-district-region
            print( '<td>' + cells[i][20] + '</td>'+ '\n')
            strDistrict = cells[i][21]
            strDistrict = strDistrict.replace('район', 'р-н')
            strDistrict = strDistrict.replace('городской округ', 'го')
            print('<td>' + strDistrict + '</td>'+ '\n')
            print('<td>' + cells[i][22].replace('область', 'обл') + '</td>'+ '\n')
            print('<td><a href="' + strF4url + '">' + cells[i][23] + '</a></td>'+ '\n')
            print('<td>' + cells[i][24] + '</td>' )
            print('<td><a href="' + strJOSMurl + '" target = "josm" >' + 'J' + '</a></td>'+ '\n')
            print('</tr>'+ '\n')
    print( '</table>'+ '\n')
    print( '<hr />'+ '\n')
    print( '<p>Дата формирования страницы: ' + getTimeStamp() + '</p>' + '\n')
    #zero frame for josm links
    print( '<div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    print( '</body>'+ '\n')
    print( '<html>' + '\n')



sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ("Content-Type: text/html; charset=utf-8 \n\n")
print

url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
strParam=urlparse.parse_qs(parsed.query).get('param','')
#strQuadrantName=url[1:-5]
strQuadrantName=cgi.FieldStorage().getvalue('param')

#print(strQuadrantName)
CreateRegionSummaryPage(strQuadrantName, "data/"+strQuadrantName+".dat", False, False)
