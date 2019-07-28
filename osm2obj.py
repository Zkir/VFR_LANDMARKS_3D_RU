import bpy
import sys
import os 


print("osm2blender scripts, (c) Zkir 2018")

#===============================================================
# get parameters and default values.
#===============================================================
#get the names of the input and output files
#we obtain them from blender command line
strInputFileName=sys.argv[5] 
#strInputFileName='d:\\models-osm\\test.osm'

#WorkDir = os.path.dirname(os.path.realpath(__file__))
WorkDir =os.getcwd()
print("we will load osm file " + strInputFileName)
print("current directory: " + WorkDir ) 

strObjectName=strInputFileName
if strObjectName[-4:len(strObjectName)] ==".osm":
    strObjectName=strObjectName[0:-4]  

#get row object name, osm file name without extention and path.
k=-1
for i in range(len(strObjectName)):
    if strObjectName[i]=="\\" or strObjectName[i]=="//":
        k=i  
if k!=-1:
    strObjectName=strObjectName[k+1:len(strObjectName)] 


strOutputFileName =  os.path.join(WorkDir, strObjectName +".blend")
strMainTextureName = os.path.join(WorkDir, strObjectName +".png")
print(strMainTextureName)



#===============================================================
# import osm file and create mesh
# blender-osm plugin is used.
#===============================================================
#bpy.ops.object.mode_set(mode='OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.data.scenes["Scene"].blender_osm.osmSource = 'file'
bpy.data.scenes["Scene"].blender_osm.osmFilepath = strInputFileName
bpy.ops.blender_osm.import_data()

#===============================================================
# create uv-coordinates
# non-premium version of blender-osm does not create them
# so we have to do it ourselves.
#===============================================================
#we need to select the first and the single object in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.context.scene.objects.active= bpy.context.scene.objects[1]

bpy.ops.object.mode_set(mode='EDIT') 
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=0.25, user_area_weight=1)

#create new image to bake
img=bpy.data.images.new("baked", 1024, 1024, alpha=False, float_buffer=False, stereo3d=False)
#img.filepath_raw = strMainTextureName
img.filepath = strMainTextureName
img.file_format = 'PNG'
img.save()

# a bit strange way to select image for baking
# currently no other is known. UV editor windows should be present.
for area in bpy.context.screen.areas:
         if area.type == 'IMAGE_EDITOR':
                 area.spaces.active.image = img

#===============================================================
# bake texture
#===============================================================
bpy.context.scene.render.bake_type = 'AO'
bpy.context.scene.render.bake_margin = 2
#Bake the image! 
bpy.ops.object.bake_image() 

#===============================================================
# add x-plane attributes. xplane2blender plugin is used.
#===============================================================
bpy.ops.scene.add_xplane_layers()
bpy.context.scene.xplane.layers[0].expanded = True
bpy.context.scene.xplane.layers[0].export_type = 'scenery'
bpy.context.scene.xplane.layers[0].name = strObjectName
bpy.context.scene.xplane.layers[0].autodetectTextures = False
bpy.context.scene.xplane.layers[0].texture = strObjectName +'.png'

#===============================================================
# save the resulting file as blender file, we can only export after save
#===============================================================
print("saving as blender file "+ strOutputFileName)
bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)

#===============================================================
# export to x-plane OBJ format. xplane2blender plugin is used.
#===============================================================
bpy.ops.scene.export_to_relative_dir()
img.save()

print ("done")




