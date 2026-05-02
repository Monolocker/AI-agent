import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output, with an optional list of CLI arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional list of CLI arguments to pass to the python file",
                ),
                description="Optional list of CLI arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None): 
    try:
        abs_path_working = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path_working, file_path))

        valid_target_file = os.path.commonpath([abs_path_working, target_file]) == abs_path_working
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        # Build command for subprocess run
        command = ["python", target_file]

        # If any additional args provided
        if args:
            command.extend(args)

        # Capture CompletedProcess object with result variable    
        result = subprocess.run(
            command,
            cwd=abs_path_working,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output string based on CompletedProcess object
        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")

        return "\n".join(output)


    except Exception as e:
        return f"Error: executing Python file: {e}"