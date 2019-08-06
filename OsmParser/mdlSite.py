from vbFunctions import *
from mdlMisc import *

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

def GetSummary(cells):
    summary = [] 
    sumrec= TSummaryRec()
    sumrec.DistrictName = ""
    sumrec.RegionName= "Всего в квадрате"
    sumrec.TotalObjects = 0
    sumrec.ObjectsWith3d= 0
    summary.append (sumrec) 
    for i in range(len(cells)):
        #find existing record
        blnFound=False
        for j in range(len(summary)):  
            if summary[j].DistrictName == "" and summary[j].RegionName == cells[i][21] :
                sumrec = summary[j]  
                blnFound = True
                break  
        if not blnFound:
            sumrec= TSummaryRec()
            sumrec.DistrictName = ""
            sumrec.RegionName= cells[i][21]
            sumrec.TotalObjects = 0
            sumrec.ObjectsWith3d = 0
            summary.append (sumrec) 
          
        sumrec.TotalObjects=sumrec.TotalObjects+1
        summary[0].TotalObjects=summary[0].TotalObjects+1

        if cells[i][22] == "True": 
            sumrec.ObjectsWith3D=sumrec.ObjectsWith3D+1
            summary[0].ObjectsWith3D=summary[0].ObjectsWith3D+1


    return summary


def CreateRegionSummaryPage(Sheet1, dsfLat, dsfLon):
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
    
    cells=[]  
    filehandle = open(strInputFile, 'r' )
    txt = filehandle.readline().strip()
    while len(txt) != 0:
        txt = filehandle.readline()
        row = txt.strip().split("|")
        if len(row)>1:
            cells.append(row)
    # end of while



    arrSummary = GetSummary(cells)

    strHTMLPage = BUILD_PATH + '\\3dcheck\\' + strQuadrantName + '.html'
    fo=open(strHTMLPage, 'w', encoding="utf-8")
    fo.write( '<html>'+ '\n')
    fo.write( '<head>'+ '\n')
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
    fo.write( '<tr><th>OSM ID</th><th>Название</th><th>Год постройки</th><th>Temples.ru</th><th>Размер, м</th><th>Высота, м</th><th>Цвет</th><th>Материал</th>' + '<th>Стиль</th><th>Город</th> <th>Район</th> <th>Область</th><th>OSM 3D </th><th>J</th></tr>'+ '\n')
   
    for i in range(len(cells)):

        if ( cells[i][10] != 'DEFENSIVE WALL' )  and  ( cells[i][10] != 'CHURCH FENCE' )  and  ( cells[i][10] != 'WATER TOWER' )  and  ( cells[i][10] != 'HISTORIC WALL' ) :
            if cells[i][22]=="True":
                fo.write( '<tr style="background: #DDFFCC" > '+ '\n')
            else:
                fo.write( '<tr>'+ '\n')
            strOSMurl = 'https://www.openstreetmap.org/' + LCase(cells[i][1]) + '/' + cells[i][2]
            lat=(float(cells[i][3])+float(cells[i][5]))/2
            lon=(float(cells[i][4])+float(cells[i][6]))/2
            strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
            strTemplesID = cells[i][9]
            if strTemplesID !="":
                strTemplesUrl = "http://temples.ru/card.php?ID=" + strTemplesID

            strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ cells[i][4] + "&right="+ cells[i][6] + "&top="+ cells[i][5] +"&bottom="+ cells[i][3] #"&select=object"
            strDescription = Trim(cells[i][7])
            if strDescription == '':
                strDescription = '&lt;&lt;' + cells[i][10] + '&gt;&gt;'
            #ID and link to osm site
            strOsmID = Left(UCase(cells[i][1] ), 1) + ':' + cells[i][2]
            strModelUrl = 'models/' + Left(UCase(cells[i][1] ), 1) + cells[i][2]  + '.html'
            fo.write( '<td><a href="' + strOSMurl + '">' + strOsmID + '</a></td>'+ '\n')
            #Print #3, "<td>" & strOsmID & "</td>"
            #Name/description
            if cells[i][22] == "True":
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
            strDistrict = "" #cells[i][21]
            strDistrict = strDistrict.replace('район', 'р-н')
            strDistrict = strDistrict.replace('городской округ', 'го')
            fo.write('<td>' + strDistrict + '</td>'+ '\n')
            fo.write('<td>' + cells[i][21].replace('область', 'обл') + '</td>'+ '\n')
            fo.write('<td><a href="' + strF4url + '">' + cells[i][22] + '</a></td>'+ '\n')
            fo.write('<td><a href="' + strJOSMurl + '" target = "josm" >' + 'J' + '</a></td>'+ '\n')
            fo.write('</tr>'+ '\n')
    fo.write( '</table>'+ '\n')
    fo.write( '<hr />'+ '\n')
    fo.write( '<p>Дата формирования страницы: ' + '???' + '</p>' + '\n')
    #zero frame for josm links
    fo.write( '<div style="display: none;"><iframe name="josm"></iframe></div>' + '\n')
    fo.write( '</body>'+ '\n')
    fo.write( '<html>' + '\n')
    fo.close()

