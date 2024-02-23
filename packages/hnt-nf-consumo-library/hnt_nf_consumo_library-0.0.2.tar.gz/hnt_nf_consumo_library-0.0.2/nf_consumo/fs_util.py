from os import getcwd, makedirs, path

DEFAULT_OUTPUT = "output"

def local_saved_path(url, dest_dir=DEFAULT_OUTPUT):
    path_dir = path.join(getcwd(), dest_dir)
    if not path.exists(path_dir):
        makedirs(path_dir)
    filename = url.rsplit('/', 1)[-1]

    return {
        "path_dir" : path_dir,
        "filename": filename,
        "full_path": path.join(path_dir, filename)
    }
