import os
import magic
import time
import argparse


def file_permission(scan_file: str, permissions_dict: dict) -> dict:
    permission = oct(os.stat(scan_file).st_mode)[-3:]
    if (permission[-1] in (1, 2, 3, 5, 6, 7)) or (int(permission) in (000, 222, 333, 666, 777)):
        if permission in permissions_dict:
            permissions_dict[permission].append(scan_file)
        else:
            permissions_dict[permission] = [scan_file]
    return permissions_dict

def search(path: str, threshold_value: dict, higher_threshold_dict: dict, sizes_dict: dict, categories_dict: dict, permissions_dict: dict) -> dict:
    try:
        files_and_directories = os.listdir(path)
        for i in range(len(files_and_directories)):
            scan_file = path + '/' + files_and_directories[i]
            directory = os.path.isdir(scan_file)
            file_permission(scan_file, permissions_dict)
            if directory == True:
                try:
                    search(scan_file, threshold_value, higher_threshold_dict, sizes_dict, categories_dict, permissions_dict)
                except PermissionError:
                    print("Нет доступка к папке:", scan_file)
                except Exception as e:
                    print("Произошла ошибка при открытии файла:", e)
            elif directory == False:
                try:
                    with open(scan_file, "rb") as f:
                        extension = magic.from_buffer(f.read(1024), mime=True)
                        file_size = os.path.getsize(scan_file)
                        if extension in categories_dict:
                            categories_dict[extension].append(files_and_directories[i])
                            sizes_dict[extension] += file_size
                        else:
                            categories_dict[extension] = [files_and_directories[i]]
                            sizes_dict[extension] = file_size
                        if files_and_directories[i] in higher_threshold_dict and threshold_value < file_size:
                            higher_threshold_dict[files_and_directories[i]] += file_size
                        elif threshold_value < file_size:
                            higher_threshold_dict[files_and_directories[i]] = file_size
                except FileNotFoundError:
                    print("Файл не найден")
                except Exception as e:
                    print("Произошла ошибка при открытии файла:", e)
        return categories_dict, sizes_dict, higher_threshold_dict
    except Exception as e:
        print("Произошла ошибка:", e)


def main():
    higher_threshold_dict = {}
    sizes_dict = {}
    categories_dict = {}
    permissions_dict = {}
    parser = argparse.ArgumentParser(description='File System Analyzer with File Type Categorization')
    parser.add_argument('indir', type=str, help='Path to analyze (default is /)')
    parser.add_argument('invalue', type=int, help='Path to analyze (default is /)')
    args = parser.parse_args()

    path = args.indir
    threshold = args.invalue

    start = time.time()
    categories_dict, sizes_dict, higher_threshold_dict = search(path, threshold, higher_threshold_dict, sizes_dict, categories_dict, permissions_dict)
    for key, value in categories_dict.items():
        print("{0}: {1}".format(key, ', '.join(value)))
    for key, value in sizes_dict.items():
        print("{0}: {1} bytes".format(key, value))
    if higher_threshold_dict == {}:
        print("No files larger than:", threshold, "bytes")
    else:
        for key, value in higher_threshold_dict.items():
            print("files are larger than", threshold, "bytes: {0} - {1} bytes".format(key, value))
    for key, value in permissions_dict.items():
        print("{0}: {1}".format(key, value))
    end = time.time() - start
    print(end)


if __name__ == "__main__":
    main()