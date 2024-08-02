from pathlib import Path


def read_file(file_name, dir_path=None):
    if not dir_path:
        file_path = file_name
    else:
        file_path = Path(dir_path).joinpath(file_name)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("File not found.")
    except IOError:
        print("An error occurred while reading the file.")


def write_file(file_name, content, dir_path=None):
    if not dir_path:
        file_path = file_name
    else:
        file_path = Path(dir_path).joinpath(file_name)
    
    # Extract directory path
    directory = Path(file_path).parent

    # Check if directory exists, create if not
    if not directory.exists():
        directory.mkdir(parents=True)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError:
        print("An error occurred while writing the file.")