import os
import magic
import time

path = input('Enter path to directions: ')
threshold_value = int(input('Enter the maximum file size in bytes: '))


def file_permission(file_path: str) -> dict:
    permissions_dict = {}
    permission = oct(os.stat(file_path).st_mode)[-3:]
    print(permission, file_path)
    if (permission[-1] in (1, 2, 3, 5, 6, 7)) or (permission == "000" or "222" or "333" or "666" or "777"):
        if permission in permissions_dict:
            permissions_dict[permission].append(file_path)
        else:
            permissions_dict[permission] = (file_path)
    return permissions_dict

def search(path: str) -> dict:
    start = time.time()
    categories_dict = {}
    sizes_dict = {}
    higher_threshold_dict = {}
    for root, dirs, files in os.walk(path):
        print(dirs)
        try:
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                permissions_dict = file_permission(file_path)
                print(1)
                with open(file_path, "rb") as f:
                    extension = magic.from_buffer(f.read(1024), mime=True)
                    if extension in categories_dict:
                        categories_dict[extension].append(file)
                        sizes_dict[extension] += file_size
                    else:
                        categories_dict[extension] = [file]
                        sizes_dict[extension] = file_size
                    if threshold_value < file_size:
                        higher_threshold_dict[file] = file_size
        except OSError as error:
            print("file opening error:", error)
    end = time.time() - start
    print(end)
    return categories_dict, sizes_dict, higher_threshold_dict, permissions_dict



    # try:
    #     files_and_directories = os.listdir(path)
    #     for i in range(len(files_and_directories)):
    #         scan_file = path + '/' + files_and_directories[i]
    #         directory = os.path.isdir(scan_file)
    #         file_permission(scan_file)
    #         if directory == True:
    #             try:
    #                 search(scan_file)
    #             except PermissionError:
    #                 print("No access:", scan_file)
    #             except Exception as e:
    #                 print("file opening error:", e)
    #         elif directory == False:
    #             try:
    #                 with open(scan_file, "rb") as f:
    #                     extension = magic.from_buffer(f.read(1024), mime=True)
    #                     file_size = os.path.getsize(scan_file)
    #                     if extension in categories_dict:
    #                         categories_dict[extension].append(files_and_directories[i])
    #                         sizes_dict[extension] += file_size       #Размер файлов
    #                     else:
    #                         categories_dict[extension] = [files_and_directories[i]]
    #                         sizes_dict[extension] = file_size
    #                     if files_and_directories[i] in higher_threshold_dict and threshold_value < file_size:
    #                         higher_threshold_dict[files_and_directories[i]] += file_size
    #                     elif threshold_value < file_size:
    #                         higher_threshold_dict[files_and_directories[i]] = file_size
    #             except FileNotFoundError:
    #                 print("file not found")
    #             except Exception as e:
    #                 print("file opening error:", e)
    #
    #     return categories_dict, sizes_dict
    # except Exception as e:
    #     print("error:", e)

def main():
    categories_dict, sizes_dict, higher_threshold_dict, permissions_dict = search(path)
    for key, value in categories_dict.items():
        print("{0}: {1}".format(key, ', '.join(value)))
    for key, value in sizes_dict.items():
        print("{0}: {1} bytes".format(key, value))
    if higher_threshold_dict == {}:
        print("No files larger than:", threshold_value, "bytes")
    else:
        for key, value in higher_threshold_dict.items():
            print("files are larger than", threshold_value, "bytes: {0} - {1} bytes".format(key, value))
    for key, value in permissions_dict.items():
        print("{0}: {1}".format(key, value))




if __name__ == "__main__":
    main()