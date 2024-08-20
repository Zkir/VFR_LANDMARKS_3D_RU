#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
import time 
from mdlMisc import *
import os.path
import json
import cgi

#========================================================================
#  Web Page for individual object, with validation errors
#========================================================================
def CreateRegionPage(strQuadrantName, cells, page_time_stamp):
    strHTMLPage = ""
    strOSMurl = ""
    strF4url = ""
    strTemplesUrl = ""
    strTemplesID = ""
    strJOSMurl = ""
    strWikipediaLink = ""    

        
      
    print( '<!doctype html>'+ '\n')
    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
   
    print( '<title>Валидатор 3D:' + strQuadrantName + ' Ошибки</title>'+ '\n')
    print( '  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'+ '\n')
    print("""
          <script src="/js/sorttable.js" type="Text/javascript"></script>
          <style>
             table {border: 1px solid grey; }
             th {border: 1px solid grey; }
             td {border: 1px solid grey; padding:5px}
          </style>
          """)
    print( '</head>'+ '\n')
    print( '<body class=\'page\'>'+ '\n')
    print( '  <div class=\'page-header\'>'+ '\n')
    
    print( '<h1>Валидатор 3D: квадрат ' + strQuadrantName + ' Ошибки</h1>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-content\'>'+ '\n')

    print( '  <h2>'+ '\n')
    print( 'Ошибки валидации'+ '\n')
    print( '  </h2>'+ '\n')
    print( '  <div class=\'errors\'  >'+ '\n')
    print( '  <table class="sortable">'+ '\n')
    
    print('<tr>')
    print('<th>Название</td>')
    print('<th>OSM ID</td>')
    print('<th>F4 Map </td>')
    print('<th> Ошибка </td>')
    print('<th> JOSM </td>')
    print('<th> ID </td>')
    print('</tr>')
    
    y = {"W":"way", "R":"relation"}
    
    # since it's region page, we need to read all errors for all objects in loop.
    for obj_rec in cells: 
    
        lat=(float(obj_rec[3])+float(obj_rec[5]))/2
        lon=(float(obj_rec[4])+float(obj_rec[6]))/2

        strOsmID = UCase(Left(obj_rec[1],1)) + obj_rec[2]
        strWikipediaName= Mid(obj_rec[17], 4)
        
        strObjectName=obj_rec[7]
        if strObjectName=="" and strWikipediaName!="":
            strObjectName=strWikipediaName
            
            
        strDescription = Trim(obj_rec[7])

        if strDescription == '':
            strDescription = Mid(obj_rec[17], 4) #wikipedia article name, if any
        #last resort -- building type
        if strDescription == '':
            strDescription = '&lt;&lt;' + obj_rec[10] + '&gt;&gt;'    

    
        #validation errors
        validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'

        if os.path.exists(validation_errors_file_name) and int(obj_rec[26])>0:
            with open(validation_errors_file_name) as f:
                validation_errors = json.load(f)
        else:
            validation_errors = []


        for error in validation_errors:
             
            part_type, part_id =  error['part_id'].split(":", 1)
        
            strOSMurl = 'https://www.openstreetmap.org/' + y[part_type] + '/' + part_id
            strJOSMurl = "http://localhost:8111/load_object?new_layer=true&objects="+ LCase(part_type)+part_id +"&relation_members=true"   #"&select=object"
            strIDurl = "https://www.openstreetmap.org/edit?editor=id&"+y[part_type]+"=" + part_id
            strF4url = 'http://demo.f4map.com/#lat=' + str(lat) + '&lon=' + str(lon) + '&zoom=19'
            strModelUrl = strQuadrantName + '/' + Left(UCase(obj_rec[1] ), 1) + obj_rec[2]  + '.html'
           
        
            print('<tr>')
             #Name/description
            if (obj_rec[23] == "True") or (int(obj_rec[24])>0):
                #Better check here that the model exists!
                print('<td width="350px"><a href="' + strModelUrl + '">' + strDescription + '</a></td>'+ '\n')
            else:
                print('<td width="350px">' + strDescription + '</td>'+ '\n')
            print('<td><a href="'+strOSMurl+'">'+error['part_id']+'<a></td>')
            print('<td><a href="' + strF4url + '">' + "F4" + '</a></td>'+ '\n')
            print('<td>'+error['error']+'</td>')
            print('<td><a href="'+strJOSMurl+'" target="josm">'+'J'+'<a></td>')
            print('<td><a href="'+strIDurl+'" target="josm">'+'ID'+'<a></td>')
            
            print('</tr>')

    print( '  </table>'+ '\n')

    

    print( '  <div style=\'clear:both;\'></div>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class=\'page-footer\'>'+ '\n')
    print( '  <div class=\'navigation\'>'+ '\n')
    print( '<hr />'+ '\n')
    print( '  <a href=\'/\'>Главная страница</a> --> <a href=\'/' + strQuadrantName + '.html\'>' + strQuadrantName + '</a> \n')
    print( '  </div>'+ '\n')
    #zero frame for josm links
    print( '<div style="display: none;"><iframe name="josm"></iframe></div>'+ '\n')
    print( '<hr />'+ '\n')
    print( '<p>Дата формирования страницы: ' + page_time_stamp + '</p>'+ '\n')    
    

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
print


url = os.environ.get("REQUEST_URI","") 
parsed = urlparse.urlparse(url) 
strParam=urlparse.parse_qs(parsed.query).get('param','')
#strQuadrantName=url[1:-5]
strQuadrantName=cgi.FieldStorage().getvalue('param')

if strQuadrantName is None:
    strQuadrantName="RU-MOW"


strInputFile = "data\\quadrants\\"+strQuadrantName+".dat"
cells = loadDatFile(strInputFile)
page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)
      
    
CreateRegionPage(strQuadrantName, cells, page_time_stamp)