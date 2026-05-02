import os
from config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file's contents (truncated to a max length) from within the permitted working directory, or returns an error string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try: 

        abs_path_working = os.path.abspath(working_directory)

        # Build absolute, normalized path to target file 
        target_file = os.path.normpath(os.path.join(abs_path_working, file_path))

        # Ensure target file is in working directory 
        valid_target_file = os.path.commonpath([abs_path_working, target_file]) == abs_path_working
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS to avoid blowing through tokens
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            # If another character exists, the file was longer than MAX_CHARS 
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content 

    
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'