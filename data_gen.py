from datasets import load_dataset
import pandas as pd
import os
import shutil
from PIL import Image
import traceback
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
from labeling3 import create_metadata_csv

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
   
def remove_duplicated_csv(dir):
    df = pd.read_csv(dir, header=None)
    df_unique = df.drop_duplicates(subset=df.columns[0], keep='first')
    output_path = "./long_name_unique.csv"
    df_unique.to_csv(output_path, index=False)
   
def move_long_to_new_dir():
    if not os.path.exists('logos3-long'):
        os.makedirs('logos3-long')
    
    df = pd.read_csv('long_name_unique.csv', header=None)
    for file_name in df.iloc[:, 0]:        
        source_path = f'./logos3/{file_name}'
        destination_path = f'./logos3-long/{file_name}'
        
        try:        
            print(f'Moving {file_name}...')
            shutil.move(source_path, destination_path)
        except Exception as e:
            print('-------------------------XX')
            print(f"An error occurred while moving '{file_name}': {e}")    
     
              
def copy_images(dir):
    count = 0
    total = len(os.listdir(dir))
    for file_name in os.listdir(dir):
        if file_name.endswith('.png'):
            source = os.path.join(dir, file_name)
            dest = os.path.join(directory, file_name)
            shutil.copyfile(source, dest)
            count +=1
            print(f'{count}/{total}')

def clean_folder(dir):
    print('start cleaning dir...')
    count = 0
    count_del = 0
    metadata = pd.read_csv(dir+'metadata.csv', lineterminator='\n')
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
            count_del +=1

    print('dir cleaned...')
    print(f'remove {count_del} files')
    
def clean_image_metadata(dir):
    count = 0
    total = len(os.listdir(dir))    
    for file_name in os.listdir(dir):
        if file_name in ['.DS_Store', 'metadata.csv'] :
            continue
        
        file_path = os.path.join(dir, file_name)
        try:
            # Read the image using OpenCV
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            
            # Check the number of channels in the image
            num_channels = img.shape[2] if len(img.shape) > 2 else 1

            # Convert RGBA images to RGB
            if num_channels == 4:
                # Create a white RGB image
                white_background = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8) * 255
                # Paste the RGBA image onto the white background
                mask = img[:,:,3] != 0  # Where the image is not transparent
                white_background[mask] = img[mask,:3]
                img = white_background
            
            # Save the image
            cv2.imwrite(os.path.join(dir, file_name), img)
            
        except:
            print(f'>>>>> sth wrong with {file_name}')
            print(file_path)
            traceback.print_exc()  # This will print the exception details

        count +=1
        print(f'{count}/{total}')

def rename_files_and_update_metadata(dir):
    print('start renaming files and updating metadata...')
    metadata = pd.read_csv(dir+'metadata.csv', lineterminator='\n')
    metadata.drop(metadata[metadata['file_name'] == 'log.txt'].index, inplace=True)
    metadata = metadata.reset_index(drop=True)

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
        

############## clean data ##############

# remove_duplicated_csv('./long_name.csv')    # remove dupliacted rows that have the same filename
move_long_to_new_dir()
# clean_image_metadata('./logos3')            # remove ICC profile in each image
# create_metadata_csv()                       # create metadata.csv for logos3 
# merge_csv()                                 # merge all three metadata.csv
# copy_images('./export_logo_512')            # copy images to dataset dir
# copy_images('./export_logo2_512')           # copy images to dataset dir
# copy_images('./logos3')                     # copy images to dataset dir
# clean_folder('./dataset/')                  # remove the images that are not in the metadata.csv
# rename_files_and_update_metadata('./dataset/')
# clean_image_metadata('./dataset')            # remove ICC profile in each image

############## clean data ##############

# dataset = load_dataset("imagefolder", data_dir="./dataset", split="train")
# print(dataset)

# images = dataset[90000:90010]['image']  # Get the first image from the dataset
# for image in images:
#     if isinstance(image, Image.Image):
#         plt.imshow(image)
#         plt.show()
#     # If the image is a numpy array, you might need to transpose it for correct visualization
#     elif isinstance(image, np.ndarray):
#         if image.shape[0] == 3:  # If the image has 3 channels
#             image = np.transpose(image, (1, 2, 0))  # Transpose it to (Height, Width, Channels)
#         plt.imshow(image)
#         plt.show()

# dataset.push_to_hub("iamkaikai/amazing_logos_v3")
