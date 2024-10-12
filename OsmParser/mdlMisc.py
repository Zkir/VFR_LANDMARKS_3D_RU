from datetime import datetime

lstColorCodes=[
['aliceblue', '#F0F8FF'],
['antiquewhite', '#FAEBD7'],
['aqua', '#00FFFF'],
['aquamarine', '#7FFFD4'],
['azure', '#F0FFFF'],
['beige', '#F5F5DC'],
['bisque', '#FFE4C4'],
['black', '#000000'],
['blanchedalmond', '#FFEBCD'],
['blue', '#0000FF'],
['blueviolet', '#8A2BE2'],
['brown', '#A52A2A'],
['burlywood', '#DEB887'],
['cadetblue', '#5F9EA0'],
['chartreuse', '#7FFF00'],
['chocolate', '#D2691E'],
['coral', '#FF7F50'],
['cornflowerblue', '#6495ED'],
['cornsilk', '#FFF8DC'],
['crimson', '#DC143C'],
['cyan', '#00FFFF'],
['darkblue', '#00008B'],
['darkcyan', '#008B8B'],
['darkgoldenrod', '#B8860B'],
['darkgray', '#A9A9A9'],
['darkgreen', '#006400'],
['darkgrey', '#A9A9A9'],
['darkkhaki', '#BDB76B'],
['darkmagenta', '#8B008B'],
['darkolivegreen', '#556B2F'],
['darkorange', '#FF8C00'],
['darkorchid', '#9932CC'],
['darkred', '#8B0000'],
['darksalmon', '#E9967A'],
['darkseagreen', '#8FBC8F'],
['darkslateblue', '#483D8B'],
['darkslategray', '#2F4F4F'],
['darkslategrey', '#2F4F4F'],
['darkturquoise', '#00CED1'],
['darkviolet', '#9400D3'],
['deeppink', '#FF1493'],
['deepskyblue', '#00BFFF'],
['dimgray', '#696969'],
['dimgrey', '#696969'],
['dodgerblue', '#1E90FF'],
['firebrick', '#B22222'],
['floralwhite', '#FFFAF0'],
['forestgreen', '#228B22'],
['fuchsia', '#FF00FF'],
['gainsboro', '#DCDCDC'],
['ghostwhite', '#F8F8FF'],
['gold', '#FFD700'],
['goldenrod', '#DAA520'],
['gray', '#808080'],
['green', '#008000'],
['greenyellow', '#ADFF2F'],
['grey', '#808080'],
['honeydew', '#F0FFF0'],
['hotpink', '#FF69B4'],
['indianred', '#CD5C5C'],
['indigo', '#4B0082'],
['ivory', '#FFFFF0'],
['khaki', '#F0E68C'],
['lavender', '#E6E6FA'],
['lavenderblush', '#FFF0F5'],
['lawngreen', '#7CFC00'],
['lemonchiffon', '#FFFACD'],
['lightblue', '#ADD8E6'],
['lightcoral', '#F08080'],
['lightcyan', '#E0FFFF'],
['lightgoldenrodyellow', '#FAFAD2'],
['lightgray', '#D3D3D3'],
['lightgreen', '#90EE90'],
['lightgrey', '#D3D3D3'],
['lightpink', '#FFB6C1'],
['lightsalmon', '#FFA07A'],
['lightseagreen', '#20B2AA'],
['lightskyblue', '#87CEFA'],
['lightslategray', '#778899'],
['lightslategrey', '#778899'],
['lightsteelblue', '#B0C4DE'],
['lightyellow', '#FFFFE0'],
['lime', '#00FF00'],
['limegreen', '#32CD32'],
['linen', '#FAF0E6'],
['magenta', '#FF00FF'],
['maroon', '#800000'],
['mediumaquamarine', '#66CDAA'],
['mediumblue', '#0000CD'],
['mediumorchid', '#BA55D3'],
['mediumpurple', '#9370DB'],
['mediumseagreen', '#3CB371'],
['mediumslateblue', '#7B68EE'],
['mediumspringgreen', '#00FA9A'],
['mediumturquoise', '#48D1CC'],
['mediumvioletred', '#C71585'],
['midnightblue', '#191970'],
['mintcream', '#F5FFFA'],
['mistyrose', '#FFE4E1'],
['moccasin', '#FFE4B5'],
['navajowhite', '#FFDEAD'],
['navy', '#000080'],
['oldlace', '#FDF5E6'],
['olive', '#808000'],
['olivedrab', '#6B8E23'],
['orange', '#FFA500'],
['orangered', '#FF4500'],
['orchid', '#DA70D6'],
['palegoldenrod', '#EEE8AA'],
['palegreen', '#98FB98'],
['paleturquoise', '#AFEEEE'],
['palevioletred', '#DB7093'],
['papayawhip', '#FFEFD5'],
['peachpuff', '#FFDAB9'],
['peru', '#CD853F'],
['pink', '#FFC0CB'],
['plum', '#DDA0DD'],
['powderblue', '#B0E0E6'],
['purple', '#800080'],
['red', '#FF0000'],
['rosybrown', '#BC8F8F'],
['royalblue', '#4169E1'],
['saddlebrown', '#8B4513'],
['salmon', '#FA8072'],
['sandybrown', '#F4A460'],
['seagreen', '#2E8B57'],
['seashell', '#FFF5EE'],
['sienna', '#A0522D'],
['silver', '#C0C0C0'],
['skyblue', '#87CEEB'],
['slateblue', '#6A5ACD'],
['slategray', '#708090'],
['slategrey', '#708090'],
['snow', '#FFFAFA'],
['springgreen', '#00FF7F'],
['steelblue', '#4682B4'],
['tan', '#D2B48C'],
['teal', '#008080'],
['thistle', '#D8BFD8'],
['tomato', '#FF6347'],
['turquoise', '#40E0D0'],
['violet', '#EE82EE'],
['wheat', '#F5DEB3'],
['white', '#FFFFFF'],
['whitesmoke', '#F5F5F5'],
['yellow', '#FFFF00'],
['yellowgreen', '#9ACD32']
]


def getColourName(strRgbCode):
    strColorName = "black"

    if not strRgbCode.startswith("#"):
        raise Exception ("wrong color format")
    if len(strRgbCode) == 4:
        r1 = int(strRgbCode[1: 2],16) * 16
        g1 = int(strRgbCode[2: 3],16) * 16
        b1 = int(strRgbCode[3: 4],16) * 16
    else:    
        r1 = int(strRgbCode[1: 3],16)
        g1 = int(strRgbCode[3: 5],16)
        b1 = int(strRgbCode[5: 7],16)
    minDistance = (r1 * r1) + g1 * g1 + b1 * b1

    for color in lstColorCodes:
        if not color[1].startswith("#"):
            raise Exception("wrong color format")

        r2 = int(color[1][1: 3],16)
        g2 = int(color[1][3: 5],16)
        b2 = int(color[1][5: 7],16)
        Distance = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

        if Distance < minDistance:
            strColorName = color[0].lower()
            minDistance = Distance

    return strColorName


def getColorDistance(strColorName1, strColorName2):

    r1 = 0
    r2 = 0
    g1 = 0
    g2 = 0
    b1 = 0
    b2 = 0
    for color in lstColorCodes:
        if strColorName1.upper() == color[0].upper():
            r1 = int(color[1][1: 3], 16)
            g1 = int(color[1][3: 5], 16)
            b1 = int(color[1][5: 7], 16)
        if strColorName2.upper() == color[0].upper():
            r2 = int(color[1][1: 3], 16)
            g2 = int(color[1][3: 5], 16)
            b2 = int(color[1][5: 7], 16)
    fn_return_value = (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2
    return fn_return_value


def composeQuadrantName(dsfLat, dsfLon):
    if dsfLat >= 0:
        fn_return_value = '+'
    else:
        fn_return_value = '-'
    fn_return_value = fn_return_value + ('00' + str(dsfLat))[-2:]
    if dsfLon >= 0:
        fn_return_value = fn_return_value + '+'
    else:
        fn_return_value = fn_return_value + '-'
    fn_return_value = fn_return_value + ('000' + str(dsfLon))[-3:]

    return fn_return_value


def getTimeStamp():
    dateTimeObj = datetime.now()
    return str(dateTimeObj.year)+'.'+str(dateTimeObj.month).zfill(2)+'.'+str(dateTimeObj.day).zfill(2)+" "+str(dateTimeObj.hour).zfill(2) + ':'+ str(dateTimeObj.minute).zfill(2) + ':' + str(dateTimeObj.second).zfill(2)

def safeString(s):
    s=s.replace("\xab","\"") 
    s=s.replace("\xbb","\"")
    return s 

#====================================================================================
# home-brew relational DB interface
# plain text files pipe (|) separated
#====================================================================================
def endcodeDatString(s):
    # we only need to encode pipe simbol
    s=s.replace(r'|', r'&#124;') 
    return s

def decodeDatString(s):
    s=s.replace(r"&#124;", r"|") 
    return s

def loadDatFile(strInputFile, encoding="utf-8"):
    cells = []
    filehandle = open(strInputFile, 'r', encoding=encoding)
    txt = filehandle.readline().strip()
    while len(txt) != 0:
        if not txt.startswith("#"):
            row = txt.strip().split("|")
            for i in range(len(row)):
                row[i] = decodeDatString(row[i].strip())
            if len(row)>1:
                cells.append(row)
        txt = filehandle.readline()
    # end of while
    filehandle.close()
    return cells

def saveDatFile(cells,strOutputFile):

    filehandle = open(strOutputFile, 'w', encoding="utf-8" )
    for row in cells:
        txt = "" 
        for field in row: 
            if txt!="":
                txt = txt + "|"   
            txt = txt + endcodeDatString(field)
        filehandle.write(txt+'\n') 
    filehandle.close()   
