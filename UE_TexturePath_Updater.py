import unreal
import os

NEW_TEXTURES_FOLDER = r"Absolute_path_to_your_folder"

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
editor_asset_lib = unreal.EditorAssetLibrary()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

# Собираем новые файлы
new_files = {}
for root, dirs, files in os.walk(NEW_TEXTURES_FOLDER):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext.lower() in [".png", ".jpg", ".tga"]:
            new_files[name.lower()] = os.path.join(root, file)

unreal.log("🔍 Найдено {} новых текстур".format(len(new_files)))

# Все текстуры в Content
all_textures = [a for a in asset_registry.get_assets_by_class("Texture2D")
                if str(a.package_name).startswith("/Game/")]

unreal.log("📦 В Content найдено {} текстур".format(len(all_textures)))

for asset_data in all_textures:
    tex_name = str(asset_data.asset_name)
    tex_path = asset_data.object_path
    unreal.log("👉 Проверяю: {} ({})".format(tex_name, tex_path))

    if tex_name.lower() in new_files:
        texture = editor_asset_lib.load_asset(tex_path)
        new_file_path = new_files[tex_name.lower()]
        unreal.log("   ✅ Нашёл новый файл: {}".format(new_file_path))

        # Создаём задачу на импорт для замены ассета
        task = unreal.AssetImportTask()
        task.filename = new_file_path
        # Приводим к строке перед rsplit
        package_name_str = str(asset_data.package_name)
        task.destination_path = package_name_str.rsplit("/", 1)[0]
        task.destination_name = tex_name
        task.replace_existing = True
        task.automated = True
        task.save = True

        # Импортируем (заменяем)
        asset_tools.import_asset_tasks([task])
        unreal.log("   🎉 Успешно заменено и реимпортировано: {}".format(tex_name))
    else:
        unreal.log("   ⛔ Файл не найден для: {}".format(tex_name))
