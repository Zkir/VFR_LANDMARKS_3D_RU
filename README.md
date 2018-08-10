# VFR_LANDMARKS_3D_RU
Visual landmarks for x-plane, based on osm-data and custom models in blender

## How does it work? ##

VBA macro in **osm-parser.xlsm** parses osm file (this osm file should be prepared using osm-filter), and creates a list of buildings which should be placed on a scenery (final DSF-TXT)

 **custom_models_list.txt** is used a 3D model library. It contains geographically placed custom objects (mostly churches), with their parameters (somewhat similar to the osm-tags), and reference to custom models. The *osm-parser.xlsm* tries to find most suitable object from  *custom_models_list.txt*

## ant-build (build.xml)  ##
Note that the build process is NOT fully automated. some steps should be done manually.

### What does the ant-build (build.xml) do? ###
It merely compiles binary DSF files from DSF-TXT and copies them as well as OBJs and other files to the build directory.

### What does the ant-build do NOT? ###
1)	It does not create dsf-txt. Those file(s) should be created via manual execution of VBA macro in **osm-parser.xlsm**
2)	It does not convert blender models (*.blend) to X-plane format (obj). It should be done manually via blender plug-in (xplane2blender)

## References ##
1) xplane2blender: https://xplane2blender.anzui.de/
2) X-plane tools: https://developer.x-plane.com/tools/xptools/
