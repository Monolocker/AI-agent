import os 
import subprocess

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