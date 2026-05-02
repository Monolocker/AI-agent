import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Ability to write and overwrite files, within strict limits from within the permitted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write or overwrite, relative to the working directory",
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write or overwrite into the file",
            ),
        },
    ),
)



def write_file(working_directory, file_path, content):
    try:
        abs_path_working = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path_working, file_path))

        valid_target_file = os.path.commonpath([abs_path_working, target_file]) == abs_path_working
        if not valid_target_file:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        # Reject writes to existing directories 
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Create any missing parent directories w/o raising error if already exists 
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Overwrite (or create) the file with the provided content
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error writing to file: {e}'