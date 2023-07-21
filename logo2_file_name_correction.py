import os
import re

dir = './export_logo2_512'    
for fileName in os.listdir(dir):
    new_fileName = re.sub('-+', '-', fileName)
    new_fileName = re.sub('-–-', '-', new_fileName)
    new_fileName = re.sub('-in-\d+', '', new_fileName)
    new_fileName = new_fileName.replace('Designed-for-', '')
    old_file_path = os.path.join(dir, fileName)
    new_file_path = os.path.join(dir, new_fileName)
    os.rename(old_file_path, new_file_path)
    
    print(fileName)
    print(new_fileName)