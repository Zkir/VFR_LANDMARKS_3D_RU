import bpy

print("Exporting Custom Model to X-Plane format...")
try:
    # Используем плагин xplane2blender для экспорта в относительную директорию
    # Файл .obj будет создан рядом с .blend файлом
    bpy.ops.scene.export_to_relative_dir()
    print("Export successful.")
except Exception as e:
    print(f"Error during export: {e}")
