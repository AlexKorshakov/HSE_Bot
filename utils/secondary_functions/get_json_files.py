import os


async def get_json_files(main_path) -> list:
    """
    """
    json_files = []
    for subdir, dirs, files in os.walk(main_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(".json"):
                json_files.append(filepath)
    return json_files