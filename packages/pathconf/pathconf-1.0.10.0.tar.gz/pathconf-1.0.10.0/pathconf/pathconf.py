import os
import re
import json
import queue
import errno
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global definitions
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, '.config', 'pathconf')
CONFIG_FILE = '.file_paths.json'
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
WORKERS = os.cpu_count() * 3


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def has_extension(filename):
    """
    Check if the given filename has an extension of
    reasonable length (5 characters or fewer).

    Parameters:
        filename (str): The filename to check.

    Returns:
        bool: True if the filename has an extension
        of reasonable length, False otherwise.
    """
    if '.' in filename:
        parts = filename.rsplit('.', 1)
        # Check if the part after the last '.' is 5 characters or fewer
        return len(parts[1]) <= 5
    return False


def search_directories(queue, dir_to_find, target, stop_event,
                       ignore_extension=False, search_folder=False,
                       deprecated=False, regex=False):
    while not queue.empty() and not stop_event.is_set():
        try:
            directory = queue.get_nowait()
        except queue.Empty:
            break

        if stop_event.is_set():
            break

        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                # Filter dirnames and filenames based on 'deprecated' flag
                if not deprecated:
                    dirnames[:] = [d for d in dirnames if 'Deprecated'
                                   not in d and 'deprecated' not in d]

                if stop_event.is_set():
                    break

                # Check if the current directory matches the partial directory
                if (dir_to_find and not os.path.normpath(
                   dirpath).endswith(os.sep + dir_to_find)):
                    continue
                if search_folder:
                    # Searching for directories
                    if target in dirnames:
                        stop_event.set()
                        return os.path.join(dirpath, target)
                else:
                    # Searching for files with regular expressions
                    if regex:
                        pattern = re.compile(target)
                        for filename in filenames:
                            if pattern.match(filename):
                                stop_event.set()
                                return os.path.join(dirpath, filename)
                    else:
                        # Standard file search
                        for filename in filenames:
                            if ignore_extension:
                                name_part = filename.rsplit('.', 1)[0]
                                if '.' in target and (filename.startswith
                                                      (target)):
                                    stop_event.set()
                                    return os.path.join(dirpath, filename)
                                elif name_part == target:
                                    stop_event.set()
                                    return os.path.join(dirpath, filename)
                            elif filename == target:
                                stop_event.set()
                                return os.path.join(dirpath, filename)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        finally:
            queue.task_done()

    return None


def load_json_config(file_path):
    """
    Load JSON configuration file. If the file does not exist,
    create a new empty JSON file.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Loaded JSON object or empty dictionary if file is invalid or new.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error("JSON Decode Error occurred")
        return {}
    except IOError as e:
        # Create the file if it doesn't exist
        if e.errno == errno.ENOENT:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump({}, f)
            logging.info(f"Created new config file: {file_path}")
            return {}
        else:
            logging.error(f"IOError occurred: {e}")
            return {}


def remove(target_path):
    if os.path.isfile(CONFIG_FILE_PATH):
        config = load_json_config(CONFIG_FILE_PATH)

        if target_path in config:
            del config[target_path]
            with open(CONFIG_FILE_PATH, 'w') as f:
                json.dump(config, f)
            logging.info(f"Removed {target_path} from config.")
        else:
            logging.info(f"{target_path} not found in config.")


def reset():
    """
    Reset the JSON configuration file, removing all items.
    """
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump({}, f)
    logging.info("Configuration file reset.")


def list_paths():
    """
    List all file paths stored in the JSON configuration file.

    Simply prints a list of key: value: pairs if config file exists.
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        paths = load_json_config(CONFIG_FILE_PATH)
        for key, value in paths.items():
            print(f"key: {key}, value: {value}")
    else:
        logging.info("No configuration file found.")


def get_paths():
    """
    List all file paths stored in the JSON configuration file.

    Returns:
        dict: A dictionary of all file paths in the config.
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        return load_json_config(CONFIG_FILE_PATH)
    else:
        logging.info("No configuration file found.")
        return {}


def find(target_path, folder=False, starting_dir=None,
         deprecated=False, regex=False):
    """
    Main function to find the path of a target file or folder,
    considering file extensions and the possibility that the
    target might be a folder. Can start the search from a specified directory.

    Parameters:
        target_path (str): Path (including optional directories) to search for.
        folder (bool): Whether to search for a folder instead of a file.
        starting_dir (str, optional): The starting directory for the search.

    Returns:
        str: Path to the found file or folder.

    Raises:
        FileNotFoundError: If the file or folder is not found.
    """
    index_suffix = '_folders.json' if folder else '.json'
    path_parts = []
    target = target_path
    dir_to_find = None
    # Split the target_path into directory (if any) and target
    if not regex:
        *path_parts, target = os.path.normpath(target_path).split(os.sep)
        dir_to_find = os.path.join(*path_parts) if path_parts else None

    index_file_to_check = (path_parts[0] + index_suffix if
                           path_parts else target + index_suffix)
    index_path = os.path.join(os.path.expanduser("~"),
                              '.config', 'pathconf', index_file_to_check)

    # Define the start path based on starting_dir or user's home directory
    start_path = os.path.expanduser(starting_dir) if starting_dir else HOME_DIR

    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index_data = json.load(f)
            # Validate if index is for the correct directory
            first_path = next(iter(index_data.get('items', {}).values()), None)
            if first_path and (os.path.commonpath([first_path, start_path])
                               == start_path):
                if target in index_data['items']:
                    return index_data['items'][target]

    # Determine whether to ignore file extension during the search
    ignore_extension = not has_extension(target) and not folder

    config_directory = os.path.join(HOME_DIR, '.config', 'pathconf')
    config_filename = '.file_paths.json'
    config_path = os.path.join(config_directory, config_filename)

    # Create the configuration directory if it doesn't exist
    os.makedirs(config_directory, exist_ok=True)

    # Load existing config or initialize new one
    config = load_json_config(config_path)

    # Check directly in the home directory
    # only if no directory part is provided in target_path
    if not dir_to_find:
        direct_path = os.path.join(start_path, target)
        found = False
        if folder:
            if os.path.isdir(direct_path):
                found = True
        else:
            if ignore_extension:
                found = any(f.split('.')[0] ==
                            target for f in os.listdir(start_path))
            else:
                found = os.path.isfile(direct_path)

        if found:
            config[target_path] = direct_path
            with open(config_path, 'w+') as f:
                json.dump(config, f)
            return direct_path

    dir_queue = queue.Queue()
    for d in os.listdir(start_path):
        if os.path.isdir(os.path.join(start_path, d)):
            dir_queue.put(os.path.join(start_path, d))

    stop_event = threading.Event()
    found_path = None

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(search_directories, dir_queue, dir_to_find,
                                   target, stop_event, ignore_extension,
                                   folder, deprecated, regex)
                   for _ in range(WORKERS)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_path = result
                break

    if found_path:
        config[target_path] = found_path
        with open(config_path, 'w+') as f:
            json.dump(config, f)
        return found_path
    else:
        raise FileNotFoundError(f"{target_path} not found.")


# def index(directory, exceptions=[], depth=-1, folders=False):
#     """
#     Function to index all files or folders in a given directory.

#     Parameters:
#         directory (str): Path to index.
#         exceptions (list, optional): List of subdir
#         exceptions (if folders = True then will
#             not index those folders either).
#         depth (int, optional): Depth to index.
#         folders (bool, optional): Whether to index folders instead of files.

#     Returns:
#         dict: Dictionary of files or folders in
#         given directory and subdirectories if depth is not 0.
#     """
#     directory_depth = directory.rstrip(os.sep).count(os.sep)
#     index_suffix = '_folders.json' if folders else '.json'
#     index_filename = (os.path.basename(os.path.normpath(directory))
#                       + index_suffix)
#     index_path = os.path.join(os.path.expanduser("~"), '.config',
#                               'pathconf', index_filename)

#     existing_index = {'depth': -1, 'items': {}}
#     if os.path.exists(index_path):
#         with open(index_path, 'r') as f:
#             existing_index = json.load(f)

#     # Determine if complete overwrite is needed
#     complete_overwrite = depth == -1

#     indexed_items = ({'depth': depth, 'items': {}} if
#                      complete_overwrite else existing_index)

#     try:
#         for root, dirs, files in os.walk(directory):
#             current_depth = root.count(os.sep) - directory_depth
#             if depth != -1 and current_depth > depth:
#                 continue

#             items = dirs if folders else files
#             for item in items:
#                 if item not in exceptions:
#                     full_path = os.path.join(root, item)
#                     # Update only if the path is within the current depth
#                     if complete_overwrite or (current_depth <=
#                                               existing_index['depth']):
#                         indexed_items['items'][item] = full_path

#         # Update depth only if we're overwriting
#         if complete_overwrite:
#             indexed_items['depth'] = depth

#         # Write updated index
#         with open(index_path, 'w') as f:
#             json.dump(indexed_items, f)

#     except Exception as e:
#         logging.error(f"Error occurred while indexing: {e}")
#         return {}

#     return indexed_items

# def index_directory(directory, exceptions, depth, folders):
#     """
#     Function to index all files or folders in a given directory.

#     Parameters:
#         directory (str): Path to index.
#         exceptions (list): List of subdir exceptions
#             (if folders=True, then will not index those folders either).
#         depth (int): Depth to index.
#         folders (bool): Whether to index folders instead of files.

#     Returns:
#         dict: Dictionary of files or folders in
#         given directory and subdirectories if depth is not 0.
#     """
#     indexed_items = {}

#     for root, dirs, files in os.walk(directory):
#         current_depth = root.count(os.sep) - directory.count(os.sep)
#         if depth != -1 and current_depth > depth:
#             continue

#         items = dirs if folders else files
#         for item in items:
#             if item not in exceptions:
#                 full_path = os.path.join(root, item)
#                 indexed_items[item] = full_path

#     return indexed_items


def index(directory, depth=-1, exceptions=[], folders=False, hidden=False):
    """
    Function to index all files and folders in a given directory.

    Parameters:
        directory (str): Path to index.
        depth (int, optional): Depth to index.
            Default is -1 (unlimited depth).
        exceptions (list, optional): List of items to exclude from indexing.
        folders (bool, optional): If True, only index folders, ignoring files.
        hidden (bool, optional): If True, include hidden files and folders.

    Returns:
        dict: Dictionary containing files and folders
            in the given directory and subdirectories.
    """
    indexed_items = {}

    # Define a recursive function to traverse directories
    def traverse_directory(current_dir, current_depth):
        if depth != -1 and current_depth > depth:
            return

        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if item not in exceptions:
                if os.path.isdir(item_path) or not folders:
                    if hidden or not item.startswith('.'):
                        indexed_items[item] = item_path

            if os.path.isdir(item_path):
                traverse_directory(item_path, current_depth + 1)

    # Start traversing from the given directory
    traverse_directory(directory, 0)

    return indexed_items
