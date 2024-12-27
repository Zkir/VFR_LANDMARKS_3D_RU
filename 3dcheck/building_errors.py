#!c:\Program Files\Python312\python.exe
import urllib.parse as urlparse
import os
import sys
import codecs
import time 
from mdlMisc import *
import os.path
import json
from mdlClassify import buildingTypeRus

#========================================================================
#  Web Page for individual object, with validation errors
#========================================================================
def CreateObjectPage(strQuadrantName,obj_rec, page_time_stamp,validation_errors):
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
    strWikipediaName= Mid(obj_rec[17], 4)
    
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
  
    print( '<!doctype html>'+ '\n')
    print( '<html>'+ '\n')
    print( '<head>'+ '\n')
    print( '  <title>' + strObjectName  +'</title>'+ '\n')
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
    print( '<body class="page">'+ '\n')
    print( '  <div class="page-header">'+ '\n')
    strPageTitle=strObjectName + ' (' + strOsmID + ') ' +strStars
    print( '    <h1 title="'+strPageTitle+'">' + strPageTitle + '</h1>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class="page-content">'+ '\n')

    print( '  <h2>'+ '\n')
    print( 'Ошибки валидации'+ '\n')
    print( '  </h2>'+ '\n')
    print( '  <div class="errors"  >'+ '\n')
    print( '  <table class="sortable">'+ '\n')
    
    print('<tr>')
    print('<th>ID Объекта </td>')
    print('<th> Ошибка </td>')
    print('<th> JOSM </td>')
    print('<th> ID </td>')
    print('</tr>')
    
    y = {"W":"way", "R":"relation"}

    for error in validation_errors:
         
        part_type, part_id =  error['part_id'].split(":", 1)
    
        strOSMurl = 'https://www.openstreetmap.org/' + y[part_type] + '/' + part_id
        #strJOSMurl = "http://localhost:8111/load_and_zoom?left="+ obj_rec[4] + "&right="+ obj_rec[6] + "&top="+ obj_rec[5] +"&bottom="+ obj_rec[3] #"&select=object"
       
        strJOSMurl = "http://localhost:8111/load_object?new_layer=true&objects="+ LCase(part_type)+part_id +"&relation_members=true"   #"&select=object"
       
        strIDurl = "https://www.openstreetmap.org/edit?editor=id&"+y[part_type]+"=" + part_id
       
    
        print('<tr>')
        print('<td><a href="'+strOSMurl+'">'+error['part_id']+'<a></td>')
        print('<td>'+error['error']+'</td>')
        print('<td><a href="'+strJOSMurl+'" target="josm">'+'J'+'<a></td>')
        print('<td><a href="'+strIDurl+'" target="josm">'+'ID'+'<a></td>')
        
        print('</tr>')
    print( '  </table>'+ '\n')
    
   

    print( '  <div style="clear:both;"></div>'+ '\n')
    print( '  </div>'+ '\n')
    print( '  <div class="page-footer">'+ '\n')
    print( '  <div class="navigation">'+ '\n')
    print( '<hr />'+ '\n')
    print( '  <a href="/">Главная страница</a> --> <a href="/countries/' + strQuadrantName + '">' + strQuadrantName + '</a>' + 
           ' --> <a href="/countries/' + strQuadrantName + '/' + strOsmID + '">'+ strObjectName + '</a>\n')
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

s=url.split("/")

if len(s)>=2:
    strQuadrantName=s[3].strip()
    intObjectIndex=s[4]#[0:-12]
    #print(intObjectIndex) 
else:
    strQuadrantName="RU-MOW"
    intObjectIndex="R3030568"

strInputFile = "data\\quadrants\\"+strQuadrantName+".dat"
cells = loadDatFile(strInputFile)
page_time_stamp =  time.strptime(time.ctime(os.path.getmtime(strInputFile)))
page_time_stamp =  time.strftime("%Y-%m-%d %H:%M:%S", page_time_stamp)
    
for rec in cells:
    if UCase(Left(rec[1],1)) + rec[2] == intObjectIndex:
       obj_rec = rec
       break  
       
        
#validation errors
validation_errors_file_name = "data\\errors\\" + UCase(Left(obj_rec[1],1)) + obj_rec[2] +'.errors.dat'




if os.path.exists(validation_errors_file_name):
    with open(validation_errors_file_name, encoding="utf-8") as f:
        validation_errors = json.load(f)
else:
    validation_errors = []
      
    
CreateObjectPage(strQuadrantName, obj_rec, page_time_stamp, validation_errors)