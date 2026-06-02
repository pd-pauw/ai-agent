import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    except Exception as e:
        return f'Error: {e}'
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
       return f'Error: "{directory}" is not a directory'
    
    file_info = []
    try:
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            file_info.append(f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}")
        
        return "\n".join(file_info)
                             
    except Exception as e:
        return f'Error: {e}'

