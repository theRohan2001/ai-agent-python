import os
import subprocess
from google.genai import types

def run_python_file(working_dir, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        valid_file = os.path.isfile(target_file)
        
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not valid_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        run = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_dir_abs)
        
        output = []

        if run.returncode != 0:
            output.append(f"Process exited with code {run.returncode}")  
        if not run.stderr and not run.stdout:
            output.append("No output produced")
        if run.stdout:
            output.append(f"STDOUT: {run.stdout}")
        if run.stderr:
            output.append(f"STDERR: {run.stderr}")

        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file in a specified file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run a python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to run a python file.",
            ),
        },
    ),
)