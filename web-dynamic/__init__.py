

import os
import errno

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
source_path = parent_dir + r"/pdf"
destination_path = parent_dir + r"/web-dynamic/static/pdf"


def remove_path(path):
    if os.path.isfile(path) or os.path.islink(path):
        # It's a file or symbolic link
        os.remove(path)
        print(f'Removed file or symbolic link: {path}')
    elif os.path.isdir(path):
        import shutil
        # It's a directory
        shutil.rmtree(path)
        print(f'Removed directory: {path}')
    else:
        print(f'The path does not exist: {path}')


def check_broken_Symbolic_link(destination_path):
    broken_slink_msg \
        = "is a broken symlink: please remove it and run the module again"
    try:
        os.stat(destination_path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            remove_path(path=destination_path)
            os.symlink(source_path, destination_path, target_is_directory=True)
        else:
            raise e


def main():
    if os.path.islink(destination_path):
        print(f"Symbolic link already exists: {destination_path}")
        check_broken_Symbolic_link(destination_path)

    elif os.path.exists(destination_path):
        print(f"Path exists but is not a symbolic link: {destination_path}")
        remove_path(path=destination_path)
        os.symlink(source_path, destination_path, target_is_directory=True)
        print(f"Created symbolic link: {source_path} -> {destination_path}")
        # raise FileExistsError(
        #     f"Path exists but is not a symbolic link: {destination_path}")

    else:
        # Create the symbolic link
        os.symlink(source_path, destination_path, target_is_directory=True)
        print(f"Created symbolic link: {source_path} -> {destination_path}")


main()
