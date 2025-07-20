#==========================================================================================================
# This script is a part of VFR_LANDMARKS_3D_RU project                                                    *
# it is intended to be run under Blender 3D version 4.4.3                                                 *
# What it does:                                                                                           *
#   It reads prepared osm-xml with a single building                                                      *
#   and save is as textured x-plane obj file suitable to be used in x-plane scenery.                      *
# Steps :                                                                                                 *  
#  1. read osm-xml file via blosm (formely blender-osm plugin)                                            *
#  2. optimize ("remesh") geometry                                                                        *
#  3. bake materials as a single png texture file, since x-plane does not understand blender materials.   *
#  4. export obj via xplane2blender plugin                                                                *
#==========================================================================================================

import bpy
import sys
import os 
import random
import bmesh
from mathutils import Vector

def checkPlugins():
    """ Make sure that all necessary plugins are present and activated """
    
    if "blosm" not in bpy.context.preferences.addons:
        print("Blosm (formerly Blender-OSM) is not installed or enabled")
        return False
        
    if "bl_ext.blender_org.bool_tool" not in bpy.context.preferences.addons:
        print("Addon Bool Tool is not enabled")
        return False
    
    if "io_xplane2blender" not in bpy.context.preferences.addons:
        print("Addon io_xplane2blender is not installed or enabled")
        return False    
        
    return True

def getWorkingParameters():
    """ get parameters and default values, mainly names for the input and  output files """
    
    #get the names of the input and output files
    #we obtain them from blender command line
    #script parameters are passed after -- 
    if  '--' not in sys.argv:
        raise Exception('required script parameters are not supplied. input file name and working folder should be specified after --')
    k=sys.argv.index('--')
            
    
    inputfilename=sys.argv[k+1] 
    workdir = os.path.join(os.getcwd(), sys.argv[k+2])
    print("we will load osm file " + inputfilename)
    print("wordking directory: " + workdir ) 

    objectname=inputfilename
    if objectname[-4:len(objectname)] ==".osm":
        objectname=objectname[0:-4]  

    #get row object name, osm file name without extention and path.
    k=-1
    for i in range(len(objectname)):
        if objectname[i]=="\\" or objectname[i]=="//":
            k=i  
    if k!=-1:
        objectname=objectname[k+1:len(objectname)] 
    
    return inputfilename, objectname, workdir

def set_work_object():
    # 0. Находим первый объект в сцене
    #       После импорта должен быть один объект,
    #       Но по какой-то загадочной причине в коллекции есть еще что-то. 
    #       Поэтому мы берем первый mesh
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Этот объект становится активным и выбранным
            #bpy.context.scene.objects.active = obj
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)       
            return obj
    else:
        # для тупых: else после for выполняется, если break не сработал.
        raise Exception("Imported object is not found in the scene")

def is_watertight(obj):
    """Проверяет, является ли меш замкнутым объемом (watertight)"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Проверка на наличие граничных ребер
    for edge in bm.edges:
        if edge.is_boundary:
            bm.free()
            return False
    
    # Проверка на наличие незамкнутых граней
    for face in bm.faces:
        if len(face.verts) < 3:
            bm.free()
            return False
    
    bm.free()
    return True

def fix_normals(obj):
    """Исправляет направление нормалей объекта наружу"""
    # Переходим в режим редактирования
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Выделяем все и исправляем нормали
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Возвращаемся в объектный режим
    bpy.ops.object.mode_set(mode='OBJECT')

def has_degenerate_geometry(obj, threshold=0.0001):
    """Проверяет объект на наличие вырожденной геометрии"""
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    degenerate_found = False
    
    # 1. Проверка вершин: ищем дубликаты
    vert_coords = set()
    for vert in bm.verts:
        # Округляем координаты для избежания численных погрешностей
        coord = tuple(round(c, 6) for c in vert.co)
        if coord in vert_coords:
            degenerate_found = True
            break
        vert_coords.add(coord)
    
    # 2. Проверка ребер: нулевая длина
    if not degenerate_found:
        for edge in bm.edges:
            if edge.calc_length() < threshold:
                degenerate_found = True
                break
    
    # 3. Проверка граней: нулевая площадь
    if not degenerate_found:
        for face in bm.faces:
            if face.calc_area() < threshold:
                degenerate_found = True
                break
    
    # 4. Проверка на изолированные элементы
    if not degenerate_found:
        # Изолированные вершины (не принадлежат граням)
        for vert in bm.verts:
            if not vert.link_faces:
                degenerate_found = True
                break
        
        # Изолированные ребра (не принадлежат граням)
        if not degenerate_found:
            for edge in bm.edges:
                if not edge.link_faces:
                    degenerate_found = True
                    break
    
    bm.free()
    return degenerate_found

def clean_degenerate_geometry(obj, threshold=0.0001):
    """Автоматически исправляет вырожденную геометрию"""
    
    # Переходим в режим редактирования
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Выполняем серию операций очистки
    bpy.ops.mesh.select_all(action='SELECT')
    
    # 1. Удаление дубликатов вершин
    bpy.ops.mesh.remove_doubles(threshold=threshold)
    
    # 2. Удаление изолированных вершин и ребер
    bpy.ops.mesh.delete_loose()
    
    # 3. Удаление граней с нулевой площадью
    bpy.ops.mesh.dissolve_degenerate(threshold=threshold)
    
    # 4. Дополнительная очистка
    bpy.ops.mesh.fill_holes(sides=0)  # Автоматическое заполнение дыр
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Возвращаемся в объектный режим
    bpy.ops.object.mode_set(mode='OBJECT')


def get_mesh_stats(obj):
    """Возвращает статистику меша: количество вершин, граней и общую площадь"""
    if obj.type != 'MESH':
        return None
        
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Рассчитываем общую площадь
    total_area = 0.0
    for face in bm.faces:
        total_area += face.calc_area()
    
    stats = {
        'vertices': len(bm.verts),
        'faces': len(bm.faces),
        'total_area': total_area
    }
    
    bm.free()
    return stats

def remesh():
    """
      we want to optimize geometry. Since building is created from basic volumes, we want to find UNION and thus remove inner invisible faces.
    """
	
    print("optimizing geometry - preparation")

    # Сохраняем ссылку на исходный объект
    original_obj = bpy.context.active_object

    # Разделение объекта на отдельные меши по несвязным частям
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Собираем все созданные объекты после разделения
    separated_objs = [obj for obj in bpy.context.scene.objects 
                     if obj.name.startswith(original_obj.name) and obj != original_obj]
    all_objs = [original_obj] + separated_objs
    
    if len(all_objs) > 2000:
        raise Exception("There are too many parts, blender is not able to unite them")
        
    print("   parts found: ", len(all_objs))    
    
    # Проверка геометрии для всех вновь полученных объектов
	# К большому сожалению, эта проверка не эффективна, и bool_tool/union всё равно колбасит
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        # Выделяем текущий объект
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Проверка замкнутости
        if not is_watertight(obj):
            raise Exception("Object "+obj.name + " is not watertight (not a closed volume)")
        
        if has_degenerate_geometry(obj):
            #raise Exception("Object "+obj.name + " has degenerate geometry")
            print("Object "+obj.name + " has degenerate geometry")
            clean_degenerate_geometry(obj)
            if has_degenerate_geometry(obj):
                raise Exception("Object "+obj.name + " has degenerate geometry")
            
        # Снимаем выделение
        obj.select_set(False)
    
    #  Увеличиваем каждый меш на 1-2% относительно его геометрического центра
    #  Это нужно потому, что иначе UNION не работает, если кординаты граней одинаковы.
    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        # Выделяем текущий объект
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Проверка направления нормалей
        fix_normals(obj)

        # Перемещаем центр координат в геометрический центр
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        
        # а рандомизация нужна, чтобы _соседние_ внешние грани не глючили.
        r = random.random()/100
        # Применяем масштабирование
        obj.scale = (1.01 + r, 1.01 + r, 1.01 + r)
        bpy.ops.object.transform_apply(scale=True)
        
        # Снимаем выделение
        obj.select_set(False)
        
    print(" no geometry problems found")
    
    JUST_JOIN_BACK = 0
    BLENDER_BUILTIN = 2
    
    union_method = BLENDER_BUILTIN
    #union_method = JUST_JOIN_BACK
    
    if union_method == JUST_JOIN_BACK:
        print("Geometry optimization is not possible -- just join meshes back ")
        #just join meshes back, if we cannot do union
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()
        
    elif union_method == BLENDER_BUILTIN:    

        #Используем штатный метод булевых операций Blender вместо bool_tool 
        print("Optimizing geometry - union with built-in boolean operations")
        
        # Выбираем первый объект как базовый для объединения
        base_obj = all_objs[0]
        bpy.context.view_layer.objects.active = base_obj
        base_obj.select_set(True)
        
        # Последовательно объединяем все объекты
        for obj in all_objs[1:]:
            # Добавляем модификатор Boolean
            bool_mod = base_obj.modifiers.new(name="BooleanUnion", type='BOOLEAN')
            bool_mod.operation = 'UNION'
            bool_mod.object = obj
            
            # Применяем модификатор
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
            
            # Удаляем объединенный объект
            bpy.data.objects.remove(obj, do_unlink=True)
        
        result_obj = base_obj
        
    else:
        raise Exception("No method defined to union meshes")        
    
    print("Optimizing geometry - final cleanup")
    #we need to return ORIGIN back!
    bpy.context.scene.cursor.location = (0., 0., 0.)
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
    # 5. Финальная подчистка результата
    result_obj.name = "Combined_Mesh"

    # Удаляем дубликаты вершин
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)

    # Исправляем нормали
    bpy.ops.mesh.normals_make_consistent(inside=False)

    # Возвращаемся в Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')


    return
    
    
def remove_bottom_faces():
    """ bottom faces are not really necessary, we can remove them 
        IMPORTANT: this can be done only after remesh.            """
        
    result_obj = bpy.context.active_object
    print("remove bottom faces", result_obj.name)
    
    # 7. Удаление граней ниже Z=0
    bpy.ops.object.mode_set(mode='EDIT')

    # Создаем BMesh для точного контроля
    mesh = result_obj.data
    bm = bmesh.from_edit_mesh(mesh)

    # Выбираем все грани, где ВСЕ вершины имеют Z<0
    faces_to_remove = []
    for face in bm.faces:
        if all(v.co.z <= 0. for v in face.verts):
            faces_to_remove.append(face)

    # Удаляем выбранные грани
    if faces_to_remove:
        bmesh.ops.delete(bm, geom=faces_to_remove, context='FACES')  # context=5 -> FACES

    print("  removed " +str(len(faces_to_remove)) + " bottom faces" )    

    # Обновляем и освобождаем BMesh
    bmesh.update_edit_mesh(mesh)
    bm.free()

    # Возвращаемся в Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # 8. Финальная оптимизация
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)  # Повторное слияние после удаления
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return 


def createUVcoords():
    """ Generate UV (aka texture coordinates). we need them for baking """
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=0.001) 
    bpy.ops.object.mode_set(mode='OBJECT')
    

def update_materials(obj):
    """ Нам нужно, чтобы материалы были представлены НОДАМИ
        иначе запекание не работает. Кажется, что блосм создает материалы по старинке, без нод   """
        
    for material in obj.data.materials:
        if material.use_nodes:
            # material is already node-based, do nothing with it.
            continue
        else:    
            # create nodes and assign attributes
            old_diffuse_color =  material.diffuse_color
            old_specular_color =  material.specular_color
            material.use_nodes = True
            # As I know, currently blosm just uses color only (shame indeed)
            material.node_tree.nodes["Principled BSDF"].inputs[ 0].default_value = old_diffuse_color
            #print(material.node_tree.nodes["Principled BSDF"].inputs[14].default_value, old_specular_color)
            #material.node_tree.nodes["Principled BSDF"].inputs[14].default_value = old_specular_color
            


def bakeTexture(obj, img):
    """ Создаем или находим нод изображения в существующих материалах
        В CYCLES, чтобы текстура запекалась, нужно добавить ноду изображения в каждый материал. """
        
    if len(obj.data.materials) == 0:
        raise Exception("Cannot bake. No materials defined for this object")

    for material in obj.data.materials:
        
        if not material:
            raise Exception("Unexpected error: empty material")
            
        if not material.use_nodes:
            raise Exception('Material "' + material.name + '" is not node-based. we need node-based materials in order to make baking work!')
            
        nodes = material.node_tree.nodes
        tex_node = None
        
        # Ищем существующий нод изображения
        for node in nodes:
            if node.type == 'TEX_IMAGE':
                tex_node = node
                break
        
        # Если не нашли - создаем новый
        if not tex_node:
            tex_node = nodes.new('ShaderNodeTexImage')
            tex_node.location = (0, 0)
        
        # Назначаем наше изображение
        tex_node.image = img
        material.node_tree.nodes.active = tex_node


    # Устанавливаем изображение в UV-редактор
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            area.spaces.active.image = img

    # Настраиваем параметры запекания
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = False
    bpy.context.scene.render.bake.margin = 2
    bpy.context.scene.render.bake.use_selected_to_active = False
    bpy.context.scene.render.bake.target = 'IMAGE_TEXTURES'
    
    
    ## FOR TESTING ONLY: save before bake 
    #bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)

    # Запекаем 
    bpy.ops.object.bake(type='DIFFUSE')
    
    return     
    
    
def saveAsXPlaneObj(strOutputFileName, objectname):
    """Save as x-plane scenery object. xplane2blender plugin is used. 
	   in Blender 4.4.3 we use root object """
    
    obj = set_work_object()
    # add x-plane attributes.   
    obj.xplane.isExportableRoot = True
    obj.xplane.layer.export_type = 'scenery'
    obj.xplane.layer.name = objectname
    obj.xplane.layer.autodetectTextures = False
    obj.xplane.layer.texture = objectname +'.png'

    # save the resulting file as blender file, we can only export after save
    print("saving as blender file "+ strOutputFileName)
    bpy.ops.wm.save_as_mainfile(filepath=strOutputFileName)

    # export to x-plane OBJ format.
    bpy.ops.scene.export_to_relative_dir()


def main():
    print("osm2blender scripts, (c) Zkir 2018-2025")
    bversion=bpy.app.version
    if bversion!=(4,4,3):
        raise Exception("This script is supposed to be run under blender 4.4.3, but you have "+ bpy.app.version_string +  ". You may remove this check but you will be on your own!")
       
    random.seed(0)
    
    if not checkPlugins():
        raise Exception('Required plugins are not installed or enabled')

    # get parameters and default values.
    inputfilename, objectname, workdir =  getWorkingParameters()
    
    print(  os.path.join(os.getcwd(), inputfilename) )

    # import osm file and create mesh
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.blosm.osmSource = 'file'
    bpy.context.scene.blosm.buildings =  True
    bpy.context.scene.blosm.highways =   False
    bpy.context.scene.blosm.vegetation = False
    bpy.context.scene.blosm.forests =    False
    bpy.context.scene.blosm.railways =   False

    bpy.context.scene.blosm.osmFilepath = inputfilename
    bpy.ops.blosm.import_data()


    #================================================================
    # since blosm is patched to create bottom faces,
    # we can optimize geometry and remove the "inner" faces
    # to create single waterproof mesh and save space in texture file 
    #================================================================
    building = set_work_object()
    print("object to process identified:", building.name)
    if not objectname:
        objectname = building.name
    
    strOutputFileName =  os.path.join(workdir, objectname +".blend")
    strMainTextureName = os.path.join(workdir, objectname +".png")    

    stats_before = get_mesh_stats(building)
    
    remesh()
    
    # we better make sure to find our building once again, after remesh.
    # original object may be deleted.
    building = set_work_object()

    # we can remove bottom faces regardless remesh succeed  or not.
    remove_bottom_faces()        
    
    stats_after = get_mesh_stats(building) 
    # calculate and print optimization results
    area_diff = stats_before['total_area'] - stats_after['total_area']
    area_percent = (area_diff / stats_before['total_area']) * 100 if stats_before['total_area'] > 0 else 0
    
    print("\nRemesh results:")
    print(f"  Area of faces decreased: {area_diff:.2f} sq.m. ({area_percent:.1f}%)")
    print(f"  Vertices now : {stats_after['vertices']} (initially {stats_before['vertices']})")
    print(f"  Faces now: {stats_after['faces']} (initially {stats_before['faces']})")
    
    # we need to create UV maps, they will not create themselves!
    createUVcoords()
    
    #create new image to bake
    img = bpy.data.images.new("baked", 1024, 1024, alpha=False)
    img.filepath = strMainTextureName
    img.file_format = 'PNG'
    
    #hide EMPTY objects (aka groups), they prevent baking
    for obj in bpy.context.scene.objects:
        #print (obj.name, obj.type)
        if obj.type == 'EMPTY':
            obj.hide_viewport=True
            
    # in blender 4+, we need materials to be node-based.        
    update_materials(building)            
    
    # bake texture
    print("baking texture")
    bakeTexture(building, img)
    
    print("exporting to x-plane")
    saveAsXPlaneObj(strOutputFileName, objectname)
    
    img.save()

    print ("done")


main()

