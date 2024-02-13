from src.main import file_permission
import os

def test_file_permission():
    # Test case: check file with permission 444
    permissions_dict = {}
    filename = "file1.txt"
    os.chmod(filename, 0o444)
    permissions_dict = file_permission(filename, permissions_dict)
    assert permissions_dict == {'444': [filename]}



