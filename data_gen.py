from datasets import load_dataset
import os
import shutil

directory = './dataset'
if not os.path.exists(directory):
    os.makedirs(directory)

def copy_images(dir):
    for file_name in os.listdir(dir):
        if file_name.endswith('.png'):
            source = os.path.join(dir, file_name)
            dest = os.path.join(directory, file_name)
            shutil.copyfile(source, dest)

copy_images('./export_logo_512')
copy_images('./export_logo2_512')

dataset = load_dataset("imagefolder", data_dir="./dataset", split="train")
dataset.push_to_hub("iamkaikai/amazing_logos_v2")
