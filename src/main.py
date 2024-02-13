import os
import magic
import argparse

# Function to detect unusual permission settings
def file_permission(path_file: str, permissions_dict: dict) -> dict:
    permission = oct(os.stat(path_file).st_mode)[-3:]
    if (int(permission[-1]) in (1, 2, 3, 5, 6, 7)) or (
        int(permission) in (000, 222, 333, 666, 777)
    ):
        if permission in permissions_dict:
            permissions_dict[permission].append(path_file)
        else:
            permissions_dict[permission] = [path_file]
    return permissions_dict

# Function to search files through a catalog
def search(
    path: str,
    threshold_value: int,
    higher_threshold_dict: dict,
    sizes_dict: dict,
    categories_dict: dict,
    permissions_dict: dict,
) -> dict:
    try:
        files_and_directories = os.listdir(path)
        # Full cycle to check all the components in a catalog
        for i in range(len(files_and_directories)):
            path_file = os.path.join(path, files_and_directories[i])
            directory = os.path.isdir(path_file)
            # Check permissions of all components in a catalog
            file_permission(path_file, permissions_dict)
            if directory == True:
                try:
                    # Check inside catalogs
                    search(
                        path_file,
                        threshold_value,
                        higher_threshold_dict,
                        sizes_dict,
                        categories_dict,
                        permissions_dict,
                    )
                except Exception as e:
                    print("Failed to open the directory:", e)
            elif directory == False:
                try:
                    # File scan based on its signatures
                    with open(path_file, "rb") as f:
                        extension = magic.from_buffer(f.read(1024), mime=True)
                        file_size = os.path.getsize(path_file)
                        # Files classification based on categories, writes files' sizes into dictionary
                        if extension in categories_dict:
                            categories_dict[extension].append(files_and_directories[i])
                            sizes_dict[extension] += file_size
                        else:
                            categories_dict[extension] = [files_and_directories[i]]
                            sizes_dict[extension] = file_size
                        # Defining a file with a size above the set value
                        if (
                            files_and_directories[i] in higher_threshold_dict
                            and threshold_value < file_size
                        ):
                            higher_threshold_dict[files_and_directories[i]] += file_size
                        elif threshold_value < file_size:
                            higher_threshold_dict[files_and_directories[i]] = file_size
                except FileNotFoundError:
                    print("File not found")
                except Exception as e:
                    print("Failed to open the file:", e)
        return categories_dict, sizes_dict, higher_threshold_dict
    except Exception as e:
        print("Failed to open the folder:", e)


def main():
    # Dictionary for files with size above the set value
    higher_threshold_dict = {}
    # Dictionary to store categories' sizes
    sizes_dict = {}
    # Dictionary of categories and their contents
    categories_dict = {}
    # Dictionary of  unusual permission settings
    permissions_dict = {}
    parser = argparse.ArgumentParser(
        description="File System Analyzer with File Type Categorization"
    )
    # Defining of the directory to be scanned
    parser.add_argument("indir", type=str, help="Path to analyze (default is /)")
    # Setting the value to define files with size above this value
    parser.add_argument("invalue", type=int, help="Set size value: (default is byte)")
    args = parser.parse_args()

    path = args.indir
    threshold = args.invalue

    categories_dict, sizes_dict, higher_threshold_dict = search(
        path,
        threshold,
        higher_threshold_dict,
        sizes_dict,
        categories_dict,
        permissions_dict,
    )

    for key, value in categories_dict.items():
        print("{0}: {1}".format(key, ", ".join(value)))
    for key, value in sizes_dict.items():
        print("{0}: {1} bytes".format(key, value))
    if higher_threshold_dict == {}:
        print("No files above:", threshold, "bytes")
    else:
        for key, value in higher_threshold_dict.items():
            print(
                "files are above",
                threshold,
                "bytes: {0} - {1} bytes".format(key, value),
            )
    for key, value in permissions_dict.items():
        print("{0}: {1}".format(key, value))


if __name__ == "__main__":
    main()
