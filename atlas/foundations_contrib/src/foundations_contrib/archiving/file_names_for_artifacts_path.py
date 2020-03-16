
def file_names_for_artifacts_path(list_of_paths_from_os_walk):
    for directory, _, files in list_of_paths_from_os_walk:
        yield from _file_paths_for_directory(directory, files)
        

def _file_paths_for_directory(directory, files):
    from os.path import join

    for file_name in files:
        yield join(directory, file_name)