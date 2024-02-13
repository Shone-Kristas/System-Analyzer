from src.main import file_permission
import os
import pytest



# def my_fakefs_test(fs):
#     # "fs" is the reference to the fake file system
#     fs.create_file("/var/data/xx1.txt")
#     assert os.path.exists("/var/data/xx1.txt")
# def test_file_permission(fs):
#     permissions_dict = {}
#     permissions_dict = file_permission(file_path, permissions_dict)
#     assert permissions_dict() == {'777': [file_path]}
# @pytest.fixture()
# def my_fakefs_test(fs):
#     # "fs" is the reference to the fake file system
#     filename = fs.create_file("C://xx1.txt", perm=0o777)
#     return filename
# def test_file_permission():
#     permissions_dict = {}
#     permissions_dict = file_permission(my_fakefs_test, permissions_dict)
#     assert permissions_dict() == {'777': [my_fakefs_test]}

# @pytest.mark.parametrize(
#     "filename, permission",
#     ["file1.txt", 0o777]
# )
# def test_file_permission(filename, permission):
#     permissions_dict = {}
#     permissions_dict = file_permission(filename, permissions_dict)
#     assert permissions_dict() == {'777': [filename]}


def test_file_permission():
    # Test case 2: check file with permission 644
    permissions_dict = {}
    filename = "file1.txt"
    os.chmod(filename, 0o444)
    permission = oct(os.stat(filename).st_mode)[-3:]
    assert permission == "444"
    # permissions_dict = file_permission(filename, permissions_dict)
    # assert permissions_dict == {'777': [filename]}
# test_file_permission()
# # Test case 3: check file with permission 000
# filename = "file3.txt"
# os.chmod(filename, 0o000)
# permissions_dict = file_permission(filename, permissions_dict)
# assert permissions_dict == {'777': [filename], '644': [filename], '000': [filename]}

# print("All tests passed")


