import os
from PIL import Image
from datasets import load_dataset

# Specify your directory
directory = './test'

# Get a list of all files in the directory
files_in_directory = os.listdir(directory)

# Iterate over the files
print('-------')
for file in files_in_directory:
    if file == '.DS_Store':
        continue
    
    # Construct the full file path
    file_path = os.path.join(directory, file)
    
    try:
        # Open the image file
        with Image.open(file_path) as img:
            # Convert the image to RGB mode
            print(f"Successfully opened image file {file}:\n {img.format}, size: {img.size}, mode: {img.mode}")
            # print(img.info)
            # rgb_img = img.convert('RGB')
            # Save the converted image
            # rgb_img.save(file_path)
    except Exception as e:
        # If an error occurs, print out the error and skip the file
        print(f"Error for file {file}: {e}")

# Now you can load the dataset
print('-------')
dataset = load_dataset("imagefolder", data_dir="./test")
dataset.push_to_hub("iamkaikai/amazing_logos_v3")
print(dataset)


