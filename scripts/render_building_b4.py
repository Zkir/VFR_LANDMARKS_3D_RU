import bpy
import math
import os
from mathutils import Vector


# Автоматическое кадрирование объектов с возможностью смещения взгляда вниз
def frame_camera_to_objects(camera, objects, margin=2, look_down_factor=0):
    min_coord = Vector((100000, 100000, 100000))
    max_coord = Vector((-100000, -100000, -100000))
    
    for obj in objects:
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ Vector(corner)
            min_coord.x = min(min_coord.x, world_corner.x)
            min_coord.y = min(min_coord.y, world_corner.y)
            min_coord.z = min(min_coord.z, world_corner.z)
            max_coord.x = max(max_coord.x, world_corner.x)
            max_coord.y = max(max_coord.y, world_corner.y)
            max_coord.z = max(max_coord.z, world_corner.z)
    
    center = (min_coord + max_coord) / 2
    size = max_coord - min_coord
    
    # Рассчитываем соотношение сторон кадра
    aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
    
    effective_size = max(
        size.x / aspect_ratio,
        size.y / aspect_ratio,
        size.z
    )
    
    distance = (effective_size**1.08) * margin
    # Позиция камеры (сверху-спереди-сбоку)
    camera.location = center + Vector((distance, -distance, distance * 0.6))
    
    # Смещаем точку фокусировки вниз
    focus_point = center.copy()
    focus_point.z -= size.z * look_down_factor
    
    # Направляем камеру на смещенную точку фокусировки
    direction = focus_point - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()


def configure_world_lighting():
    scene = bpy.context.scene
    world = scene.world
    
    # Создаем новый world если отсутствует
    if world is None:
        world = bpy.data.worlds.new("RenderWorld")
        scene.world = world
    
    # Включаем ноды и настраиваем освещение
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    
    # Очищаем существующие ноды
    nodes.clear()
    
    # Создаем ноды для освещения
    bg_node = nodes.new(type='ShaderNodeBackground')
    env_node = nodes.new(type='ShaderNodeTexEnvironment')
    output_node = nodes.new(type='ShaderNodeOutputWorld')
    mix_node = nodes.new(type='ShaderNodeMixShader')
    ao_node = nodes.new(type='ShaderNodeAmbientOcclusion')
    
    # Позиционируем ноды
    bg_node.location = (400, 0)
    env_node.location = (-300, 0)
    output_node.location = (800, 0)
    mix_node.location = (600, 0)
    ao_node.location = (200, 0)
    
    # Создаем стандартную HDRI текстуру
    env_node.image = bpy.data.images.new("DefaultHDRI", 1024, 1024)
    env_node.image.generated_type = 'COLOR_GRID'
    
    # Настраиваем Ambient Occlusion
    ao_node.samples = 32  # Качество AO
    ao_node.inside = True  # Учитывать внутренние поверхности
    
    # Соединяем ноды
    links.new(env_node.outputs['Color'], bg_node.inputs['Color'])
    links.new(bg_node.outputs['Background'], mix_node.inputs[1])
    links.new(ao_node.outputs['Color'], mix_node.inputs[2])
    links.new(mix_node.outputs['Shader'], output_node.inputs['Surface'])
    
    # Настраиваем интенсивность
    bg_node.inputs['Strength'].default_value = 1.5  # Ярче базовый свет
    mix_node.inputs['Fac'].default_value = 0.3     # Баланс между основным светом и AO


def configure_render_settings():
    scene = bpy.context.scene
    
    # Переключаем на Cycles
    scene.render.engine = 'CYCLES'
    
    # Настройки Cycles
    scene.cycles.samples = 128  # Качество рендеринга
    scene.cycles.use_denoising = True  # Шумоподавление
    scene.cycles.denoiser = 'OPTIX'  # Используем Optix для NVIDIA
    
    # Включаем Ambient Occlusion в сцене
    scene.cycles.use_ambient_occlusion = True
    scene.cycles.ao_factor = 1.0  # Сила эффекта
    scene.cycles.ao_distance = 5.0  # Расстояние эффекта
    
    # Настройки EEVEE (если вдруг переключимся обратно)
    #scene.eevee.use_gtao = True
    #scene.eevee.gtao_factor = 1.0
    #scene.eevee.gtao_distance = 5.0


def main():
    # Определение пути вывода
    if bpy.data.filepath:
        blend_path = bpy.data.filepath
        directory = os.path.dirname(blend_path)
        filename = os.path.splitext(os.path.basename(blend_path))[0]
        output_path = os.path.join(directory, filename + "_render.png")
    else:
        output_path = "//building_render.png"
    
    # Настройки рендеринга
    scene = bpy.context.scene
    scene.render.resolution_x = 512
    scene.render.resolution_y = 256
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = True
    scene.render.filepath = output_path

    # Удаление источников света
    lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
    for light in lights:
        bpy.data.objects.remove(light)

    # Настройка освещения и рендера
    configure_world_lighting()
    configure_render_settings()

    # Создание/получение камеры
    if "RenderCamera" in bpy.data.objects:
        cam_object = bpy.data.objects["RenderCamera"]
    else:
        cam_data = bpy.data.cameras.new(name="RenderCamera")
        cam_object = bpy.data.objects.new(name="RenderCamera", object_data=cam_data)
        bpy.context.collection.objects.link(cam_object)
    
    scene.camera = cam_object
    cam_data = cam_object.data
    cam_data.clip_end = 10000.0

    # Кадрирование объектов
    mesh_objects = [obj for obj in scene.objects if obj.type == 'MESH']
    if mesh_objects:
        frame_camera_to_objects(cam_object, mesh_objects, look_down_factor=0)
    else:
        cam_object.location = (10, -10, 6)
        cam_object.rotation_euler = (
            math.radians(65),
            math.radians(0),
            math.radians(45)
        )

    # Рендеринг
    bpy.ops.render.render(write_still=True)
    print(f"Rendering completed. Image saved: {output_path}")


if __name__ == "__main__":
    main()