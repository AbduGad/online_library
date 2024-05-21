

import os
import errno

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
source_path = parent_dir + r"/pdf"
destination_path = parent_dir + r"/web-dynamic/static/pdf"


def check_broken_Symbolic_link(destination_path):
    broken_slink_msg \
        = "is a broken symlink: please remove it and run the module again"
    try:
        os.stat(destination_path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise FileExistsError(
                f'{destination_path} {broken_slink_msg}')
        else:
            raise e


def main():
    if os.path.islink(destination_path):
        print(f"Symbolic link already exists: {destination_path}")
        check_broken_Symbolic_link(destination_path)

    elif os.path.exists(destination_path):
        print(f"Path exists but is not a symbolic link: {destination_path}")

    else:
        # Create the symbolic link
        os.symlink(source_path, destination_path, target_is_directory=True)
        print(f"Created symbolic link: {source_path} -> {destination_path}")


main()
