import bpy
import sys
import os 


print("osm2blender scripts, (c) Zkir 2018")

#===============================================================
# get parameters and default values.
#===============================================================
#get the names of the input and output files
#we obtain them from blender command line
if len(sys.argv)>=6:
    strInputFileName=sys.argv[5]
else:     
    strInputFileName='d:\\_BLENDER-OSM-TEST\\samples\\Church-vozdvizhenskoe.osm'


if len(sys.argv)>=7:
    WorkDir=sys.argv[6]
else:     
    WorkDir='d:\\_BLENDER-OSM-TEST\\output'

#WorkDir =os.getcwd()

print("we will load osm file " + strInputFileName)
print("output directory: " + WorkDir ) 

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
# Let's do some cleanup
#===============================================================
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)
# collection will be recreated by blender-osm-plugin

#===============================================================
# import osm file and create mesh
# blender-osm plugin is used.
#===============================================================
#bpy.ops.object.mode_set(mode='OBJECT') 
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.data.scenes["Scene"].blender_osm.osmSource = 'file'
bpy.data.scenes["Scene"].blender_osm.highways = False
bpy.data.scenes["Scene"].blender_osm.vegetation = False
bpy.data.scenes["Scene"].blender_osm.osmFilepath = strInputFileName

bpy.ops.blender_osm.import_data()

#===============================================================
# we need new uv-map for baking
# so we will create uv-coordinates
#===============================================================
#we need to select the first and the single object in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active= bpy.context.scene.objects[0]

bpy.ops.object.mode_set(mode='EDIT') 
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.uv_texture_add()
bpy.ops.uv.smart_project(angle_limit =30, island_margin=0.1, user_area_weight=1, use_aspect=True)

#create new image to bake
img=bpy.data.images.new("baked", 1024, 1024, alpha=False, float_buffer=False, stereo3d=False)
#img.filepath_raw = strMainTextureName
img.filepath = strMainTextureName
img.file_format = 'PNG'
img.save()

bpy.ops.object.mode_set(mode='OBJECT') 
bpy.context.scene.render.engine = 'CYCLES'


#===============================================================
# We need to add a nodes for texture for each material
# this is how baking works in cycles. 
# Target texture should be active in material node tree.
#===============================================================
# https://blender.stackexchange.com/questions/5668/add-nodes-to-material-with-python

for mat in bpy.data.materials:  
    node_tree=mat.node_tree
    if not (node_tree is None):
        nodes=node_tree.nodes
        node1 = nodes.new('ShaderNodeTexImage')
        node1.location = (00, -200)
        node1.image=img

        node2 = nodes.new('ShaderNodeUVMap')
        node2.uv_map = "UVMap"
        node2.location = (-200, -200)

        node_tree.links.new(node2.outputs["UV"], node1.inputs["Vector"])
        node1.select=True
        node_tree.nodes.active = node1
        


print("saving as blender file "+ strOutputFileName)
bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)


#===============================================================
# bake texture
#===============================================================
bpy.context.scene.cycles.bake_type = 'DIFFUSE'
bpy.context.scene.render.bake.margin = 2
bpy.context.scene.render.bake.use_pass_direct=False
bpy.context.scene.render.bake.use_pass_indirect=False
bpy.context.scene.render.bake.use_pass_color=True

#Bake the texture
bpy.ops.object.bake(type='DIFFUSE') 

#===============================================================
# add x-plane attributes. xplane2blender plugin is used.
#===============================================================
#bpy.ops.scene.add_xplane_layers()
#we need to use the last collection, which was created by blender-osm
xplane_layer=bpy.data.collections[-1].xplane.layer
bpy.data.collections[-1].xplane.is_exportable_collection = True
xplane_layer.expanded = True

xplane_layer.export_type = 'scenery'
xplane_layer.name = strObjectName
xplane_layer.autodetectTextures = False
xplane_layer.texture = strObjectName +'.png'


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

