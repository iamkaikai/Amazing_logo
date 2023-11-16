import matplotlib.font_manager
from PIL import Image, ImageDraw, ImageFont
import os

# Directory for saving images
output_dir = './data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get a list of system fonts
fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
font_size = 32
image_size = (512, 512)

# Iterate over each font
for font_path in fonts:

    # Create a blank image with white background for each font
    image = Image.new('RGB', image_size, color='white')
    draw = ImageDraw.Draw(image)

    # Extract the font name
    font_name = font_path.split('/')[-1].split('.')[0]
    # print(f'generating font: {font_name}')
    
    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
        if not all(font.getsize(char)[0] > 0 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            print(f'{font_name} not support!')
            continue  # Skip this font if it can't render all characters
        
    except IOError:
        continue  # Skip this font if it can't be loaded

    # Draw each character A-Z with the current font
    for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        x = image_size[0]*0.15 + (i % 13) * (image_size[0]*0.7 // 13)
        y = image_size[1]*0.4 + (1 + (i // 13)) * font_size
        draw.text((x, y), char, (0, 0, 0), font=font)

    # Save the image
    image.save(f'{output_dir}/{font_name}.png')
