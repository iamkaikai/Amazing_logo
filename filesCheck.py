import os
import filecmp
import re

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

# dir1 = './logos/'  # replace with your first directory path
# dir2 = './logos/export_512'  # replace with your second directory path
# only_in_dir1, only_in_dir2 = compare_directories(dir1, dir2)

def clean_name(fileName):
    words_to_replace = ['design', 'logo', 'image', 'icon', 'Icon', 'LOGO', 'Logo', 'Icon', 'RGB']
    new_name = fileName
    for word in words_to_replace:
        new_name = new_name.replace(word, '')
    return new_name

def clean_double_space(fileName):
    new_name = fileName.replace('  ', ' ')
    return new_name

def clean_space_png(fileName):
    new_name = fileName.replace(' .png', '.png')
    return new_name

def remove_suffix_digit(fileName):
    new_name = re.sub('\d{1,2}$', '', fileName)
    new_name = new_name.replace(' -', '')
    return new_name

def rename(dir, curName, newName):
    path = dir + '/'    
    os.rename(path + curName, path + newName)
    print(f'----- [rename] from {curName}')
    print(f'----- [rename] to {newName}') 

dir = './logos3'
def name_check(dir):
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count = 0
    for fileName in os.listdir(dir):
        
        if fileName == '.DS_Store':
            continue      
        
        length = len(fileName.split('_'))
        
        if length == 1:
            print(fileName)
            print('\n-------')
            count_1 +=1
        
        elif length == 2:
            
            new_name = fileName.replace('.png','')     #remove .png
            list = new_name.split('_')
            if list[-1].isdigit():
                new_name = list[0]
            list = new_name.split('_')
            words_to_remove = ['design', 'logo', 'image', 'icon', 'Icon', 'LOGO', 'Logo', 'Icon', 'RGB', 'Logos', 'LogoLounge']
            new_list = [i for i in list if i not in words_to_remove]
            new_name = ' '.join(new_list) + '.png'      #add .png back
            rename(dir, fileName, new_name)
            
            count_2 +=1
            
        elif length == 3:
            
            count_3 +=1
        
        else:
            list = fileName.split('_')
            tags = list.pop()
            ind = list.pop()
            name = ' '.join(list)
            new_name = clean_name(name)
            new_name = clean_space_png(new_name)
            new_name = remove_suffix_digit(new_name)
            new_name = clean_double_space(new_name)
            new_name = '_'.join([new_name, ind, tags]).replace(' _', '_')
            rename(dir, fileName, new_name)

            count_4 +=1
   
    print(f'count_1 = {count_1} count_2 = {count_2} count_3 = {count_3} count_4 = {count_4}')
        
name_check(dir)


