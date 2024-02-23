import functools
import hashlib
import os


def create_dirs_with_init_py(end_path, start_dir="."):
    # Ensure the start_dir is an absolute path
    start_dir = os.path.abspath(start_dir)

    # Construct the full path to the target directory
    # Split the relative path into its components
    relative_path = os.path.relpath(end_path, start_dir)
    dirs = relative_path.split(os.sep)

    # Create __init__.py along the relative path
    for i in range(1, len(dirs) + 1):
        # Construct the path up to the current depth within the relative path
        current_dir = os.path.join(start_dir, os.sep.join(dirs[:i]))
        if not os.path.exists(current_dir):
            # Create the directory if it doesn't exist
            os.makedirs(current_dir, exist_ok=True)
        init_file = os.path.join(current_dir, "__init__.py")
        if not os.path.isfile(init_file):
            # Create __init__.py if it doesn't exist
            open(init_file, "a").close()


def file_hash(file_path, hash_func=hashlib.md5):
    hash_obj = hash_func()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def get_directory_hashes(directory, hash_func=hashlib.md5):
    hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                relative_path = os.path.relpath(file_path, directory)
                hashes[relative_path] = file_hash(file_path, hash_func)
    return hashes


def get_changed_files(directory, hash_func=hashlib.md5):
    def decorator_check_files(func):
        @functools.wraps(func)
        def wrapper_check_files(*args, **kwargs):
            # Check file hashes before function execution
            before_hashes = get_directory_hashes(directory, hash_func)
            func(*args, **kwargs)  # Execute the function
            # Check file hashes after function execution
            after_hashes = get_directory_hashes(directory, hash_func)

            if before_hashes != after_hashes:
                out = {}
                for file_path in before_hashes:
                    if before_hashes[file_path] != after_hashes.get(file_path):
                        out[file_path] = (
                            before_hashes[file_path],
                            after_hashes.get(file_path),
                        )
                return out

            return {}

        return wrapper_check_files

    return decorator_check_files
