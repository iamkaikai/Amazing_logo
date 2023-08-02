from datasets import load_dataset
import pandas as pd
import os
import shutil
from PIL import Image
import traceback
import cv2
import numpy as np
import glob


directory = './dataset'
if not os.path.exists(directory):
    os.makedirs(directory)

def merge_csv():
    directory = './dataset'

    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # read the two CSV files
    df1 = pd.read_csv('./export_logo_512/metadata.csv')
    df2 = pd.read_csv('./export_logo2_512/metadata.csv')
    df3 = pd.read_csv('./logos3/metadata.csv')

    # concatenate the two dataframes along the rows
    merged_df = pd.concat([df1, df2, df3])

    # write the merged dataframe to a new CSV file
    merged_df.to_csv('./dataset/metadata.csv', index=False)
    
    
def copy_images(dir):
    for file_name in os.listdir(dir):
        if file_name.endswith('.png'):
            source = os.path.join(dir, file_name)
            dest = os.path.join(directory, file_name)
            shutil.copyfile(source, dest)


# Iterate over actual filenames
def clean_folder(dir):
    print('start cleaning dir...')
    count = 0
    metadata = pd.read_csv(dir+'metadata.csv')
    metadata_filenames = metadata['file_name'].tolist()
    actual_filenames = os.listdir(dir)
    
    for filename in actual_filenames:
        print(f'{count}/{len(actual_filenames)}...')
        count +=1
        if filename == 'metadata.csv':
            continue
        
        # If the filename is not in the metadata, delete it
        if filename not in metadata_filenames:
            file_path = os.path.join(dir, filename)
            os.remove(file_path)
            print(f'Removed file: {file_path}')

    print('dir cleaned...')
    

def rename_files_and_update_metadata(dir):
    print('start renaming files and updating metadata...')
    metadata = pd.read_csv(dir+'metadata.csv')
    metadata.drop(metadata[metadata['file_name'] == 'log.txt'].index, inplace=True)

    # Create a dictionary to store the new names
    new_names = {}

    # Iterate over the DataFrame
    for i, row in metadata.iterrows():
        old_name = row['file_name']
        new_name = f"{i:06d}.png"  # This will create names like 000001.jpg, 000002.jpg, etc.
        new_names[old_name] = new_name
        
        old_file_path = os.path.join(dir, old_name)
        new_file_path = os.path.join(dir, new_name)

        # Rename the file
        if os.path.exists(old_file_path):
            new_names[old_name] = new_name
            shutil.move(old_file_path, new_file_path)
            print(f"Renamed file: {old_file_path} to {new_file_path}")
        else:
            print(f"File not found: {old_file_path}. Skipping this file.")

    # Update the metadata DataFrame
    metadata['file_name'] = metadata['file_name'].map(new_names)

    # Save the updated metadata
    metadata.to_csv(dir+'metadata.csv', index=False)

    print('files renamed and metadata updated...')


def clean_image_metadata(dir):    
    for file_name in os.listdir(dir):
        if file_name in ['.DS_Store', 'metadata.csv'] :
            continue
        
        file_path = os.path.join(dir, file_name)
        print(file_path)
        try:
            img = Image.open(file_path)
            # Remove ICC profile if it exists
            if 'icc_profile' in img.info:
                del img.info['icc_profile']
            # Convert RGBA or LA images to RGB
            if img.mode in ['RGBA', 'LA']:
                # Create a white RGB image
                white_background = Image.new('RGB', img.size, (255, 255, 255))
                # Paste the RGBA or LA image onto the white background
                white_background.paste(img, mask=img.split()[-1])  # The alpha channel is the last channel in the image
                img = white_background
            elif img.mode in ['P','PNG']:
                img = img.convert('RGB')
            
            img.save(os.path.join(dir, file_name.replace('.png','.jpg')))
        except:
            print(f'>>>>> sth wrong with {file_name}')
            traceback.print_exc()  # This will print the exception details
            
def change_csv_png_to_jpg():
    df = pd.read_csv('./dataset/metadata.csv')
    df['file_name'] = df['file_name'].str.replace('.png', '.jpg')
    df.to_csv('./dataset/metadata.csv', index=False)


def clean_image_metadata(dir):    
    for file_name in os.listdir(dir):
        if file_name in ['.DS_Store', 'metadata.csv'] :
            continue
        
        file_path = os.path.join(dir, file_name)
        print(file_path)
        try:
            # Read the image using OpenCV
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            
            # Convert RGBA images to RGB
            if img.shape[2] == 4:
                # Create a white RGB image
                white_background = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255
                # Paste the RGBA image onto the white background
                mask = img[:,:,3] != 0  # Where the image is not transparent
                white_background[mask] = img[mask,:3]
                img = white_background
            
            # Save the image
            cv2.imwrite(os.path.join(dir, file_name.replace('.png','.jpg')), img)
        except:
            print(f'>>>>> sth wrong with {file_name}')
            traceback.print_exc()  # This will print the exception details

def remove_png_files(dir):
    # Get a list of all the png files in the directory
    png_files = glob.glob(os.path.join(dir, '*.png'))

    # Iterate over the list of filepaths & remove each file.
    for file in png_files:
        try:
            os.remove(file)
            print(f"File {file} has been removed successfully")
        except Exception as e:
            print(f"Error occurred while deleting file : {file}. Error : {str(e)}")

         
# from wand.image import Image
# os.environ['WAND_SUPPRESS_WARNINGS'] = 'True'

# def remove_icc_profile(file_path):
#     with Image(filename=file_path) as img:
#         img.profiles.clear()
#         img.save(filename=file_path)

# print('copying files from folders..')
# copy_images('./export_logo_512')
# copy_images('./export_logo2_512')
# copy_images('./logos3')
# rename_files_and_update_metadata("./dataset/")
# clean_folder('./dataset/')

# clean_image_metadata('./dataset')
# change_csv_png_to_jpg()
# remove_png_files('./dataset')

dataset = load_dataset("imagefolder", data_dir="./dataset", split="train")
print(dataset)
dataset.push_to_hub("iamkaikai/amazing_logos_v3")
