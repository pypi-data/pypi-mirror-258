
def create_file(file_path):
    try:
        with open(file_path, 'x') as f:
            pass  
    except FileExistsError:
        return