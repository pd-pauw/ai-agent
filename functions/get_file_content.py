import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content= types.FunctionDeclaration(
    name = "get_file_content",
    description= "read the content of the file on the specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to read content from, relative to the working directory"
            ),
        },
    required=["file_path"]),
    
)

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
    except Exception as e:
        return f'Error: {e}'
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
       return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file,"r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
   