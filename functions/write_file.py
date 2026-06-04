import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description= "write speciefied content to the file on the specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to write content to, relative to the working directory"
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="Content that will be written to the specified file"
            )
        },
        required=["file_path","content"]
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
    except Exception as e:
        return f'Error: {e}'
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        if not os.path.exists(target_file):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'