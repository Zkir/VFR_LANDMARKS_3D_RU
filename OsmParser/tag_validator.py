import json
from mdlStartDate import parseStartDate


"""

-- We do not check those tags, but could in the future
building:part 
roof:colour, 
building:colour
building:material=*
roof:material=*

"""

#TODO: Obviously should be checked with blender-osm
roof_shapes = [ "flat",	"gabled", "gabled_height_moved", "skillion",  
                "hipped", "half-hipped", "side_hipped", "side_half-hipped",
                "hipped-and-gabled", "mansard", "gambrel",
                "pyramidal", "crosspitched", "sawtooth", "butterfly",
                "cone", "dome", "onion", "round",
                "saltbox", #not in the original Simple3D, but supported by F4 and blender-osm
                "half-dome", "zakomar" # additions by zkir to blender-osm
                ]
                
roof_orientations = ["along", "across"]
roof_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

#we have several groups of tags. 
#1. tags which reflect heigth, probably with unit. Blender-osm does not understand units though. 
#2. tags of float value like angle and direction
#3. tags of integer value, like leveles.

meter_value_tags = ["height", "min_height","roof:height"]
float_value_tags = ["roof:angle" ]
integer_value_tags = [ "building:levels" , "building:min_level", "roof:levels"]


def checkInt(s):
    try:
        n = int(s)
        r = True
    except ValueError:
        r=False 
    return r

def checkFloat(s):
    try:
        n = float(s)
        r = True
    except ValueError:
        r=False 
    return r

def checkMeter(s):    
    return checkFloat(s)    
    
    
# Erorrs
UNPARSED_START_DATE =        "Неразбочивое значение даты постройки: {}" #"Unparsed start_date value: {}"
HEIGHT_TAG_MISSING =         "Ни высота, ни этажность не заданы" #"Height tag is missing"
ZERO_HEIGHT_BUILDING_PART =  "Нулевая высота не разрешается для частей здания" #"Zero height is not allowed for building parts" 
ZERO_HEIGHT_BUILDING =       "Зданий с нулевой высотой не бывает" #"Zero height is not recommended for buildings"
UNKNOWN_ROOF_ORIENTATION =   "Неизвестная ориентация крыши: {}" #"Unknown roof orientation {} "
UNKNOWN_ROOF_DIRECTION =     "Неизвестное направление крыши: {}" #"Invalid value for roof direction: {}"
UNKNOWN_ROOF_SHAPE =         "Неизвестная форма крыши: {}" #"Unknown roof shape {} "
ROOF_SHAPE_MANY =            "Тег roof:shape=many не допустим для частей здания" #"Roof shape 'many' is not allowed for building parts"
INVALID_VALUE_FOR_KEY =      "Недопустимое значение для тега {}: {}" #"Invalid value for {} tag: {}"
DEPRECATED_BUILDING_HEIGHT = "Тег building:height устарел, используйте просто height" #"building:height is deprecated, use height instead"
SINGLE_BUILDING_PART =       "Здание из одной-единственной части не имеет большого смысла и это практически всегда ошибка"         
HEIGHT_DISCREPANCY   =       "Высота указанная на здании ({} м) и вычисленная по частям ({} м) сильно различаются"      
    
def log_error(part_id, s, *data ):
    s=s.format(*data)
    #print("Error: " + s + ", building part "+ str(part_id)) 
    return {"error":s, "part_id":part_id}
    
    
def validate_tags(part_id, osmtags, is_building_part):
    tags = {} 
    errors = []
    ## convert to dictionary 
    #for tag in osmtags:
    #    tags[tag[0]] = tag[1]
    
    tags = osmtags
        
    if "start_date" in tags: 
        if tags["start_date"] != "" and parseStartDate(tags["start_date"]) is None:    
           errors.append(log_error(part_id, UNPARSED_START_DATE,  tags["start_date"] ))    
   
    
    if ("height" not in tags) and ("building:levels" not in tags):
        # missing height 
        # height should be present in tags
        # building part cannot be rendered without height 
        if is_building_part:  
            errors.append(log_error(part_id, HEIGHT_TAG_MISSING))
    else: 
        if tags.get("height","") == "0" or  tags.get("building:levels","") == "0":
            if is_building_part:
                errors.append(log_error(part_id, ZERO_HEIGHT_BUILDING_PART))
            else:
                errors.append(log_error(part_id, ZERO_HEIGHT_BUILDING ))
        
        
    if "roof:orientation" in tags: #=along/across  
        if tags["roof:orientation"] not in roof_orientations: 
            errors.append(log_error(part_id, UNKNOWN_ROOF_ORIENTATION, tags["roof:orientation"] ))

           
    if "roof:direction" in tags: #roof direction can be angle or direction code (NNW, SE etc)  
        if tags["roof:direction"] not in roof_directions and not (checkFloat(tags["roof:direction"])): 
            errors.append(log_error(part_id, UNKNOWN_ROOF_DIRECTION,  tags["roof:direction"]))            

    
    if "roof:shape" in tags: 
        if tags["roof:shape"] not in roof_shapes: 
            if tags["roof:shape"] == "many":
                if is_building_part:
                    errors.append(log_error(part_id, ROOF_SHAPE_MANY ))   
                else:
                    # roof:shape=many is allowed for buildings 
                    pass                 
            else:           
                errors.append(log_error(part_id, UNKNOWN_ROOF_SHAPE, tags["roof:shape"] ))    
                        

    for key in tags:
        if key in meter_value_tags:
            if not checkMeter(tags[key]):
                errors.append(log_error(part_id, INVALID_VALUE_FOR_KEY, key, tags[key]))        
    
        if key in float_value_tags:
            if not checkFloat(tags[key]):
                errors.append(log_error(part_id, INVALID_VALUE_FOR_KEY, key, tags[key]))        
                
        if key in integer_value_tags:
            if not checkInt(tags[key]):
                errors.append(log_error(part_id, INVALID_VALUE_FOR_KEY, key, tags[key])) 
    
    if "building:height" in tags:
        errors.append(log_error(part_id, DEPRECATED_BUILDING_HEIGHT )) 
        
    return errors

def dump_errors(strOutputFileName, errors):    
    #if len(errors)>0:
    #   print(errors) 
       
    with open(strOutputFileName, 'w',encoding="utf-8") as f:
        json.dump(errors, f, indent=4) # , ensure_ascii=False