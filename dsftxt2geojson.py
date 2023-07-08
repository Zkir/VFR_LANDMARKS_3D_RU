import sys

def escapeJsonString(s):
    s = s.replace("\"", "")
    s = s.replace("'","")
    s = s.replace("\\","\\\\") # single \ to double \\
    return s

def main():
    #strInputFileName = '+56+038.dsf.txt'
    #strOutputFileName = '+56+038.geojson'

    strInputFileName = sys.argv[1]
    strOutputFileName = sys.argv[2]
    
    fo1 = open(strInputFileName, 'r', encoding='UTF-8' )
    fo2 = open(strOutputFileName, 'w', encoding='UTF-8')
    
    
    fo2.write('{ \n')
    fo2.write('  "type": "FeatureCollection",\n')
    fo2.write('  "generator" : "zdsftxt2geojson.py",\n')
    fo2.write('  "source": "'+escapeJsonString(strInputFileName)+'",\n')
    fo2.write('  "features": [\n')
   
    
    j=0
    polygon_defs = []
    object_defs = []

    for line in fo1:
        tokens=line.strip().split(' ')
        
        if tokens[0]=='OBJECT_DEF':
            object_defs.append(tokens[1])

        if tokens[0]=='POLYGON_DEF':
            polygon_defs.append(tokens[1])

        # "Objects" in x-plane dsf are points. Just a single line per objects
        #OBJECT 2 38.379056992 56.466031510 229.996796

        if tokens[0]=='OBJECT':
            if j!=0:
                fo2.write(',\n')
            j=j+1 

            fo2.write('        { \n')  # start of feature 
            fo2.write('            "type": "Feature",\n')
            fo2.write('            "properties": { \n') 
            fo2.write('                "@id": "' + str(j) +'",\n')
            fo2.write('                "type": "' + tokens[1] +'",\n')
            fo2.write('                "param": "' + tokens[4] + '",\n')
            fo2.write('                "def": "' + escapeJsonString(object_defs[int(tokens[1])]) + '"\n')
            fo2.write('            }, \n')  #end of property 
            fo2.write('            "geometry": {\n')
            fo2.write('                "type": "Point",\n')
            fo2.write('                "coordinates": [' + tokens[2] + ', ' + tokens[3] + '],\n')
            fo2.write('            }\n') #end of geometry
            fo2.write('        }') # end of feature 

        #polygons in x-plane are polygones with possible holes. luckily there no multipolygons in x-plane.
        #BEGIN_POLYGON 1 255 2 #<type> <param> [<coords>]
        #BEGIN_WINDING
        #POLYGON_POINT 38.904329747 56.687333104 
        #END_WINDING
        #END_POLYGON

        if tokens[0]=='BEGIN_POLYGON':
            if j!=0:
                fo2.write(',\n')
            j=j+1  
            fo2.write('        { \n')  # start of feature 
            fo2.write('            "type": "Feature",\n')
            fo2.write('            "properties": { \n') 
            fo2.write('                "@id": "' + str(j) +'",\n')
            fo2.write('                "type": "' + tokens[1] +'",\n')
            fo2.write('                "param": "' + tokens[2] + '",\n')
            fo2.write('                "coords": "' + tokens[3] + '",\n')
            fo2.write('                "def": "' + escapeJsonString(polygon_defs[int(tokens[1])]) + '"\n')
            fo2.write('            }, \n')  #end of property 
            fo2.write('            "geometry": {\n')
            fo2.write('                "type": "Polygon",\n')
            fo2.write('                "coordinates": [\n')      
            i = 0 # winding counter 
            
        if tokens[0]=='BEGIN_WINDING':
            if i!=0:
                fo2.write(',\n')
            fo2.write('                    [\n')
            i = i + 1
            k = 0 
            
        if tokens[0]=='POLYGON_POINT':    
            if k==0:
                lon0 = tokens[1]
                lat0 = tokens[2]

            fo2.write('                        [' + tokens[1] + ', ' + tokens[2] + '],\n')
            k = k + 1              
        
        if tokens[0]=='END_WINDING':
            fo2.write('                        [' + lon0 + ', ' + lat0 + ']\n') # for some funny reason polygons in dsf are not closed. to save space maybe?
            fo2.write('\n')
            fo2.write('                    ]') 

        
        if tokens[0]=='END_POLYGON':
            fo2.write('\n')
            fo2.write('                ]\n') # end of coordinates      
            fo2.write('            }\n') #end of geometry
            
            fo2.write('        }') # end of feature 
    
    
    
    
    fo2.write('  ]\n')
    fo2.write('} ')
    
    print ("point object types detected: "+str(len(object_defs)))    
    print ("polygon types detected: "+str(len(polygon_defs)))    
    print ("features processed: "+str(j))

    
    fo1.close
    fo2.close

main()