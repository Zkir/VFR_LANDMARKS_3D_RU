# VFR_LANDMARKS_3D_RU
Project to create visual landmarks for x-plane, based on osm-data and custom models in blender

## How does it work? ##
The process works in the good old way:
1. The planet.osm.pbf (or rather the country extract) is downloaded then updated (osmconvert, osmupdate, osmfilter and osmosis are used for this purpose). 
2. Osm-xmls with buildings and parts are extracted, lists of the extracted osm-xml are created.
3. Additionally, those buildings are checked for errors, error messages are saved into corresponding dat file.
4. 3D models are created via Blender with Blender-OSM plugin, textures are baked.
5. Experimental feature: 3D models are created also via osm2world (it seems that osm2world currently is much more buggy, but it supports windows:* tags)
6. 3D models are exported from blender into x-plane format via xplane2blender plugin
7. x-plane .obj files are converted to x3d files, since there is simple library to display them on web. 
8. x-plane scenery package is compliled. 
9. All that is copied to 3dcheck folder, where it can be displayed on web by Apache.

 

## How to install? ##
###  Windows ###
1. Clone the git repostitory. Directory should be **d:\\_VFR_LANDMARKS_3D_RU**
2. Install dependencies (see below).
3. Run run_validator.bat
4. Enjoy.

### Linux ###
You are free and open to do whatever you please.  Most likely it is needed to change backslashes to slashes in paths, and rewrite bats to sh.
Everything else should be cross platform. WINE may be an option too.


### Dependencies ###
Known dependencies include:
1. GNU Make
2. touch utility
3. aria2
4. wget
5. OsmTools (osmupdate, osmconvert, osmfilter)
6. osmosis
7. Python (currenty 3.12.7 is used)
8. Some Python libraries are needed to be installed. [requirements.txt](requirements.txt) could help.
9. Blender 2.79b
10. Blender-osm plugin (version 2.3.6 is used, compartible with Blender 2.79b )
11. Patch for the Blender-osm plugin, to support additional roof shapes. Included into this [repository](blender-osm-patch).
12. Blender Startup file (not sure where it is now)
13. xplane2blender plugin (version 3.5.0 is used, compartible with Blender 2.79b)
14. x-plane tools
15. Osm2world
16. Apache web server, for frontend. 

## References ##
1) X-plane tools: https://developer.x-plane.com/tools/xptools/
2) xplane2blender: https://xplane2blender.anzui.de/
3) blender-osm plugin by vvoovv: https://gumroad.com/l/blender-osm
