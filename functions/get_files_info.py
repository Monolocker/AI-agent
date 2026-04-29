import os
from google.genai import types

# Tells the LLM how the function should be called
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_path_working = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_path_working, directory))

    # target_dir falls within abs_path_working, finding longest sub_path shared by the two. Will be True or False
    valid_target_dir = os.path.commonpath([abs_path_working, target_dir]) == abs_path_working

    # Reject paths and escape the sandbox (ex: "/bin" or "../")
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Confirm target is actually a directory (not a file or missing path)
    try:
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error: {e}"
    
    # Read directory's contents. Returns a list of strings: ["main.py", "pkg", "tests.py"]
    try:
        dir_content = os.listdir(target_dir)
    except Exception as e:
        return f"Error: {e}"
    
    items = []
    for item in dir_content:
        try: 
            item_path = os.path.normpath(os.path.join(target_dir, item))
            items.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}")
        except Exception as e:
            return f"Error: {e}"
     
    return "\n".join(items)

