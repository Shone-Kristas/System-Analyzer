import os
import magic

path = input('Введите путь до папки сканирования: ')

permissions_dict = {}
higher_threshold_dict = {}
sizes_dict = {}
categories_dict = {}
threshold_value = int(input('Введите пороговый размер файлов в bytes: '))


def file_permission(scan_file: str) -> dict:
    permission = oct(os.stat(scan_file).st_mode)[-3:]
    if (permission[-1] == "1" or "2" or "3" or "5" or "6" or "7") or (permission == "000" or "222" or "333" or "666" or "777"):
        if scan_file in permissions_dict:
            permissions_dict[permission].append(scan_file)
        else:
            permissions_dict[permission] = (scan_file)
    return permissions_dict

def search(path: str) -> dict:
    try:
        files_and_directories = os.listdir(path)
        for i in range(len(files_and_directories)):
            scan_file = path + '/' + files_and_directories[i]
            directory = os.path.isdir(scan_file)
            file_permission(scan_file)
            if directory == True:
                try:
                    search(scan_file)
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
                            sizes_dict[extension] += file_size       #Размер файлов
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

        return categories_dict, sizes_dict
    except Exception as e:
        print("Произошла ошибка:", e)


search(path)
for key, value in categories_dict.items():
  print("{0}: {1}".format(key, ', '.join(value)))
for key, value in sizes_dict.items():
  print("{0}: {1} bytes".format(key, value))
if higher_threshold_dict == {}:
    print("Нет файлов превышающих:", threshold_value, "bytes")
else:
    for key, value in higher_threshold_dict.items():
        print("Файлы превышающие порог в", threshold_value, "bytes: {0} - {1} bytes".format(key, value))
for key, value in permissions_dict.items():
  print("{0}: {1}".format(key, value))