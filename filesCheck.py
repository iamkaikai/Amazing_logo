import os
import filecmp

def get_file_set(directory):
    return set(os.path.splitext(file)[0] for file in os.listdir(directory))

def compare_directories(dir1, dir2):
    files_dir1 = get_file_set(dir1)
    files_dir2 = get_file_set(dir2)

    common = files_dir1 & files_dir2
    only_in_dir1 = files_dir1 - common
    only_in_dir2 = files_dir2 - common

    print(f'size of dir1 = {len(files_dir1)}')
    print(f'size of dir2 = {len(files_dir2)}')
    print(f'size of common = {len(common)}')
    # print(only_in_dir1)
    

    return only_in_dir1, only_in_dir2

dir1 = './logos/'  # replace with your first directory path
dir2 = './logos/export_512'  # replace with your second directory path

only_in_dir1, only_in_dir2 = compare_directories(dir1, dir2)

# print('Files only in {}:'.format(dir1))
# for file_name in only_in_dir1:
#     print(file_name)

# print('Files only in {}:'.format(dir2))
# for file_name in only_in_dir2:
#     print(file_name)

