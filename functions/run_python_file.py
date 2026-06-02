import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
    except Exception as e:
        return f'Error: {e}'
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path.split(".")[1] != "py":
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, text=True, timeout=30 , cwd=working_directory_abs, capture_output=True)
        output = ""
        if completed_process.returncode > 0 :
            output += f"Process exited with code {completed_process.returncode} \n"
        if not completed_process.stderr and not completed_process.stdout:
            output += "No output produced \n"
        else:
            if completed_process.stdout:
                output += f"STDOUT: {completed_process.stdout} \n"
            if completed_process.stderr:
                output += f"STDERR: {completed_process.stderr} \n"
    except Exception as e:
        return f"Error: {e}"
    
    return output