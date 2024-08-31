import json
from mdlStartDate import parseStartDate


"""

-- statistics only
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
    
def log_error(s, part_id):
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
           errors.append(log_error('Unparsed start_date value: ' + tags["start_date"], part_id))    
   
    
    if ("height" not in tags) and ("building:levels" not in tags):
        # missing height 
        # height should be present in tags
        # building part cannot be rendered without height 
        if is_building_part:  
            errors.append(log_error("Height tag is missing", part_id))
    else: 
        if tags.get("height","") == "0" or  tags.get("building:levels","") == "0":
            if is_building_part:
                errors.append(log_error("Zero height is not allowed for building parts", part_id))
            else:
                errors.append(log_error("Zero height is not recommended for buildings", part_id))
        
        
    if "roof:orientation" in tags: #=along/across  
        if tags["roof:orientation"] not in roof_orientations: 
            errors.append(log_error("Unknown roof orientation " + tags["roof:orientation"], part_id))

           
    if "roof:direction" in tags: #roof direction can be angle or direction code (NNW, SE etc)  
        if tags["roof:direction"] not in roof_directions and not (checkFloat(tags["roof:direction"])): 
            errors.append(log_error("Invalid value for roof direction: " + tags["roof:direction"], part_id))            

    
    if "roof:shape" in tags: 
        if tags["roof:shape"] not in roof_shapes: 
            if tags["roof:shape"] == "many":
                if is_building_part:
                    errors.append(log_error("Roof shape 'many' is not allowed for building parts", part_id))   
                else:
                    # roof:shape=many is allowed for buildings 
                    pass                 
            else:           
                errors.append(log_error("Unknown roof shape: " + tags["roof:shape"], part_id))    
                        

    for key in tags:
        if key in meter_value_tags:
            if not checkMeter(tags[key]):
                errors.append(log_error("Invalid value for "+ key + " tag: "+tags[key], part_id))        
    
        if key in float_value_tags:
            if not checkFloat(tags[key]):
                errors.append(log_error("Invalid value for "+ key + " tag: "+tags[key], part_id))        
                
        if key in integer_value_tags:
            if not checkInt(tags[key]):
                errors.append(log_error("Invalid value for "+ key + " tag: "+tags[key], part_id)) 
    
    if "building:height" in tags:
        errors.append(log_error("building:height is deprecated, use height instead", part_id)) 
        
    return errors

def dump_errors(strOutputFileName, errors):    
    #if len(errors)>0:
    #   print(errors) 
       
    with open(strOutputFileName, 'w',encoding="utf-8") as f:
        json.dump(errors, f, indent=4)